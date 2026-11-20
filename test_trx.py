"""Offline self-checks: python3 test_trx.py (no network, no real config touched)."""
import importlib.machinery, importlib.util, io, os, stat, sys, tempfile
from contextlib import redirect_stdout

here = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("trx", os.path.join(here, "trx"))
trx = importlib.util.module_from_spec(importlib.util.spec_from_loader("trx", loader))
loader.exec_module(trx)

tmp = tempfile.mkdtemp()
trx.CFG = os.path.join(tmp, "env")
for k in list(os.environ):
    if k.startswith("TR_"): del os.environ[k]

# config: atomic 0600 save, round-trip, ${VAR} expansion, unresolved -> unset
trx.save_cfg({"TR_API_KEY": "secret-123456", "TR_LANG": "Polish", "TR_MODEL": ""})
assert stat.S_IMODE(os.stat(trx.CFG).st_mode) == 0o600
assert trx.read_cfg() == {"TR_API_KEY": "secret-123456", "TR_LANG": "Polish"}
os.environ["TRX_TEST_KEY"] = "from-env"
open(trx.CFG, "a").write("TR_BASE_URL=${TRX_TEST_KEY}\nTR_FALLBACK_URL=${TRX_MISSING}\n")
cfg = trx.read_cfg()
assert cfg["TR_BASE_URL"] == "from-env" and cfg["TR_FALLBACK_URL"] == ""

# config file overrides stale shell vars
os.environ["TR_API_KEY"] = "stale"
trx.load_cfg()
assert os.environ["TR_API_KEY"] == "secret-123456"

# masking never reveals more than last 4 chars
assert trx.mask("secret-123456") == "****3456" and trx.mask("short") == "****" and trx.mask("") == "(unset)"

# themes: all parse; unknown falls back to default
for name in trx.THEMES:
    t = trx.theme(name)
    assert len(t) == 7 and all(len(v) == 3 and all(0 <= x <= 255 for x in v) for v in t.values()), name
assert trx.theme("nope") == trx.theme("default")

# --theme NAME with no text saves theme
assert trx.main(["--theme", "nord"]) == 0 and trx.read_cfg()["TR_THEME"] == "nord"
assert trx.main(["--theme", "bogus"]) == 2

# render: plain output (not a TTY) has no ANSI and shows every section
d = {"input": "hey", "ipa": "/heɪ/", "part_of_speech": ["interjection"], "_dict": True,
     "meaning": [{"sense": "greeting", "explanation": "hello", "example_en": "Hey!", "example_tr": "Cześć!"}],
     "translations": [{"text": "cześć", "usage_pct": 70, "note": ""}, {"text": "hej", "usage_pct": 30, "note": "casual"}],
     "slang": [], "context": [{"situation": "Hey, guys!", "tr": "Cześć, ludzie!", "note": ""}]}
buf = io.StringIO()
with redirect_stdout(buf): trx.render(d, "Polish")
out = buf.getvalue()
assert "\033[" not in out
for s in ("hey", "/heɪ/", "dictionary + LLM", "Meaning", "cześć", "70%", "none known", "Cześć, ludzie!"):
    assert s in out, s

print("all checks passed")
