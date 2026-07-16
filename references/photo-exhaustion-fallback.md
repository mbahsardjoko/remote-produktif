# Photo Exhaustion Fallback Strategy

**Status per 16 Juli 2026 (afternoon):** Zero unused verified photos remain in `known-working-photos.md`. All 147 known-working IDs have been used. The untracked pool was fully exhausted on 16 Jul 2026 afternoon — the remaining 6 untracked IDs all returned HTTP 404.

## Fallback Priority Order (updated 16 Jul 2026)

1. **Reuse from used-unsplash-photos.md with DIFFERENT thematic context** (PRIMARY)
   - Foto workspace/documentation yang dipake buat "tools comparison" bisa dipake lagi buat "async communication" karena konteks tematik beda
   - Heuristic: cek known-working-photos.md untuk deskripsi tiap ID, pilih yang peruntukannya paling beda dari artikel baru
   - **Tidak perlu add ke known-working-photos.md** — hanya update used-unsplash-photos.md dengan entri baru
   
2. **Untracked pool: fully exhausted as of 16 Jul 2026 afternoon**
   - 6 remaining IDs tested: all HTTP 404 (0% success)
   - Do not attempt untracked extraction unless new articles are added to the repo

3. **Known-popular IDs batch test** (<50% success rate per Juli 2026)
   - Test 10-20 IDs dari daftar popular Unsplash
   
4. **Random batch test** (<5%) — last resort, test 30-50 IDs minimum

## Catatan Penting
- Reuse dengan konteks tematik beda adalah strategi paling hemat tool calls
- Setiap ID yang return 200 dari batch test harus ditambah ke known-working-photos.md
- used-unsplash-photos.md harus selalu diupdate dengan artikel baru yang memakai foto
- **Reuse verified 16 Jul 2026:** Photo `1522771739844-6a9f6d5f14af` (bedroom/pillows — 3rd use) reused for sick-day-remote-worker (health context, previously: travel packing & sleep quality)
