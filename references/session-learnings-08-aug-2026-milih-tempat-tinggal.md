# Session Learnings — 8 Agustus 2026: milih-tempat-tinggal-remote-worker

## Summary
Cron session: 2 orphan recoveries + 1 new article (milih-tempat-tinggal-remote-worker), single commit.

## Key Learnings

### 1. Orphan recovery protocol worked cleanly this session
- `merayakan-progres-kecil-remote-worker.html`: **committed orphan** (commit 429e0b7, 15 Juli 2026) — file already in HEAD, just missing artikel.json entry. Working tree had a **modified version** (lo → kamu improvements in opening). Recovery: verify HTML, update date, insert entry.
- `cek-kesehatan-rutin-remote-worker.html`: **untracked new orphan** — never committed. Full pre-commit verification passed (4 backlinks, 0 CJK, 0 lo, GA quoted).
- Both had **correct canonical, GA, OG** already — just needed re-registration + date update.
- ⚠️ JSON descs I wrote from scratch were **>150 chars** (153, 154) while the HTML descs were fine (107, 114). Lesson: **README the JSON desc from the HTML `<meta name="description">`**, don't re-author it.

### 2. Tag selection: match sibling articles
- cek-kesehatan-rutin: all other physical health articles use **"Kesehatan & Energi"** (not "Kesehatan Mental"). Use the sibling-article tag, not a guess.
- merayakan-progres: motivation/progress → chose **"Produktivitas & Mental"**; alternates: Kesehatan Mental, Produktivitas.

### 3. Gap discovery this session
- Housing/living-quarters cluster (kost, apartemen, kontrakan, sewa rumah, milih tempat) = **0 in titles/slugs**, only scattered body mentions (~1 per article, never an article about it).
- Neighbor articles checked: pindah-kota-remote-worker (relocation PROCESS — different angle), coworking-space-vs-heja-rumah (workspace venue, not residence), home-studio (room inside home). All distinct → genuine gap.
- Rich ecosystem for backlinks: internet-stabil, pindah-kota, anggaran-keuangan, coworking-space, keuangan-remote, wfh-setup — 14+ candidates ✓.
- Note: "powder nap"/"kafein"/"kopi" topics are already saturated (strategi-kopi, manfaat-power-nap, power-nap-routine, strategi-teh) — don't write in that area.

### 4. Photo reuse
- Used `1518241353330-0f7941c2d9b5` (calm home interior) — **3rd use** (prior: boundaries-sehat-kerja-remote, work-life-balance-digital-nomad). Batch-tested 200 at w=800/1200/600.
- All 5 candidates tested worked (1518241353330, 1470071459604, 1507925921958, 1528715471579, 1543269865).
- used-unsplash-photos.md file is still near-empty (~9 rows) — per 7-Agu lesson, authoritative used-set comes from HTML scan, not from the file.

### 5. Article stats (Pola B)
- 4 backlinks first pass (2 body: internet-stabil, anggaran-keuangan; 2 related: pindah-kota, coworking).
- "lo" count: 1 (uppercase in opening hook). Checked: 0 CJK, 0 markdown, tag-balance OK, GA `gtag('config', 'G-JEM1XWBLHE')` quoted.
- Desc: 130 chars in all 4 locations (meta/og/twiter/artikel.json).
- Wrote via head-skeleton + 2 execute_code body chunks + fix pass (3 textual cleanups), total 10.8KB.