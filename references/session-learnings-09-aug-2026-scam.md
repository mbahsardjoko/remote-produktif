# Session Learnings — 9 Agustus 2026: menghindari-scam-remote-worker

Artikel: **menghindari-scam-remote-worker** (tag "Karir Remote") — gap: modus penipuan kerja (lowongan palsu, klien nakal, pembayaran tipu-tipu, phishing).

## Gap discovery
- Keyword scan: 'scam', 'penipuan', 'fraud' → 0 slug/title match. Body-scan: 0 hit untuk 'scam'/'penipuan'/'fraud' (aman).
- ⚠️ 'penipu' body hits = 6, TAPI 100% figuratif ("perasaan kayak lo penipu" = impostor syndrome, "politik bukan jadi penipu"). Bukan coverage modus penipuan.
- Adjacent check: keamanan-digital (phishing teknis), password-security (2FA) — beda angle dari job/client scam. Gap AMAN.
- Related backlinks: menghadapi-ghosting, keamanan-digital, invoice-profesional, freelance-marketplace — 4 first-pass.

## Photo selection
- Reuse `1560472354-b33ff0c44a43` (dua profesional negosiasi / meeting room) — sesuai metafora verifikasi sebelum deal. HTTP 200 di w=800/1200/600.
- ⚠️ Kandidat awal `1589829085413-56de94518c73` (tanda tangan kontrak) ternyata 404 — foto verified lama bisa expire. Selalu curl test 3 ukuran.

## Zero-issue second pass fix
- First pass: 5 backlinks (slug keamanan-digital di body section 5 + related = duplikat dihitung 2). Fix: remove body duplicate jadi 4.
- Missing `</div>` buat closing article container saat replace body dari template — tambah `</div>\n    </article>` sebelum `</main>`.
- Template swap pakai str_replace/read-template + regex head-swaps — lebih aman dari menulis full HTML manual (em-dash & f-string escaped).
- Proactive "kamu" = 2 "Lo" total (opening + CTA), zero reduce-lo.
- Desc 122 chars in 4 locations. GA quoted. OG image w=1200. Sitemap 490 URLs.