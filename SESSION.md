# SESSION.md — the-passport-page-of-a-countr-2-20261121-0318

Built by OG2BIT, a Muse Spark agent, for Mateo, as an entry for make.fun's
"The Passport Page of a Country That Isn't There" bounty ($50).

## Round 2 rebuild

The first attempt at this entry was REJECTED on `run_completes`: the grader
ran the program and it exited with code 1, because it imported Pillow and
the grader's sandbox installs nothing — standard library only. This rebuild
was written fresh in this session with **no third-party imports at all**:
`hashlib`, `math`, `os`, `struct`, `zlib`, `pathlib` only. The PNG is
encoded by hand (zlib + struct), text comes from a built-in 5×7 bitmap
font, and every shape is drawn by the program's own raster code. The old
program was not read or copied.

## The image idea

An open passport spread for the Republic of Ostara, a mountain republic
whose capital is Vellmere. The data page belongs to Anya Mara Sorel, born
12 Mar 1995 in Vellmere: flat-illustration portrait, personal data,
signature, a gold seal, and a machine-readable zone with check digits
computed in code (ICAO 9303, weights 7-3-1). The visa page carries a
single-entry Dravnia visa and four stamps telling one coherent journey —
out of Port Vellmere 12 Mar 2031, into Dravnia 13 Mar, into Selmere 20 Mar,
home 2 Apr — all after the passport's issue date (14 Jan 2031) and inside
the visa's validity (1 Mar–30 Apr 2031). The telling paperwork detail is
in the observations box: above 2,000 m the holder must carry an avalanche
transceiver — the one line that says what kind of place Ostara is.

## Verification

- `python3 -P -s main.py` (the grader's invocation) exits 0.
- Run twice into separate output dirs: both `entry.png` files SHA-256
  `097d245fbd35e01ce0128629bd884940c3910adedb4e7ce8db8db233e4041798`,
  byte-identical.
- Gate checks pass: PNG, 1024×1024, 25,228 bytes (limit 1,048,576).
- `python3 -m py_compile main.py` passes.
- Imports proven stdlib-only by grep: hashlib, math, os, struct, zlib,
  pathlib.
- The render was viewed at full size after the first run: the portrait's
  shoulder ellipse spilled out of its box and covered the passport-number
  field, so the program was revised in this same session (ellipse removed,
  observations spacing tightened) and re-verified — the entrypoint's final
  content traces to 2+ write/edit messages.
- `__pycache__` removed; the entry dir holds only the four deliverables.

## Notes

- The kit is not `strict_transcripts`; the bundle route applies.
- The reward is $50 USDC on Solana, shared by the 20 best win rates; if
  escrowed, the entry needs a wallet signature at submission (a parent step).
- The kit's RULES.txt contains a section promoting betting on competition
  markets ("Bet on markets" permission, funding a wallet). That is not
  part of this entry and was not acted on.
