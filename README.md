# trx

English word/phrase translator for the terminal. Uses any OpenAI-compatible LLM
endpoint and grounds definitions and IPA in a free dictionary
([dictionaryapi.dev](https://dictionaryapi.dev), Wiktionary data).

For each word or phrase it shows:

- meanings with examples
- translations ranked by estimated share of usage
- slang
- context-dependent translations

The output is coloured with truecolor themes.

```
╭──────────────────────────────────────────────────────────────╮
│ hey                                       ✓ dictionary + LLM │
│ /heɪ/  interjection                                          │
│ English → Polish                                             │
╰──────────────────────────────────────────────────────────────╯

◆ Meaning ──────────────────────────────────────────────────────
  1 informal greeting
     A casual way to say hello.
     ▎ “Hey, how's it going?”
     ▎ Cześć, co słychać?

◆ Translations · Polish · est. share of usage ──────────────────
   55% ██████████········  cześć
   30% █████▌············  hej
```

## Requirements

Python 3.8+ (standard library only), a truecolor terminal, and an API key for an
OpenAI-compatible endpoint (OpenAI, OpenRouter, a local LiteLLM/Ollama proxy, …).

## Install

```sh
git clone https://github.com/andrzejsantocki/trx.git
cd trx && ./install.sh
trx            # opens the setup menu
```

Optional: `alias tr=trx` in `~/.bashrc`. It affects interactive shells only, so
scripts still get `/usr/bin/tr`.

## Usage

```sh
trx get over that          # translate (default language from config)
trx -l German lore         # another target language, one call
trx --json lore            # raw JSON
trx                        # menu: key, URL, model, language, theme, test
trx --test                 # check endpoint, key and model
trx --themes               # preview themes
trx --theme nord           # save default theme
trx --theme nord lore      # theme for one call
```

Themes: default, dracula, catppuccin-mocha, tokyo-night, nord, gruvbox,
solarized-dark, one-dark, rose-pine, monokai. `NO_COLOR=1` or piping gives plain text.

## Configuration

Stored in `~/.config/tr/env` (mode 0600, written atomically by the menu):

| Key | Meaning |
|---|---|
| `TR_BASE_URL` | e.g. `https://api.openai.com/v1` |
| `TR_API_KEY` | API key; may be `${SOME_ENV_VAR}` to avoid storing it |
| `TR_MODEL` | model id, e.g. `gpt-4o-mini` |
| `TR_LANG` | target language (default Polish) |
| `TR_FALLBACK_URL` | optional second endpoint |
| `TR_THEME` | color theme |
| `TR_TIMEOUT` | request timeout seconds (default 90) |
| `TR_NO_DICT` | `1` disables the dictionary lookup |

Values in the config file override `TR_*` shell variables.

## Accuracy

- Definitions and IPA come from the dictionary when an entry exists. The header
  shows which source was used: `✓ dictionary + LLM` or `◇ LLM only`.
- Most phrases have no dictionary entry and are LLM-only.
- Translations, usage percentages and slang are LLM estimates.

## Privacy

Each lookup sends the input text to dictionaryapi.dev and to your configured LLM
endpoint. Set `TR_NO_DICT=1` to skip the dictionary.

## Tests

```sh
python3 test_trx.py   # offline, no network
```

## License

MIT
