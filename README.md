# CaseFinder — Case Compatibility Checker

Look up which phone cases and screen protectors fit a given smartphone. Covers 67
models across Apple, Samsung, Google, OnePlus, Huawei, HTC, LG, Motorola, Xiaomi,
ZTE and Nokia.

**Try it online:** https://allsmartaccessories.com/tools/case-checker/

## Install

```bash
pip install casefinder
```

## Usage

```bash
casefinder brands                          # list supported brands
casefinder models --brand Samsung          # list Samsung models
casefinder check "iPhone 17"               # full compatibility report
casefinder check "Galaxy S24 Ultra" --json # raw JSON
```

## Example output

```
Apple iPhone 17 (2025)
MagSafe: yes
Compatible case types:
  - rugged
  - clear
  - slim
  - stylish
Screen protector: tempered-glass (curved)
Recommended cases: https://allsmartaccessories.com/top-10-best-iphone-17-cases-for-ultimate-protection-in-2026/
```

## Data

`data/phones.json` is the single source of truth, shared by the CLI and the web app —
`tests/test_sync.py` fails if the two copies drift apart. Each entry records the
release year, whether the phone supports MagSafe, compatible case types, screen
protector type, and a link to a full buying guide.

> Dimensions are not yet populated for every model (`dimensionsVerified: false`).
> The UI hides the dimensions row when the value is absent rather than guessing.

## Development

```bash
python -m pytest tests/ -q     # run the test suite
python -m build --wheel        # build a wheel
```

## License

MIT — see [LICENSE](LICENSE).
