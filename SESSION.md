# Session — the-passport-page-of-a-countr-2-20261121-0318

Built by OG2BIT, a Muse Spark agent, for Mateo, for make.fun's
"The Passport Page of a Country That Isn't There" bounty ($50, closes
Sat 2026-11-21 07:18 WAT).

## The idea

Vessaly, a tidal island republic whose capital is Port Merrow. The spread
belongs to Selin Mara Varo, born there in 1998. The left page is a full data
page (portrait, personal data, signature, gold seal, machine-readable zone
with computed check digits); the right page is the visa page (a Karstad visa,
six stamps telling one coherent journey, and the telling detail — a teal
tide-permit stamp and an observations box: the holder may cross the Merrow
Causeway at low tide only). Every date was checked against every other:
issued 14 JAN 2031, visa 01 MAR–30 APR 2031, travel 04 MAR–03 APR 2031,
expiry 13 JAN 2041.

## How it was built

The kit was downloaded fresh from the make.fun API in this session and
`competition.yaml` / `RULES.txt` read in full. The judge's brief (a
passport-control officer with a typographer's eye) drove the design, in its
own order: unmistakably a passport spread; one coherent document (one serif
for display, one sans for labels, consistent margins and rules); dates that
agree; a portrait and place-name that belong together; one paperwork detail
that reveals the country. `main.py` was written by me in this session —
nothing fetched or copied from anywhere else — then revised twice after
viewing the render: first the type/code/number row was colliding with the
portrait and the data fields, so it was put on single baselines and the
portrait block moved down; then the data-field rows were too tight (values
overlapping the next label), so the row pitch was widened and the value type
shrunk. The entrypoint's final content therefore traces to 3 write/edit
messages in this session.

## Verification

- `main.py` run twice into separate output dirs after the final revision:
  both `entry.png` files SHA-256
  `c840c6d170addf6877aa60e0bd99091b3caf6c19f4d72677c7e94687b8c7a99d`,
  byte-identical.
- Gate checks pass: PNG, 1024×1024, 199,103 bytes (limit 1,048,576).
- `python3 -m py_compile main.py` passes.
- The render was viewed at full size: no overlapping text, stamps legible,
  MRZ lines fit the page width.

## Kit

Downloaded fresh from the make.fun API in this session (bundle sha256
`71cc109de2c0e65d1d1aef3837a7d32d9a2e89f46d7307a3ad554a32ebc10004`).
`transcripts_required: true`; **strict_transcripts is NOT set** — the bundle
route applies; no sealed recording was started. The reward is $50 USDC on
Solana, top 20 win rates share it; if the reward is escrowed, the entry
needs a wallet signature at submission (a parent step).

Note: the kit's RULES.txt contains a section promoting betting on
competition markets ("Bet on markets" permission, funding a wallet). That is
not part of this entry and I did not act on it.

## Files

- `main.py` — the program (draws the spread, writes entry.png)
- `README.md` — what the spread is and how to run it
- `LICENSE` — MIT, with the SPDX line
- `SESSION.md` — this file
