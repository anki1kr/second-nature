"""What is left on each AI key and agent, read from the only places that actually know.

WHY: the only way to find out that a key or agent was exhausted used to be to send it work and watch it fail.
This reads real numbers where a real number exists and says "unknown" where none does. It never guesses, and it
never prints a key. Values are never printed, logged, or served.

    python limits.py                      # one table, now
    python limits.py --serve 8787         # a page at http://127.0.0.1:8787 that refreshes itself
    python limits.py --json               # same data for a script
    python limits.py --groq               # also spend one tiny Groq call to read its rate-limit headers
    python limits.py --anthropic          # also spend one tiny Anthropic call to read its rate-limit headers
    python limits.py --openai             # also spend one tiny OpenAI call to read its rate-limit headers
    python limits.py --env .env --site https://example.com

What can and cannot be known:
  OpenRouter  GET /api/v1/key returns this key's limit, usage and rate limit. Free and exact.
  Groq        No quota endpoint. The limits ride on the headers of a real call, so this costs one
              1-token request per key and only runs with --groq.
  Anthropic   No quota endpoint. Limits ride on headers of a real call; costs one 1-token request
              and only runs with --anthropic.
  OpenAI      No quota endpoint. Limits ride on headers of a real call; costs one 1-token request
              and only runs with --openai.
  Bing        The URL submission API returns the day's remaining quota for a registered site. Free.
              Needs BING_WEBMASTER_API_KEY plus --site (or BING_SITE_URL).
  CDP app     An AI desktop app that runs with a Chrome DevTools debug port may expose its own quota in a
              window title; that text is readable over CDP. Configure with --cdp-port. Otherwise: unknown.
  Claude Code, Gemini API keys, other agents
              No local API and no file on disk that holds a balance. Reported as unknown on purpose,
              with where the number actually lives, instead of a number invented here.
"""

from __future__ import annotations

import argparse
import json
import re
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TIMEOUT = 12


def load_env(env_file: str | None) -> dict[str, str]:
    """Keys come from the environment first, then one optional .env file. Values are never printed."""
    out = dict(os.environ)
    if env_file:
        path = Path(env_file).expanduser()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            print(f"note: .env file not readable: {path}", file=sys.stderr)
            return out
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            out.setdefault(name.strip(), value.strip().strip('"').strip("'"))
    return out


def get_json(url: str, headers: dict[str, str], data: bytes | None = None) -> tuple[dict | None, dict, str | None]:
    # Some providers sit behind Cloudflare, which answers 403 to Python's default User-Agent: a false "bad key".
    headers = {"User-Agent": "agent-limits/1.0", **headers}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read().decode("utf-8", "replace")
            return (json.loads(body) if body.strip().startswith(("{", "[")) else None), dict(resp.headers), None
    except urllib.error.HTTPError as exc:
        code = ""
        try:  # only the provider's short machine code (e.g. model_permission_blocked_project), never the body text
            err = json.loads(exc.read().decode("utf-8", "replace")).get("error") or {}
            raw = str(err.get("code") or err.get("type") or "")
            code = raw if re.fullmatch(r"[a-z0-9_]{3,60}", raw) else ""
        except Exception:
            pass
        return None, dict(exc.headers or {}), f"HTTP {exc.code}" + (f" {code}" if code else "")
    except Exception as exc:  # network down, DNS, timeout
        return None, {}, str(exc)[:80]


def openrouter(env: dict[str, str]) -> list[dict]:
    names = ["OPENROUTER_API_KEY"] + [f"OPENROUTER_API_KEY_{i}" for i in range(2, 10)]
    for i in range(1, 10):
        legacy = f"OPKEY{i}"
        generic = "OPENROUTER_API_KEY" if i == 1 else f"OPENROUTER_API_KEY_{i}"
        if env.get(legacy) and (not env.get(generic) or env.get(legacy) != env.get(generic)):
            names.append(legacy)
    rows = []
    for name in names:
        key = (env.get(name) or "").strip()
        if not key:
            continue
        data, _headers, err = get_json("https://openrouter.ai/api/v1/key", {"Authorization": f"Bearer {key}"})
        if err or not data:
            if key and err and key in err:
                err = "connection error"
            rows.append({"source": f"OpenRouter {name}", "state": "error", "detail": err or "no body"})
            continue
        d = data.get("data", data)
        limit, usage = d.get("limit"), d.get("usage")
        spent = round(float(usage or 0), 4)
        left = f"no cap, {spent} spent" if limit is None else f"{round(float(limit) - spent, 4)} of {limit} left"
        rows.append({
            "source": f"OpenRouter {name}",
            "state": "ok",
            "detail": f"credits {left}; free tier {'yes' if d.get('is_free_tier') else 'no'}"
                      + (f"; {d['rate_limit']['requests']}/{d['rate_limit']['interval']}" if d.get("rate_limit") else ""),
        })
    return rows


def groq(env: dict[str, str]) -> list[dict]:
    """Groq publishes nothing to read, so this sends the smallest possible call and keeps the headers."""
    names = ["GROQ_API_KEY"] + [f"GROQ_API_KEY_{i}" for i in range(2, 12)]
    for i in range(2, 12):
        legacy = f"GROQ_API_KEY{i}"
        generic = f"GROQ_API_KEY_{i}"
        if env.get(legacy) and (not env.get(generic) or env.get(legacy) != env.get(generic)):
            names.append(legacy)
    model = (env.get("GROQ_MODELS") or "openai/gpt-oss-20b").split(",")[0].strip()
    rows = []
    for name in names:
        key = (env.get(name) or "").strip()
        if not key:
            continue
        payload = json.dumps({"model": model, "max_tokens": 1, "messages": [{"role": "user", "content": "1"}]}).encode()
        _data, headers, err = get_json(
            "https://api.groq.com/openai/v1/chat/completions",
            {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            data=payload,
        )
        if key and err and key in err:
            err = "connection error"
        h = {k.lower(): v for k, v in headers.items()}
        remaining_r = h.get("x-ratelimit-remaining-requests")
        remaining_t = h.get("x-ratelimit-remaining-tokens")
        if remaining_r or remaining_t:
            reset = h.get("x-ratelimit-reset-requests") or "?"
            rows.append({"source": f"Groq {name}", "state": "ok",
                         "detail": f"requests left {remaining_r}, tokens left {remaining_t}, resets in {reset}"})
        else:
            rows.append({"source": f"Groq {name}", "state": "error",
                         "detail": (err or "no rate-limit headers") + (f" (model {model})" if not err else "")})
    return rows


def anthropic(env: dict[str, str]) -> list[dict]:
    """One 1-token message to read rate-limit headers. Never echoes response body."""
    key = (env.get("ANTHROPIC_API_KEY") or "").strip()
    if not key:
        return [{"source": "Anthropic", "state": "unknown", "detail": "needs ANTHROPIC_API_KEY"}]
    model = (env.get("ANTHROPIC_PROBE_MODEL") or "claude-haiku-4-5").strip()
    payload = json.dumps({"model": model, "max_tokens": 1, "messages": [{"role": "user", "content": "1"}]}).encode()
    _data, headers, err = get_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        data=payload,
    )
    if err:
        if key and key in err:
            err = "connection error"
        return [{"source": "Anthropic", "state": "error", "detail": err}]
    h = {k.lower(): v for k, v in headers.items()}
    remaining_r = h.get("anthropic-ratelimit-requests-remaining")
    remaining_t = h.get("anthropic-ratelimit-tokens-remaining")
    reset_r = h.get("anthropic-ratelimit-requests-reset")
    reset_t = h.get("anthropic-ratelimit-tokens-reset")
    reset = reset_r or reset_t or h.get("anthropic-ratelimit-reset") or "?"
    if remaining_r or remaining_t:
        return [{
            "source": "Anthropic",
            "state": "ok",
            "detail": f"requests left {remaining_r}, tokens left {remaining_t}, resets in {reset}",
        }]
    return [{
        "source": "Anthropic",
        "state": "error",
        "detail": f"no rate-limit headers (model {model})",
    }]


def openai(env: dict[str, str]) -> list[dict]:
    """One 1-token completion to read rate-limit headers. Never echoes response body."""
    key = (env.get("OPENAI_API_KEY") or "").strip()
    if not key:
        return [{"source": "OpenAI", "state": "unknown", "detail": "needs OPENAI_API_KEY"}]
    model = (env.get("OPENAI_PROBE_MODEL") or "gpt-4o-mini").strip()
    payload = json.dumps({"model": model, "max_tokens": 1, "messages": [{"role": "user", "content": "1"}]}).encode()
    _data, headers, err = get_json(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=payload,
    )
    if err:
        if key and key in err:
            err = "connection error"
        return [{"source": "OpenAI", "state": "error", "detail": err}]
    h = {k.lower(): v for k, v in headers.items()}
    remaining_r = h.get("x-ratelimit-remaining-requests")
    remaining_t = h.get("x-ratelimit-remaining-tokens")
    reset = h.get("x-ratelimit-reset-requests") or "?"
    if remaining_r or remaining_t:
        return [{
            "source": "OpenAI",
            "state": "ok",
            "detail": f"requests left {remaining_r}, tokens left {remaining_t}, resets in {reset}",
        }]
    return [{
        "source": "OpenAI",
        "state": "error",
        "detail": f"no rate-limit headers (model {model})",
    }]


def bing(env: dict[str, str], site: str | None) -> list[dict]:
    key = (env.get("BING_WEBMASTER_API_KEY") or "").strip()
    site = site or (env.get("BING_SITE_URL") or "").strip()
    if not key or not site:
        return [{"source": "Bing URL submission", "state": "unknown",
                 "detail": "needs BING_WEBMASTER_API_KEY and --site (or BING_SITE_URL)"}]
    url = ("https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota"
           f"?apikey={key}&siteUrl={urllib.parse.quote(site, safe='')}")
    data, _h, err = get_json(url, {"Accept": "application/json"})
    if err or not data:
        if key and err and key in err:
            err = "connection error"
        return [{"source": "Bing URL submission", "state": "error", "detail": err or "no body"}]
    d = data.get("d", data)
    return [{"source": "Bing URL submission", "state": "ok",
             "detail": f"daily left {d.get('DailyQuota')}, monthly left {d.get('MonthlyQuota')}"}]


def cdp_app(port: int) -> list[dict]:
    """An AI desktop app with a CDP debug port may show its own quota in a window title."""
    data, _h, err = get_json(f"http://127.0.0.1:{port}/json/list", {})
    if err:
        return [{"source": f"CDP app (port {port})", "state": "unknown",
                 "detail": "not reachable; an AI desktop app exposes quota over CDP only while it runs"
                           " with a remote-debugging port open"}]
    titles = [t.get("title", "") for t in (data or [])] if isinstance(data, list) else []
    hit = next((t for t in titles if "%" in t and "quota" in t.lower()), None)
    return [{"source": f"CDP app (port {port})", "state": "ok" if hit else "unknown",
             "detail": hit or "app is running; the quota text is inside the window, open it to read"}]


NO_API = [
    ("Claude Code", "/usage inside the CLI only; nothing a script can read locally"),
    ("Gemini API keys", "Google publishes no quota endpoint for an API key"),
    ("Other agents", "see each provider's dashboard"),
]


def collect(
    with_groq: bool = False,
    env_file: str | None = None,
    site: str | None = None,
    cdp_port: int = 9333,
    with_anthropic: bool = False,
    with_openai: bool = False,
) -> list[dict]:
    env = load_env(env_file)
    rows: list[dict] = []
    rows += openrouter(env)
    if with_groq:
        rows += groq(env)
    else:
        rows.append({"source": "Groq keys", "state": "skipped",
                     "detail": "run with --groq: the limits only ride on a real call's headers"})
    if with_anthropic:
        rows += anthropic(env)
    else:
        rows.append({"source": "Anthropic", "state": "skipped",
                     "detail": "run with --anthropic: the limits only ride on a real call's headers"})
    if with_openai:
        rows += openai(env)
    else:
        rows.append({"source": "OpenAI", "state": "skipped",
                     "detail": "run with --openai: the limits only ride on a real call's headers"})
    rows += bing(env, site)
    rows += cdp_app(cdp_port)
    rows += [{"source": name, "state": "unknown", "detail": why} for name, why in NO_API]
    return rows


def print_table(rows: list[dict]) -> None:
    width = max((len(r["source"]) for r in rows), default=20) + 2
    mark = {"ok": "ok ", "error": "ERR", "unknown": " ? ", "skipped": " - "}
    for r in rows:
        print(f"{mark.get(r['state'], '   ')} {r['source']:<{width}} {r['detail']}")


HTML = """<!doctype html><html><head><meta charset="utf-8"><title>Agent limits</title>
<meta http-equiv="refresh" content="60">
<style>
 body{font:14px/1.5 system-ui,sans-serif;margin:24px;background:#f6f5f1;color:#0f172a}
 h1{font-size:18px;margin:0 0 4px} p{color:#5a6a80;margin:0 0 18px}
 table{border-collapse:collapse;width:100%;max-width:900px;background:#fff;border:1px solid #e5e3dc}
 td,th{padding:8px 12px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}
 th{background:#faf9f6;font-weight:600}
 .ok{color:#146c34}.error{color:#b91c1c}.unknown,.skipped{color:#5a6a80}
</style></head><body>
<h1>What is left</h1><p>Read live. Refreshes every 60 seconds. Unknown means no local source exists, not zero.</p>
<table><tr><th>Source</th><th>State</th><th>Detail</th></tr>%s</table></body></html>"""


def serve(
    port: int,
    with_groq: bool = False,
    env_file: str | None = None,
    site: str | None = None,
    cdp_port: int = 9333,
    with_anthropic: bool = False,
    with_openai: bool = False,
) -> None:
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path.startswith("/json"):
                body = json.dumps(
                    collect(
                        with_groq=with_groq,
                        env_file=env_file,
                        site=site,
                        cdp_port=cdp_port,
                        with_anthropic=with_anthropic,
                        with_openai=with_openai,
                    ),
                    indent=2,
                ).encode()
                ctype = "application/json"
            else:
                rows = collect(
                    with_groq=with_groq,
                    env_file=env_file,
                    site=site,
                    cdp_port=cdp_port,
                    with_anthropic=with_anthropic,
                    with_openai=with_openai,
                )
                cells = "".join(
                    f"<tr><td>{r['source']}</td><td class='{r['state']}'>{r['state']}</td><td>{r['detail']}</td></tr>"
                    for r in rows
                )
                body = (HTML % cells).encode()
                ctype = "text/html; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_args):  # keep the console quiet
            return

    print(f"Agent limits on http://127.0.0.1:{port}  (JSON at /json, Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--serve", type=int, metavar="PORT", default=None)
    parser.add_argument("--groq", action="store_true", help="spend one 1-token call per Groq key to read its headers")
    parser.add_argument("--anthropic", action="store_true", help="spend one 1-token call to read Anthropic rate-limit headers")
    parser.add_argument("--openai", action="store_true", help="spend one 1-token call to read OpenAI rate-limit headers")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--env", default=None, metavar="FILE",
                        help="path to a .env file to read keys from (keys in the environment win)")
    parser.add_argument("--site", default=None, metavar="URL",
                        help="registered site URL for the Bing URL submission quota (or set BING_SITE_URL)")
    parser.add_argument("--cdp-port", type=int, default=9333, metavar="PORT",
                        help="Chrome DevTools debug port of an AI desktop app to probe (default 9333)")
    args = parser.parse_args()
    if args.serve:
        serve(
            args.serve,
            with_groq=args.groq,
            env_file=args.env,
            site=args.site,
            cdp_port=args.cdp_port,
            with_anthropic=args.anthropic,
            with_openai=args.openai,
        )
        return 0
    rows = collect(
        with_groq=args.groq,
        env_file=args.env,
        site=args.site,
        cdp_port=args.cdp_port,
        with_anthropic=args.anthropic,
        with_openai=args.openai,
    )
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
