# Session Learnings — 10 Agu 2026: kerja-malam-remote-worker

## Gap Discovery
- **kerja-malam-remote-worker** (Kesehatan & Energi) — genuine gap:
  - "shift malam" / "kerja malam" / "night shift" → 0 dedicated article (hits cuma mentions: night-shift = mode HP, begadang = avoid-mentions di artikel lain)
  - Adjacent-article H2 check PASSED: `night-routine-remote` (winding down BEFORE sleep), `kualitas-tidur-remote-worker` (sleep hygiene daytime workers), `chronotype-remote` (identify body clock — complementary, NOT overlapping), `perbedaan-zona-waktu-remote` (team coordination, not individual night-shift lifestyle). None cover the person who ACTIVELY works at night (US/EU clients, night owl).
- Site sudah sangat jenuh (500+ artikel). Hampir semua cluster 0-match ternyata false-gap (kue, renang, seni, journaling, pensiun, psikolog, vitamin, berkebun, hewan, dll semua ada).

## Photo
- `1531297484001-80022131f5a1` — FREE (never used in repo!) + HTTP 200 di 3 ukuran. Verified dark/night via avg-brightness check (PIL: brightness 18/255 = malam) — teknik baru: download w=200, convert grayscale, hitung mean brightness buat konfirmasi tema gelap tanpa vision tool.
- Famous `1517842645767-c639042777db` (man-at-desk) ternyata brightness 167 = TIDAK gelap — jangan asumsi dari memori.

## Gap Scan Efficiency
- 3 execute_code rounds cukup buat nolak ~60 keyword clusters (hampir semuanya covered). Pola: check slug → body-scan context window → adjacent H2 check untuk final gap.

## Template
- `kesehatan-rambut-remote-worker.html` = template bersih (multi-line head, GA quoted, Style A). 15.1KB artikel sukses via write_file skeleton (4.4KB) + 4 patch calls (~3-4KB per patch) — zero STREAM timeout. Marker chain `<!--BODY-->` → `<!--BODY2-->` → `<!--BODY3-->` → `<!--BODY4-->` works.
- Pre-commit all green first pass: 2 Lo, 0 CJK, desc 117 4-lokasi, 4 backlinks (2 body chronotype/kualitas-tidur + 2 related perbedaan-zona-waktu/shutdown-ritual), GA quoted, OG lengkap, tag balance clean.