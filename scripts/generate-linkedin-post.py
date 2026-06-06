#!/usr/bin/env python3
"""
Generate LinkedIn teaser post for a remoteproduktif.online article.

Usage:
    python3 generate-linkedin-post.py <slug>
    
    Reads article info from ../artikel.json and generates a LinkedIn-optimized
    teaser post saved to ../linkedin-posts/{slug}-linkedin.txt
"""

import json, os, re, sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find_article(slug):
    with open(os.path.join(REPO, 'artikel.json')) as f:
        data = json.load(f)
    for a in data:
        if a['slug'] == slug:
            return a
    return None

def generate_post(article):
    title = article['title']
    slug = article['slug']
    tag = article['tag']
    url = f"https://remoteproduktif.online/{slug}"
    
    hooks = {
        "Karir": "Lo pernah ngerasa stuck di tempat kerja, gak ada jenjang karir yang jelas?",
        "Karir & Pengembangan": "Salah satu pertanyaan paling sering gue denger dari remote worker: gimana caranya naik level tanpa harus masuk kantor?",
        "Tools & Review": "Tools yang lo pake tiap hari bisa nentuin produktivitas lo — atau malah jadi sumber stres.",
        "Tools & Setup": "Masalah teknis adalah musuh terbesar produktivitas remote. Tapi jarang yang sadar.",
        "Komunikasi & Kolaborasi": "Komunikasi yang efektif itu bukan soal sering chat. Tapi soal gimana lo nyampein maksud dengan jelas.",
        "Kesehatan Mental": "Kerja remote itu enak. Tapi ada harga yang harus dibayar: kesehatan mental lo.",
        "Manajemen Tim": "Manage tim remote beda banget sama offline. Yang works di kantor belum tentu works di rumah.",
        "Fokus & Produktivitas": "Fokus di rumah itu susah. Bukan karena lo males — tapi karena lingkungan lo gak dirancang buat kerja.",
        "Work-Life Balance": "Batas antara kerja dan hidup pribadi makin tipis. Lo perlu strategi buat jaga keseimbangan.",
        "Kolaborasi Tim": "Tim remote yang solid bukan karena sering ngumpul. Tapi karena punya sistem komunikasi yang jelas.",
        "Komunikasi & Kolaborasi": "Meeting itu penting. Tapi meeting yang gak efektif? Musuh produktivitas nomor satu.",
    }
    
    ctas = {
        "Karir": "Selengkapnya di remoteproduktif.online — link di komentar 👇",
        "Karir & Pengembangan": "Selengkapnya di artikel gue — link di komentar 🔥",
        "Tools & Review": "Baca selengkapnya di remoteproduktif.online — link di komentar 💻",
        "Tools & Setup": "Lengkapnya ada di remoteproduktif.online — link di komentar 🔧",
        "Komunikasi & Kolaborasi": "Selengkapnya — link di komentar 👇",
        "Kesehatan Mental": "Lengkapnya di remoteproduktif.online — link di komentar 🧠",
        "Manajemen Tim": "Baca selengkapnya — link di komentar 🔥",
        "Fokus & Produktivitas": "Selengkapnya di remoteproduktif.online — link di komentar 🚀",
        "Work-Life Balance": "Lengkapnya — link di komentar 💡",
        "Kolaborasi Tim": "Selengkapnya di remoteproduktif.online — link di komentar 🤝",
        "Komunikasi & Kolaborasi": "Baca selengkapnya — link di komentar 💬",
    }
    
    hook = hooks.get(tag, "Pernah gak lo ngalamin ini?")
    cta = ctas.get(tag, "Selengkapnya di remoteproduktif.online — link di komentar 👇")
    
    # Clean title - remove subtitle after " — " or " – " (NOT hyphen within words)
    # Indonesian blog titles use: "Title — Subtitle" or "Title – Subtitle"
    if ' — ' in title:
        main_title = title.split(' — ')[0].strip()
    elif ' – ' in title:
        main_title = title.split(' – ')[0].strip()
    else:
        main_title = title.strip()
    # Generate a more engaging middle paragraph
    article_url_clean = f"https://remoteproduktif.online/{slug}"
    
    post = f"""{hook}

Gue baru nulis soal **{main_title}** di remoteproduktif.online. Dari riset dan pengalaman, ada beberapa hal yang jarang dibahas orang — termasuk trik-trik yang langsung gue terapin sendiri.

Kalau lo kerja remote dan ngerasa stuck di salah satu masalah ini, mungkin artikel ini bisa bantu. Semua praktis, langsung bisa dicoba.

{cta}

#RemoteWorker #Produktivitas #RemoteIndonesia #{tag.replace(' & ', '')}"""
    
    return post.strip()

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    if not slug:
        # Get latest article
        with open(os.path.join(REPO, 'artikel.json')) as f:
            data = json.load(f)
        slug = data[0]['slug']
    
    article = find_article(slug)
    if not article:
        print(f"❌ Article '{slug}' not found", file=sys.stderr)
        sys.exit(1)
    
    post = generate_post(article)
    
    outdir = os.path.join(REPO, 'linkedin-posts')
    os.makedirs(outdir, exist_ok=True)
    
    outpath = os.path.join(outdir, f'{slug}-linkedin.txt')
    with open(outpath, 'w') as f:
        f.write(post + '\n')
    
    print(f"✅ LinkedIn post saved: {outpath}")
    print(f"   Article: {article['title']}")
    print(f"   URL: https://remoteproduktif.online/{slug}")
    print()
    print(post)

if __name__ == '__main__':
    main()
