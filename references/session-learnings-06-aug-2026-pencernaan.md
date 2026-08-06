# Session Learnings — 6 Agustus 2026: kesehatan-pencernaan-remote-worker

## Zero-issue workflow (clean pass)
- Topic gap: **Pencernaan (digestive health)** — confirmed genuine zero-match gap via body-scan.
  - ⚠️ "maag" 0-match in titles/slugs, BUT substring false-positive in body: `maag` matched `magang` (468 files). This is the illusion-reverse of body-coverage false-gap: a head term that LOOKS matched but is actually a **substring false-positive** (magang-remote-fresh-graduate). Always verify body scan context, not just count.
  - Body-part completion cluster now: gigi, kulit, telinga, leher, pergelangan-tangan, mata, jantung — pencernaan was the missing piece. This is a thematic cluster that keeps yielding clean gaps.
- Backlinks: Pola B 4 slugs first pass (2 body sarapan-sehat + hidrasi, 2 related camilan-sehat + jalan-kaki). 4/4 verified.
- Proactive "kamu" → only **1 "Lo"** uppercase in opening hook. Zero reduce-lo.py.
- Photo: reuse `1556910103-1c02745aae4d` (kitchen/memasak) — 2nd use, cross-domain food-adjacent (memasak-remote-worker → pencernaan). HTTP 200 at w600/w800/w1200.

## Fixed a repo data bug: duplicate slug self-love-remote-worker
- `artikel.json` had TWO entries for `self-love-remote-worker`: one dated 6 Agustus 2026 (tag "Work-Life Balance", current title/desc) and one stale dated 26 Juli 2026 (tag "Kesehatan Mental", older title/desc).
- Root cause: a prior session's recovery/commit path likely double-inserted. The HTML `<title>`/`<div class="meta">` showed the 6 Agustus entry is the live correct one.
- **Fix:** removed the stale 26 Juli entry via Python filter (kept the entry matching the HTML file), re-validated no remaining duplicates, bundled in the article publish commit.

## Also present (3 Agu 2026) — duplicate-slug detection reminder
Detect before publish with `Counter(a['slug'] for a in artikel.json)`. This one slipped through prior sessions; scan for it during Step 3.