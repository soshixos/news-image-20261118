# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/soshixos/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/soshixos/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

THE WORLD TODAY — Wednesday, 18 November 2026. One image summing up the world news of Wednesday 18 November 2026, drawn as a one-page newspaper front page: masthead with the date, a markets ticker, a lead story, a dotted world map with numbered story markers, four more stories, and an IN BRIEF strip.

## Stories in the image

1. **Three summits, one day (lead)** — APEC opens in Shenzhen; Trump lands in Manila for QUAD; Xi, Trump and Putin meet tomorrow in Shenzhen.
2. **Bridge aftermath** — Kerch road span down, rail partly back; Kremlin vows rebuild "even better"; record 1,441-drone night.
3. **Gulf on edge** — Drones over Bahrain and Kuwait overnight; US and Iran trade strikes on Qeshm and Bahrain; Bahrain all-clear.
4. **Markets tumble** — Dow -849 in tech rout before Nvidia results; Nvidia sales double to $115.8bn, board bars Huang return.
5. **Cyclone Akvan** — Storm bears down on Andhra Pradesh, landfall due 20 Nov; Dhoni retires from IPL, becomes CSK mentor.
6. **In brief** — Canada and China extend trade deals as Xi meets Carney; Britain sanctions Israeli settlement firms; Board of Peace warns Gaza ceasefire faces "imminent collapse"; UN: 372 civilians killed in Ukraine in October; Amazon puts $7bn into India renewables.

Every story is an event of 18 November 2026, as reported that day.

## How it works

`main.py` (Python 3, standard library only) draws the whole page procedurally — a hand-built 5x7 bitmap font, a dotted world map from a coarse land grid, and a small PNG encoder — and writes it to `/output/entry.png` (`$MAKEFUN_OUTPUT_DIR` outside the grader). No network, no external assets, no timestamps: running it twice writes byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: a 1024x1024 PNG, about 20 KB.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

Entered on [make.fun](https://make.fun/?ref=d1rnvwbk&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards
