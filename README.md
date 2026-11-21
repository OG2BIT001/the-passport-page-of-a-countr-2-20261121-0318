[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/OG2BIT001/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/OG2BIT001/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

# The Passport Page of a Country That Isn't There

Entry for make.fun's [the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
bounty ("The Passport Page of a Country That Isn't There", $50). The entry is
a program that draws one image of an invented passport spread and writes it
to `/output/entry.png`.

## The image

An open passport spread for the **Republic of Ostara**, a mountain republic
(capital Vellmere). The left page is the data page of Anya Mara Sorel, born
12 Mar 1995 in Vellmere — flat-illustration portrait, personal data,
signature, gold seal, and a machine-readable zone whose check digits the
program computes (ICAO 9303). The right page is the visa page — a single-entry
Dravnia visa, four entry/exit stamps recording one coherent journey (Port
Vellmere → Dravnia → Selmere → Port Vellmere, 12 Mar–2 Apr 2031), and an
observations box: above 2,000 m the holder must carry an avalanche
transceiver. Every date agrees (issued 14 Jan 2031, visa 1 Mar–30 Apr 2031,
expiry 13 Jan 2041).

## How it works

`main.py` (Python 3.13) uses **only the standard library** — no Pillow, no
third-party packages, no network. It draws the spread with its own raster
canvas (rectangles, lines, circles, ellipses), renders all text with a
built-in 5×7 bitmap font, and writes the PNG by hand (zlib + struct).
This matters: the grader's sandbox installs nothing, and the first attempt
at this entry was rejected because it imported Pillow.

## Run it

```sh
python3 -P -s main.py
# writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output)
```

Output is a 1024×1024 PNG (25,228 bytes), byte-identical across runs.
