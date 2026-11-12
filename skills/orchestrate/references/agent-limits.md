
# Agent limits

The only way to learn that a key or agent was empty used to be to send it work and watch it fail. This reads the real
number where one exists and says **unknown** where none does. It never guesses and it never prints a key.

```bash
python scripts/limits.py                       # table, now
python scripts/limits.py --serve 8787          # page at http://127.0.0.1:8787, refreshes itself
python scripts/limits.py --json                # same data for a script
python scripts/limits.py --groq                # reads Groq limits (costs one 1-token call per key)
python scripts/limits.py --anthropic           # reads Anthropic limits (costs one 1-token call)
python scripts/limits.py --openai              # reads OpenAI limits (costs one 1-token call)
python scripts/limits.py --env .env --site https://example.com
```

Standard library only, no install, no network except the providers it asks.

| Source | What it reports | How |
| --- | --- | --- |
| OpenRouter | credits left or spent, free-tier flag, rate limit, per key (`OPENROUTER_API_KEY`, `OPENROUTER_API_KEY_2..9`, legacy `OPKEY1..9`) | `GET /api/v1/key`, free |
| Groq | requests and tokens left, reset time, per key (`GROQ_API_KEY`, `GROQ_API_KEY_2..11`) | only on `--groq`: spends one 1-token request per key |
| Anthropic | requests and tokens left, reset time (`ANTHROPIC_API_KEY`) | only on `--anthropic`: spends one 1-token request |
| OpenAI | requests and tokens left, reset time (`OPENAI_API_KEY`) | only on `--openai`: spends one 1-token request |
| Bing | URL submissions left today and this month | the webmaster API; needs the key plus `--site` (or `BING_SITE_URL`) |
| CDP app | whether an AI desktop app that keeps a Chrome DevTools debug port open is up, and its quota when a window title exposes it | `--cdp-port` (default 9333) |
| Claude Code, Gemini API keys, other agents | **unknown**, with where the number actually lives | no local API exists; inventing one would be worse than saying so |

Keys are read from the environment first, then from the `.env` file given with `--env`. Values are never printed,
logged or served; only the derived numbers are. With no keys set the script still prints the full table, with
`unknown` on every row that needs one.
