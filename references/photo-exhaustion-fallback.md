# Photo Exhaustion Fallback Strategy

**Status per 13 Juli 2026:** Zero unused verified photos remain in `known-working-photos.md`. All 145 known-working IDs have been used.

## Fallback Priority Order (updated 13 Jul 2026)

1. **Reuse from used-unsplash-photos.md with DIFFERENT thematic context** (PRIMARY)
   - Foto workspace/documentation yang dipake buat "tools comparison" bisa dipake lagi buat "async communication" karena konteks tematik beda
   - Heuristic: cek known-working-photos.md untuk deskripsi tiap ID, pilih yang peruntukannya paling beda dari artikel baru
   - **Tidak perlu add ke known-working-photos.md** — hanya update used-unsplash-photos.md dengan entri baru
   
2. **Batch test untracked inline photos from HTML files** (~3 tersisa per Juli 2026)
   - Ekstrak dari SEMUA file .html yang belum dipake
   - Test dengan curl, tambah yang 200 ke known-working-photos.md
   
3. **Known-popular IDs batch test** (<50% success rate per Juli 2026)
   - Test 10-20 IDs dari daftar popular Unsplash
   
4. **Random batch test** (<5%) — last resort, test 30-50 IDs minimum

## Catatan Penting
- Reuse dengan konteks tematik beda adalah strategi paling hemat tool calls
- Setiap ID yang return 200 dari batch test harus ditambah ke known-working-photos.md
- used-unsplash-photos.md harus selalu diupdate dengan artikel baru yang memakai foto
