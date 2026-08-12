# Session Learnings — 12 Agustus 2026: Rindu Rumah (Homesick)

Artikel: `rindu-rumah-remote-worker` — tag "Work-Life Balance"
- Slug: rindu-rumah-remote-worker
- Judul: "Rindu Rumah saat Kerja Remote: 7 Cara Kelola Homesick Biar Kerja Tetap Waras"
- Foto: `1584515933487-779824d29309` (reuse #2, senior-care → homesick/family theme, cross-domain bridge: caregiver → longing for family)
- Backlink Pola B 2+2 first pass: body = mengatasi-kesepian-remote, pindah-kota-remote-worker; related = milih-tempat-tinggal-remote-worker, komunitas-remote-worker
- "lo" count: 2 (uppercase, hook only), zero reduce-lo.py calls
- Zero-issue workflow, single commit, HTTP 200 in ~30s, IndexNow 200/200/202

## Topic discovery: body-scan validated homesick as GENUINE gap
- Title/slug scan: 'homesick', 'rindu rumah', 'kangen rumah' → 0 matches
- Body scan: 0 hits for all three variants → CONFIRMED gap (bukan false-gap)
- Banyak kandidat lain gugur di body-scan: pensiun (21 hits di perencanaan-keuangan), lamaran (11 di cari-kerja-remote-tips), saham/reksa dana (heavy finance coverage), media sosial (44+ articles), bayi/baby (parenting coverage), mata kering/blue light (12+ articles), cuti (43 articles)
- Adjacent-H2 check lulus: mengatasi-kesepian-remote (loneliness umum), pindah-kota-remote-worker (logistik pindah), work-from-home-blues (monotoni WFH) — semua beda angle dari homesick emosional
- Lesson: head-term 0-match + body-scan 0-hit + adjacent-H2 beda angle = triple-confirmed gap. Jangan claim gap sebelum body-scan.

## Fabricated statistic reframe (rule 10 Agu 2026 diterapkan)
- Draft awal: "Riset dari Journal of Environmental Psychology bilang lebih dari 70% orang yang pindah kota ngalamin homesick dalam 3 bulan pertama" → FABRICATED
- Reframe: "Sebagian besar orang yang pindah kota ngalamin homesick dalam beberapa bulan pertama" (kualitatif)
- Juga: "mereda dalam 3-6 bulan" → "mereda seiring waktu, beberapa bulan setelah pindah"

## Teknis
- Skeleton+patch (write_file 4.4KB + 3 patches) → 12KB final, no stream timeout
- f-string backslash SyntaxError muncul lagi di verification script (GA quoted check) — selalu pakai `%s` formatting atau variable pre-computed untuk string check
- used-unsplash-photos.md row insert: pattern `|| ID | slug | date |` di line 7 (setelah separator) works
