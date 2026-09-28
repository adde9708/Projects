# AGENTS.md

Personal sandbox of ~66 standalone Python scripts (`adde9708/Projects`, default branch `main`).
Not an application, not a package. There is no product to run.

## Shape of the repo

- Flat: 63 scripts sit at the repo root. Three subprojects live in subdirectories:
  `login/login/` (Ada Super Computer, co-authored with a friend, has its own README +
  `requirements.txt`), `mobile_app/` (kivy calculator), `quantization_tutorial/` (PyTorch QAT).
- No `pyproject.toml` or `setup.py`, and no CI workflows. Nothing is installable. The only
  `requirements.txt` is scoped to `login/login/` and is not a lockfile.
- Each `.py` is its own entrypoint: run it directly, `python <script>.py`, **from the repo root**
  (exceptions below).

## `84702ee` was a mass deletion — files are recoverable

Commit `84702ee` ("made some changes", 2025-01-25) deleted ~200 MB: all of `mobile_app/`,
`login/login/Assets/`, and `quantization_tutorial/` (including its 398-image dataset). It was
housekeeping bundled with a legitimate `calculator_wx_python.py` refactor, so it reads as
intentional in `git log` but was arguably over-broad.

The kivy app, the Ada audio assets, the quantization script, and its dataset have since been
restored from `84702ee^`. **Compiled binaries were deliberately left out** (`KvCalc.exe`, both
`SecondIteration.exe`, `python37.dll`) — don't "restore" them without asking.

To recover anything still missing:

```
git restore --source=84702ee^ -- <path>
```

**Never `git revert 84702ee`.** That commit also *added* `speed_test.py` and `wx_python_test.py`
and *modified* `calculator_wx_python.py`, so reverting it would delete live files and roll back
nine later commits to the calculator. Path-scoped `git restore` is the only safe tool here.

## No dependency manifest — read the imports

Dependencies must be discovered by reading a script's imports; there is no lockfile. The local
interpreter is an ad-hoc global Python 3.14 with only some of these installed:

| Installed | NOT installed |
| --- | --- |
| `pygame-ce` (provides the `pygame` module), `numpy`, `pandas`, `scipy`, `requests`, `bs4`/`beautifulsoup4`, `wx`, `gspread`, `google-auth*` | `kivy`, `torch`, `torchvision`, `matplotlib`, `psycopg2`, `pyinputplus`, `names`, `gtts`, `tqdm` |

As of 2026-09-28 `wx`, `gspread`, and `google-auth*` were added, so `calculator_wx_python.py` and
both scrapers can now actually run. Still missing: everything for `login/login/`, the kivy app,
and the quantization tutorial.

### `kivy` is blocked on the Python version, not just uninstalled

Kivy 2.3.1 (Dec 2024) officially supports **Python 3.8–3.13**, and PyPI ships wheels only up to
`cp313`. The local interpreter is 3.14, so `pip install kivy` would fall back to building from
source. Upstream tracks this as [kivy#9225](https://github.com/kivy/kivy/issues/9225).

To run the kivy app you'd need a **separate 3.13 (or older) interpreter** rather than downgrading
the global one — most of the installed packages above are already 3.14-compatible and shouldn't be
disturbed. A venv on 3.13 is the clean route.

Do not assume an import resolves. If a script needs a missing package, say so rather than
"fixing" the import.

## No working lint / test / typecheck pipeline

`.trunk/` (ruff, black, isort, bandit, trivy) existed but was **deleted in June 2024** and is now
gitignored. The root `isort.cfg` is a leftover. `.mypy_cache/` is still on disk but `mypy` is not
installed, and `black`, `ruff`, `isort`, and `pytest` are absent too.

- There is no command to run for `lint`, `typecheck`, or `test`. Do not claim one exists.
- Verification is manual: run the script and look at stdout. A stale import or typo will not be
  caught for you.

## Never `pytest` this repo

There is no test suite, and files named `*_test.py` are ad-hoc scripts, not pytest tests.
`postgres_test.py:21` calls `connect_postgres()` at import time and needs a live PostgreSQL on
`localhost:5432` (db `postgres`, user `postgres`, password `password`, table `tweets`) — importing
it will fail or hang. Same pattern in `cell_test.py`, `dis_module_test.py`, `turing_machine_test.py`,
`wx_python_test.py`, `AVX2_and_FMA_test.py`, `for_test.py`, `speed_test.py`, `time_test.py`.

## 46 of 63 root scripts execute at import time

Only 17 use `if __name__ == "__main__":`. The rest run top-level code on import. So:

- Never `import` a repo module to test or inspect it. That runs the whole script (GUI windows,
  network calls, blocking `input()`, timing loops).
- Don't "tidy up" by adding main guards to unrelated scripts. New work should use `main()` + a
  guard, matching the newer files.

## Run from the repo root

Scripts resolve data files by bare relative path, so cwd matters:

- `game_dev_web_scraper.py:162` → `pd.read_csv("companies.csv")` (data file at repo root)
- `game_dev_web_scraper.py:31,32` / `web_scraping.py:20` → `token.pickle`, `creds.json` (written into cwd)

Three subprojects need cwd to be **their own directory**, not the repo root:

- `login/login/AdaSuperComputer_DEFAULT_TERMINAL_01.py` — ~30 hardcoded `os.system("start .\Assets\*.wav")`
  calls, plus `start SystemName01.mp3` with no directory. Run it from `login/login/` or the audio
  silently fails. `Assets/` (101 MB, 21 files) is committed and required at runtime.
  `SystemName01.mp3` and `PercentageT2S-01.mp3` are *generated* by `gTTS` at runtime (lines 336, 865),
  not read — their committed copies are just seeds.
- `mobile_app/main.py` — hardcodes `"Textures\\...jpg"` with a **backslash**, Windows-only, cwd-relative.
  Run from `mobile_app/`. Needs `kivy`, which is **not installable on the local Python 3.14** (see below),
  and it is *not* in `requirements.txt`.
- `quantization_tutorial/quantization_with_resnet18.py` — reads `quantization_tutorial/data/hymenoptera_data`
  (committed, 398 images: 124/121 train ants/bees, 70/83 val), but run it from the **repo root**.
  Needs `torch`/`torchvision`/`matplotlib` (not installed) and downloads ResNet18 weights on first run.
  A modified copy of the PyTorch quantized transfer learning tutorial.

## `.gitignore` hides all JSON, not just credentials

Line 1 is `*.json` (bare pattern → matches at any depth). This is deliberate for `creds.json` /
OAuth client secrets, but it also silently hides any new JSON data file. To add one:

```
git add -f path/to/file.json
```

Also ignored: `*.spec` and `*.manifest` (PyInstaller) — **no `.spec` is committed anywhere**, so
builds are ad-hoc one-liners and cannot be reproduced from the repo.

## Compiled binaries are committed

`pong.exe` (8.5 MB), `pong_korge_port.exe` (9.5 MB), `custom_square_root.exe` (24.8 MB),
`DMA_cell.exe` (24.8 MB), `mtrr.exe` (7 MB), plus `dis_module_test.exe`, `ifstatement.exe`,
`potatos.exe`. Git history shows a recurring "recompile <name>" commit pattern.

- Don't delete or `git rm` these — they are intentional deliverables.
- Don't add new ones unless asked. Binary churn is what the last several commits are mostly made of.
- No `.pdb` files are committed any more; `DMA_cell.pdb` and `mtrr.pdb` were removed in `67bf7dd`.
- A stray `python37.dll` was committed at the root in 2021 ("files that got incorrectly ignored").
  It was unreferenced by any source and has been removed. If it reappears, it's the same mistake.

## Conventions for new scripts

The newer files (post-2024) are the style to match; older ones vary wildly.

- `snake_case.py` filenames. A legacy CamelCase set exists (`DMA_cell.py`, `IfStatement.py`,
  `LinearSearch.py`, `HelloWorld.py`, `MultTable.py`) — don't copy it. Note the `.exe` counterpart
  doesn't always match case (`IfStatement.py` → `ifstatement.exe`).
- Full type hints, wrapping at 88 columns (black default). No `from __future__ import annotations`.
- Config and state bags are `@dataclass` (often named `Constants` or `Config`):
  `game_dev_web_scraper.py:17`, `web_scraping.py`. Classes get `__slots__`
  (`pong_korge_port.py`).
- Use `secrets.choice` for randomness in games, not `random.choice`
  (`hangman2.py`, `rock_paper_scissors.py`, `ohm_enc.py`).
- A `main()` function plus `if __name__ == "__main__": main()`.

## Secrets

Never commit real credentials. `creds.json` and `token.pickle` are gitignored, which is correct.
`DiscordBot.py:19` ships a literal placeholder token string — keep it a placeholder.

## `README.md` is stale — trust the file tree instead

It claims "a calculator using kivy as GUI". The kivy app is `mobile_app/` (`main.py`, a
`Textures/` asset) and is now restored, so the README is *accidentally* right again about the GUI
toolkit. It was deleted 2025-01-25 in `84702ee` and recovered from `84702ee^`; the README itself
has not been edited since 2024-05-13.

There are two calculators, not one. `calculator_wx_python.py` was **added 2024-11-29** (`71e1aba`,
"add another calculator but use wxpython instead"), so for two months the repo had both. Only `wx`
is installed now, so that one runs and the kivy one does not. Don't use the README to decide what
exists; use the file tree.

Corollary: the repo *did* have CI (Travis, scoped to `login/login/`) until that Jan 2025 cleanup;
`login/login/.travis.yml` is now restored too. "No CI" describes the current tree, not the history.
