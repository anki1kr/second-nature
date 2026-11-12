"""Tests for agent-limits: limits.py."""

from pathlib import Path
import sys
import unittest

# Ensure the directory of limits.py is importable regardless of working directory
sys.path.insert(0, str(Path(__file__).parent.resolve()))
import limits


class TestAgentLimits(unittest.TestCase):
    def setUp(self):
        self._orig_get_json = limits.get_json

    def tearDown(self):
        limits.get_json = self._orig_get_json

    def test_back_compat_names_read_openrouter(self):
        def mock_get_json(url, headers, data=None):
            return {"data": {"limit": 10.0, "usage": 2.5, "is_free_tier": False}}, {}, None

        limits.get_json = mock_get_json
        env = {"OPKEY2": "legacy-or-key-val"}
        rows = limits.openrouter(env)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "OpenRouter OPKEY2")
        self.assertEqual(rows[0]["state"], "ok")
        self.assertIn("7.5 of 10.0 left", rows[0]["detail"])

    def test_back_compat_names_read_groq(self):
        def mock_get_json(url, headers, data=None):
            h = {
                "x-ratelimit-remaining-requests": "30",
                "x-ratelimit-remaining-tokens": "6000",
                "x-ratelimit-reset-requests": "1.5s",
            }
            return None, h, None

        limits.get_json = mock_get_json
        env = {"GROQ_API_KEY2": "gsk-legacy-val"}
        rows = limits.groq(env)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "Groq GROQ_API_KEY2")
        self.assertEqual(rows[0]["state"], "ok")
        self.assertIn("requests left 30", rows[0]["detail"])

    def test_generic_names_read(self):
        def mock_get_json(url, headers, data=None):
            if "openrouter" in url:
                return {"data": {"limit": 5.0, "usage": 1.0, "is_free_tier": True}}, {}, None
            return None, {"x-ratelimit-remaining-requests": "10", "x-ratelimit-remaining-tokens": "2000"}, None

        limits.get_json = mock_get_json
        or_rows = limits.openrouter({"OPENROUTER_API_KEY_2": "generic-or-key"})
        self.assertEqual(len(or_rows), 1)
        self.assertEqual(or_rows[0]["source"], "OpenRouter OPENROUTER_API_KEY_2")

        groq_rows = limits.groq({"GROQ_API_KEY_2": "generic-groq-key"})
        self.assertEqual(len(groq_rows), 1)
        self.assertEqual(groq_rows[0]["source"], "Groq GROQ_API_KEY_2")

    def test_missing_anthropic_key_unknown(self):
        rows = limits.anthropic({})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "Anthropic")
        self.assertEqual(rows[0]["state"], "unknown")
        self.assertIn("ANTHROPIC_API_KEY", rows[0]["detail"])

    def test_missing_openai_key_unknown(self):
        rows = limits.openai({})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "OpenAI")
        self.assertEqual(rows[0]["state"], "unknown")
        self.assertIn("OPENAI_API_KEY", rows[0]["detail"])

    def test_header_parsing_anthropic(self):
        def mock_get_json(url, headers, data=None):
            self.assertEqual(url, "https://api.anthropic.com/v1/messages")
            self.assertEqual(headers.get("x-api-key"), "ant-test-key")
            self.assertEqual(headers.get("anthropic-version"), "2023-06-01")
            h = {
                "anthropic-ratelimit-requests-remaining": "45",
                "anthropic-ratelimit-tokens-remaining": "38400",
                "anthropic-ratelimit-requests-reset": "2026-11-12T10:00:00Z",
            }
            return None, h, None

        limits.get_json = mock_get_json
        rows = limits.anthropic({"ANTHROPIC_API_KEY": "ant-test-key"})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "Anthropic")
        self.assertEqual(rows[0]["state"], "ok")
        self.assertIn("45", rows[0]["detail"])
        self.assertIn("38400", rows[0]["detail"])
        self.assertIn("2026-11-12T10:00:00Z", rows[0]["detail"])

    def test_header_parsing_openai(self):
        def mock_get_json(url, headers, data=None):
            self.assertEqual(url, "https://api.openai.com/v1/chat/completions")
            self.assertEqual(headers.get("Authorization"), "Bearer oai-test-key")
            h = {
                "x-ratelimit-remaining-requests": "999",
                "x-ratelimit-remaining-tokens": "199950",
                "x-ratelimit-reset-requests": "6ms",
            }
            return None, h, None

        limits.get_json = mock_get_json
        rows = limits.openai({"OPENAI_API_KEY": "oai-test-key"})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source"], "OpenAI")
        self.assertEqual(rows[0]["state"], "ok")
        self.assertIn("999", rows[0]["detail"])
        self.assertIn("199950", rows[0]["detail"])
        self.assertIn("6ms", rows[0]["detail"])

    def test_error_row_never_contains_key_anthropic(self):
        secret_key = "sk-ant-api03-verysecretstring98765"

        def mock_get_json(url, headers, data=None):
            return None, {}, "HTTP 401"

        limits.get_json = mock_get_json
        rows = limits.anthropic({"ANTHROPIC_API_KEY": secret_key})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["state"], "error")
        self.assertEqual(rows[0]["detail"], "HTTP 401")
        self.assertNotIn(secret_key, rows[0]["detail"])
        self.assertNotIn(secret_key, str(rows[0]))

    def test_error_row_never_contains_key_openai(self):
        secret_key = "sk-proj-verysecretstring12345"

        def mock_get_json(url, headers, data=None):
            return None, {}, "HTTP 429"

        limits.get_json = mock_get_json
        rows = limits.openai({"OPENAI_API_KEY": secret_key})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["state"], "error")
        self.assertEqual(rows[0]["detail"], "HTTP 429")
        self.assertNotIn(secret_key, rows[0]["detail"])
        self.assertNotIn(secret_key, str(rows[0]))

    def test_no_flags_collect_contains_full_table(self):
        rows = limits.collect()
        sources = [r["source"] for r in rows]
        self.assertIn("Groq keys", sources)
        self.assertIn("Anthropic", sources)
        self.assertIn("OpenAI", sources)
        self.assertIn("Bing URL submission", sources)
        self.assertIn("Other agents", sources)


if __name__ == "__main__":
    unittest.main()
