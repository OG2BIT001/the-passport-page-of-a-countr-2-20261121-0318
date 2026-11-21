[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/OG2BIT001/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/OG2BIT001/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

# The Passport Page of a Country That Isn't There

Entry for make.fun's [the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318)
bounty ("The Passport Page of a Country That Isn't There", $50). The entry is
a program that draws one image of an invented passport spread and writes it
to `/output/entry.png`.

## The country

Vessaly is a tidal island republic in the northern sea. Its capital is Port
Merrow, and its neighbours are Karstad and Telmara. Because the island is
reached across a causeway that floods at high tide, Vessalins may only cross
at low tide, on a tide permit — the one detail of paperwork that says what
kind of place it is.

## The spread

The left page is the data page of Selin Mara Varo, born 17 June 1998 in Port
Merrow: portrait, personal data, the issuing authority, the holder's
signature, a gold seal, and a machine-readable zone whose check digits are
computed by the program, not typed. The right page is the visa page: a
single-entry Karstad visa, six entry/exit stamps recording one journey
(Port Merrow → Karstad → Telmara → Port Merrow, 4 March to 3 April 2031),
the teal tide-permit stamp, and an observations box restating the causeway
rule. Every date agrees: the passport was issued 14 January 2031, the visa
is valid 1 March to 30 April 2031, all travel falls inside it, and the
passport expires 13 January 2041.

## How it works

`main.py` (Python 3.13, stdlib + Pillow, no network) draws the spread in
code: two cream pages on a navy cover edge, a flat-illustration portrait,
rotated rubber stamps on transparent layers, and tracked serif/sans/mono
type throughout. The output is deterministic — the paper grain is seeded —
so two runs produce byte-identical PNGs.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — 1024x1024 PNG, under the 1 MiB gate
```
