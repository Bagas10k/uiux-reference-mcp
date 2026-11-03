#!/usr/bin/env python3
"""
MCP Server: uiux-reference (Pustaka Referensi Desain Web & UI/UX Board)
Author: Bagas Cihuy & Hermes Agent
Integrasi: Pustaka /home/ubuntu/referensi-desain/ dan Aturan AGOTIMA UI/UX
"""

import os
import json
import asyncio
from typing import List, Optional
from mcp.server.mcpserver import MCPServer

KATALOG_PATH = "/home/ubuntu/referensi-desain/katalog.json"
BASE_DIR = "/home/ubuntu/referensi-desain"

server = MCPServer("uiux-reference")

def _load_catalog():
    if not os.path.exists(KATALOG_PATH):
        return []
    with open(KATALOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("items", [])

def _get_item_file_path(item):
    rel = item.get("rel_path") or item.get("file_name") or ""
    return os.path.join(BASE_DIR, rel)

def _get_item_size(item):
    kb = item.get("size_kb")
    if kb:
        if kb >= 1024:
            return f"{kb/1024:.2f} MB"
        return f"{kb:.1f} KB"
    return item.get("size", "N/A")

@server.tool()
def uiux_search(query: str = "", category: str = "all", limit: int = 8) -> str:
    """
    Cari aset referensi desain web di pustaka 100 aset server berdasarkan kata kunci atau kategori.
    Kategori: 'all', '01-landing-pages-saas', '02-portofolio-agency', '03-dashboard-admin', '04-ecommerce-produk', 'prioritized', 'recommended'.
    """
    items = _load_catalog()
    if not items:
        return "Pangkalan data katalog referensi tidak ditemukan di server."

    results = items
    if category == "prioritized":
        results = [i for i in results if i.get("prioritized")]
    elif category == "recommended":
        results = [i for i in results if i.get("recommended")]
    elif category != "all":
        results = [i for i in results if category.lower() in i.get("category", "").lower()]

    if query.strip():
        q = query.lower().strip()
        matched = []
        for i in results:
            text_corpus = f"{i.get('id', '')} {i.get('title', '')} {i.get('category', '')} {i.get('format', '')} {i.get('recommendation_note', '')}".lower()
            if q in text_corpus:
                matched.append(i)
        results = matched

    results = results[:limit]
    if not results:
        return f"Tidak ada referensi desain yang cocok untuk query='{query}', category='{category}'."

    output_lines = [f"### Ditemukan {len(results)} Referensi Desain:"]
    for r in results:
        prio_tag = " [UTAMA/PIN]" if r.get("prioritized") else ""
        rec_tag = " [REKOMENDASI]" if r.get("recommended") else ""
        note = f" - Catatan: {r.get('recommendation_note')}" if r.get("recommendation_note") else ""
        abs_path = _get_item_file_path(r)
        size_str = _get_item_size(r)
        output_lines.append(
            f"- **[{r.get('id').upper()}] {r.get('title')}**{prio_tag}{rec_tag}\n"
            f"  Kategori: `{r.get('category')}` | Format: `{r.get('format', 'PNG')}` | Dimensi: `{r.get('dimensions', '-')}` ({size_str})\n"
            f"  Path Berkas: `{abs_path}`{note}"
        )
    return "\n".join(output_lines)

@server.tool()
def uiux_view(ref_id: str) -> str:
    """
    Lihat rincian lengkap satu berkas referensi desain berdasarkan ID (contoh: 'ref-012' atau 'ref-034').
    Mengembalikan path absolut berkas fisik di disk untuk analisis visual (vision_analyze).
    """
    items = _load_catalog()
    clean_id = ref_id.lower().strip()
    item = next((i for i in items if i.get("id", "").lower() == clean_id), None)
    if not item:
        return f"Referensi dengan ID '{ref_id}' tidak ditemukan di katalog."

    file_path = _get_item_file_path(item)
    exists = os.path.exists(file_path)
    size_str = _get_item_size(item)

    details = [
        f"### Detail Referensi: {item.get('title')}",
        f"- **ID**: `{item.get('id').upper()}`",
        f"- **Kategori**: `{item.get('category')}`",
        f"- **Format Berkas**: `{item.get('format', 'PNG')}`",
        f"- **Dimensi**: `{item.get('dimensions', 'N/A')}`",
        f"- **Ukuran Berkas**: `{size_str}`",
        f"- **Status Pin Prioritas**: `{'Ya' if item.get('prioritized') else 'Tidak'}`",
        f"- **Status Rekomendasi**: `{'Ya' if item.get('recommended') else 'Tidak'}`",
        f"- **Catatan Arsitektur**: `{item.get('recommendation_note') or 'Belum ada catatan'}`",
        f"- **Path Berkas Fisik**: `{file_path}` (Ada di Disk: {exists})",
        f"- **URL Pratinjau Publik**: `https://www.jajandigital.web.id/api/referensi-desain/{item.get('id')}/image`"
    ]
    return "\n".join(details)

@server.tool()
def uiux_reference_board(ref_ids: List[str]) -> str:
    """
    Buat Reference Board terstruktur membandingkan 4-8 ID referensi desain (sesuai Step 4 AGOTIMA).
    Membandingkan hirarki informasi, tata letak grid, model navigasi, dan kesesuaian pola.
    """
    items = _load_catalog()
    items_map = {i.get("id", "").lower(): i for i in items}
    
    selected = []
    for rid in ref_ids:
        cid = rid.lower().strip()
        if cid in items_map:
            selected.append(items_map[cid])

    if not selected:
        return "Tidak ada ID referensi yang valid dari daftar yang diberikan."

    lines = [
        f"# UI/UX REFERENCE BOARD ({len(selected)} Kandidat Terpilih)",
        "Dianalisis berdasarkan 10 Pilar Evaluasi Desain AGOTIMA:\n"
    ]

    for idx, s in enumerate(selected, 1):
        file_path = _get_item_file_path(s)
        size_str = _get_item_size(s)
        note_str = s.get('recommendation_note') or 'Pola antarmuka bersih & struktur komponen responsif.'
        lines.append(
            f"### {idx}. [{s.get('id').upper()}] {s.get('title')}\n"
            f"- **Kategori & Tipe**: `{s.get('category')}`\n"
            f"- **Path Gambar**: `{file_path}`\n"
            f"- **Dimensi**: `{s.get('dimensions')}` ({size_str})\n"
            f"- **Fokus Pola**: {note_str}\n"
        )

    lines.append("### Sintesis Perbandingan:")
    lines.append("- **Saran Ekstraksi:** Ambil struktur layout dan hirarki informasi terbaik, hindari menyalin satu desain secara utuh.")
    lines.append("- **Verifikasi Visual:** Panggil vision_analyze pada masing-masing `Path Gambar` di atas sebelum memutuskan.")
    return "\n".join(lines)

@server.tool()
def uiux_extract_patterns(ref_ids: List[str], problem_type: str = "general") -> str:
    """
    Ekstrak prinsip keputusan desain (Design Decisions) dari beberapa referensi terpilih
    tanpa menyalin gambar mentah ke memori (sesuai Step 6 & 7 AGOTIMA).
    """
    items = _load_catalog()
    items_map = {i.get("id", "").lower(): i for i in items}
    
    selected = [items_map[rid.lower().strip()] for rid in ref_ids if rid.lower().strip() in items_map]
    if not selected:
        return "Referensi tidak ditemukan untuk ekstraksi pola."

    lines = [
        f"### Hasil Sintesis Pola Desain (Masalah: {problem_type})",
        f"Dianalisis dari {len(selected)} referensi: {', '.join([s.get('id').upper() for s in selected])}\n",
        "**Keputusan Desain Siap Simpan (AGOTIMA Unit Memory):**"
    ]

    for s in selected:
        file_path = _get_item_file_path(s)
        lines.append(
            f"```yaml\n"
            f"subject: UI_DESIGN\n"
            f"predicate: pattern_{s.get('category', 'web').replace('-', '_')}\n"
            f"value: {s.get('title')} ({s.get('format', 'PNG')} layout, {s.get('dimensions', '5K')})\n"
            f"scope: design_library\n"
            f"importance: 0.8\n"
            f"confidence: 0.95\n"
            f"source: {file_path}\n"
            f"```"
        )
    return "\n".join(lines)

@server.tool()
def uiux_creative_archetypes() -> str:
    """
    Daftar arketipe desain kreatif anti-repetitif (solusi agar desain web tidak itu-itu terus).
    Menyajikan spesifikasi estetika, palet warna, tipografi, dan filosofi interaksi.
    """
    archetypes = [
        {
            "id": "isometric-3d-wireframe",
            "name": "Isometric 3D Wireframe (ala SpiralDB)",
            "palette": "Stark Monochromatic (Ink Black #0a0a0c, Slate White #f8fafc, Wireframe Line #cbd5e1)",
            "typography": "Heavy Grotesque Sans Display (All-Caps) + Monospace Meta/URL",
            "visual_elements": "3D isometric floating cubes/blocks, dashed grid receding into space, minimalist outline buttons",
            "best_for": "Database systems, developer tooling, 404 pages, technical SaaS"
        },
        {
            "id": "playful-storytelling-vector",
            "name": "Playful Storytelling Vector (ala Maxima Therapy)",
            "palette": "Warm Vibrant Pastels (Blush Pink #fdf2f8, Royal Blue #2563eb, Tangerine #f97316, Soft Lavender #f3e8ff)",
            "typography": "Rounded Geometrical Sans (Plus Jakarta Sans / Nunito) with friendly pill badges",
            "visual_elements": "Organic blob shapes, whimsical characters looking through binoculars/telescopes, storytelling empty states",
            "best_for": "Consumer apps, pediatric/lifestyle platforms, friendly error pages, onboarding"
        },
        {
            "id": "swiss-botanical-ascii",
            "name": "Swiss Modernist Botanical ASCII (ala Maximilian Kaspar)",
            "palette": "Paper Grain Off-White (#fbfbf9) + Architectural Charcoal (#111827)",
            "typography": "Strict Lowercase Monospace (JetBrains Mono / Space Mono) + Giant Serif/Sans Numbers",
            "visual_elements": "Delicate ASCII art illustrations (plants/nature), thin Cartesian grid lines, utilitarian high-density layout",
            "best_for": "Portfolios, editorial magazines, experimental web, high-aesthetic landing pages"
        },
        {
            "id": "neo-brutalist-glitch",
            "name": "Neo-Brutalist Glitch & Data Slice (ala R4XNTECH)",
            "palette": "Tactile Noise White + CMYK Glitch Slices (Red #ef4444, Cyan #06b6d4, Lime #84cc16, Yellow #eab308)",
            "typography": "Ultra-Heavy Grotesque Display + Angle Brackets <...> Code Meta",
            "visual_elements": "Alpha-channel transparency checkerboards, sliced horizontal offset bars, pin-markers with circular endpoints",
            "best_for": "Creative tech showcases, developer agency carousels, error pages, hacker culture"
        },
        {
            "id": "cyber-hud-cockpit",
            "name": "Cyber HUD Cockpit (Telemetri Enterprise)",
            "palette": "Deep Charcoal Slate (#0f172a) + Neon Violet (#8b5cf6) + Emerald (#10b981)",
            "typography": "High-Density JetBrains Mono + Plus Jakarta Sans Headings",
            "visual_elements": "Circular SVG tachometer dials, reactive vector mascot HUD, live tick graphs, zero-emoji SVG icons",
            "best_for": "Real-time telemetry, server monitors, crypto dashboards, trading terminals"
        },
        {
            "id": "warm-paper-obsidian",
            "name": "Warm Paper & Obsidian (Digital Book Vault)",
            "palette": "Warm Cream Paper (#faf6ef) + Architect Obsidian (#14120e)",
            "typography": "Literary Serif Headings (Merriweather/Lora) + High-Legibility Body (Plus Jakarta Sans)",
            "visual_elements": "Tactile dog-ear corner peel fold, book spine crease shadow, silk bookmark ribbon, stipple dot texture",
            "best_for": "Knowledge bases, personal wikis, reading interfaces, documentation books"
        }
    ]

    lines = ["# KATALOG ARKETIPE DESAIN KREATIF (ANTI-DESAIN ITU-ITU TERUS)\n"]
    for a in archetypes:
        lines.append(f"### ✦ {a['name']} (`{a['id']}`)")
        lines.append(f"- **Palet Warna**: {a['palette']}")
        lines.append(f"- **Tipografi**: {a['typography']}")
        lines.append(f"- **Elemen Visual**: {a['visual_elements']}")
        lines.append(f"- **Sangat Cocok Untuk**: {a['best_for']}\n")
    lines.append("Gunakan `uiux_get_component_recipe(archetype, component_type)` untuk menghasilkan kode sasis siap pakai.")
    return "\n".join(lines)

@server.tool()
def uiux_get_component_recipe(archetype: str, component_type: str = "404-error-page") -> str:
    """
    Hasilkan sasis kode komponen siap pakai (HTML/CSS/SVG) berdasarkan arketipe kreatif tertentu.
    Arketipe: 'isometric-3d-wireframe', 'playful-storytelling-vector', 'swiss-botanical-ascii', 'neo-brutalist-glitch'.
    Tipe Komponen: '404-error-page', 'empty-state', 'hero-header', 'interactive-card'.
    """
    arch = archetype.lower().strip()
    comp = component_type.lower().strip()

    if "isometric" in arch:
        return f"""<!-- RECIPE: Isometric 3D Wireframe ({comp}) -->
<div style="background:#fafafa; min-height:480px; padding:3rem 2rem; font-family:'JetBrains Mono',monospace; border:1px solid #e5e7eb; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; position:relative; overflow:hidden;">
  <!-- Isometric Grid Lines Background -->
  <svg style="position:absolute; inset:0; width:100%; height:100%; opacity:0.35;" viewBox="0 0 800 500">
    <pattern id="iso-grid" width="60" height="34.64" patternUnits="userSpaceOnUse" patternTransform="scale(1)">
      <path d="M 0 17.32 L 30 0 L 60 17.32 L 30 34.64 Z" fill="none" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="3 3"/>
    </pattern>
    <rect width="100%" height="100%" fill="url(#iso-grid)" />
    <!-- 3D Isometric Cube Elements -->
    <g transform="translate(400, 160)">
      <polygon points="0,-40 35,-20 0,0 -35,-20" fill="#f1f5f9" stroke="#0f172a" stroke-width="1.8"/>
      <polygon points="-35,-20 0,0 0,40 -35,20" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.8"/>
      <polygon points="0,0 35,-20 35,20 0,40" fill="#94a3b8" stroke="#0f172a" stroke-width="1.8"/>
    </g>
    <g transform="translate(280, 220) scale(0.65)">
      <polygon points="0,-40 35,-20 0,0 -35,-20" fill="#f8fafc" stroke="#475569" stroke-width="1.8"/>
      <polygon points="-35,-20 0,0 0,40 -35,20" fill="#e2e8f0" stroke="#475569" stroke-width="1.8"/>
      <polygon points="0,0 35,-20 35,20 0,40" fill="#cbd5e1" stroke="#475569" stroke-width="1.8"/>
    </g>
  </svg>
  <div style="position:relative; z-index:2; text-align:center; max-width:540px; margin-top:140px;">
    <div style="font-size:0.75rem; letter-spacing:0.18em; text-transform:uppercase; color:#64748b; margin-bottom:0.75rem;">// HTTP STATUS CODE 404</div>
    <h1 style="font-size:2.8rem; font-weight:900; letter-spacing:-0.03em; color:#0f172a; margin:0 0 0.5rem; text-transform:uppercase; font-family:'Plus Jakarta Sans',sans-serif;">PAGE NOT FOUND</h1>
    <p style="font-size:0.85rem; color:#475569; margin-bottom:1.5rem; line-height:1.6;">Titik koordinat data yang Anda cari tidak ditemukan di dalam partisi kisi basis data ini.</p>
    <a href="/" style="display:inline-block; border:1.5px solid #0f172a; padding:0.6rem 1.4rem; border-radius:9999px; font-size:0.75rem; font-weight:700; color:#0f172a; text-decoration:none; text-transform:uppercase; letter-spacing:0.05em; transition:all 0.2s;">[ Kembali ke Beranda ]</a>
  </div>
</div>"""

    elif "playful" in arch:
        return f"""<!-- RECIPE: Playful Storytelling Vector ({comp}) -->
<div style="background:#fdf2f8; min-height:480px; padding:3rem 2rem; border-radius:24px; border:2px solid #fbcfe8; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; font-family:'Plus Jakarta Sans',sans-serif; position:relative; overflow:hidden;">
  <!-- Whimsical Organic Blobs -->
  <div style="position:absolute; top:-40px; left:-40px; width:220px; height:220px; background:#fde047; opacity:0.45; border-radius:58% 42% 65% 35% / 45% 60% 40% 55%; filter:blur(20px);"></div>
  <div style="position:absolute; bottom:-50px; right:-50px; width:280px; height:280px; background:#60a5fa; opacity:0.35; border-radius:40% 60% 35% 65% / 55% 35% 65% 45%; filter:blur(25px);"></div>
  <!-- Character Illustration with Binoculars (Pure SVG) -->
  <svg width="180" height="140" viewBox="0 0 180 140" style="position:relative; z-index:2; margin-bottom:1rem;">
    <!-- Large Blue 404 -->
    <text x="90" y="55" font-size="54" font-weight="900" fill="#2563eb" text-anchor="middle" font-family="'Plus Jakarta Sans',sans-serif" letter-spacing="-2">404</text>
    <!-- Whimsical Binoculars -->
    <g transform="translate(50, 65)">
      <circle cx="25" cy="25" r="22" fill="#f97316" stroke="#0f172a" stroke-width="3"/>
      <circle cx="25" cy="25" r="14" fill="#67e8f9"/>
      <circle cx="55" cy="25" r="22" fill="#f97316" stroke="#0f172a" stroke-width="3"/>
      <circle cx="55" cy="25" r="14" fill="#67e8f9"/>
      <rect x="35" y="21" width="10" height="8" rx="4" fill="#0f172a"/>
      <!-- Eyes reflection -->
      <circle cx="22" cy="20" r="4" fill="#ffffff"/>
      <circle cx="52" cy="20" r="4" fill="#ffffff"/>
    </g>
  </svg>
  <div style="position:relative; z-index:2; max-width:480px;">
    <h2 style="font-size:1.85rem; font-weight:800; color:#1e293b; margin:0 0 0.5rem;">Ups! Kami Sudah Mencarinya ke Mana-mana...</h2>
    <p style="font-size:0.92rem; color:#64748b; line-height:1.5; margin-bottom:1.5rem;">Halaman yang Anda tuju sepertinya sedang berpetualang ke tempat lain. Yuk kembali ke jalan yang aman!</p>
    <a href="/" style="display:inline-flex; align-items:center; gap:8px; background:#2563eb; color:#ffffff; padding:0.75rem 1.6rem; border-radius:9999px; font-weight:700; font-size:0.85rem; text-decoration:none; box-shadow:0 8px 20px rgba(37,99,235,0.25);">
      Kembali ke Beranda
    </a>
  </div>
</div>"""

    elif "ascii" in arch:
        return f"""<!-- RECIPE: Swiss Modernist Botanical ASCII ({comp}) -->
<div style="background:#fbfbf9; min-height:480px; padding:2.5rem; border:1px solid #111827; font-family:'JetBrains Mono',monospace; position:relative; display:grid; grid-template-columns:1fr 1fr; gap:2rem; align-items:center;">
  <!-- Strict Architectural Cartesian Grid Frame -->
  <div style="position:absolute; top:12px; left:12px; font-size:0.65rem; color:#6b7280; letter-spacing:0.1em;">■ ARCHITECTURAL SWISS GRID · 04/05</div>
  <div style="position:absolute; bottom:12px; right:12px; font-size:0.65rem; color:#6b7280; letter-spacing:0.1em;">REF: BOTANICAL-ASCII-SYSTEM</div>
  <!-- Left Column: Botanical ASCII Art -->
  <div style="background:#ffffff; border:1px solid #e5e7eb; padding:1.5rem; border-radius:4px; text-align:center;">
    <pre style="margin:0; font-size:0.68rem; line-height:1.2; color:#111827; font-family:monospace; user-select:none;">
          .::.
        :;;;;;;:
       :;;;;;;;;:
        :;;;;;;:
          :;;:
           ||
       .::.||.::.
      :;;;;||;;;;:
     :;;;;;||;;;;;:
      :;;;;||;;;;:
        '::||::'
           ||
           ||  /\\
           || //\\\\
           ||//  \\\\
    ───────███████───────
    </pre>
    <div style="font-size:2.4rem; font-weight:800; color:#111827; letter-spacing:-0.04em; margin-top:0.5rem;">404</div>
  </div>
  <!-- Right Column: Minimalist Utilitarian Copy -->
  <div>
    <div style="font-size:0.72rem; color:#9ca3af; text-transform:lowercase; margin-bottom:0.5rem;">[status: item_not_found]</div>
    <h3 style="font-size:1.6rem; font-weight:700; color:#111827; letter-spacing:-0.03em; margin:0 0 0.75rem; text-transform:lowercase;">halaman tidak terpetakan.</h3>
    <p style="font-size:0.8rem; color:#4b5563; line-height:1.6; margin-bottom:1.5rem;">
      jalur url yang anda panggil belum didefinisikan pada sistem struktur ini. silakan verifikasi rute atau kembali ke root indeks.
    </p>
    <div style="display:flex; gap:12px;">
      <a href="/" style="font-size:0.75rem; color:#111827; text-decoration:underline; font-weight:700;">[root_index]</a>
      <a href="javascript:history.back()" style="font-size:0.75rem; color:#6b7280; text-decoration:none;">[kembali]</a>
    </div>
  </div>
</div>"""

    else:
        return f"""<!-- RECIPE: Neo-Brutalist Glitch ({comp}) -->
<div style="background:#f8fafc; border:2.5px solid #000000; box-shadow:6px 6px 0 #000000; border-radius:12px; padding:2.5rem; font-family:'Plus Jakarta Sans',sans-serif; position:relative; overflow:hidden;">
  <!-- Glitch Color Slices & Transparency Grid -->
  <div style="position:absolute; top:20px; right:20px; display:flex; gap:4px;">
    <div style="width:18px; height:6px; background:#ef4444;"></div>
    <div style="width:18px; height:6px; background:#06b6d4;"></div>
    <div style="width:18px; height:6px; background:#84cc16;"></div>
    <div style="width:18px; height:6px; background:#eab308;"></div>
  </div>
  <span style="display:inline-block; background:#fef08a; border:1.5px solid #000000; padding:3px 8px; font-size:0.7rem; font-weight:800; font-family:'JetBrains Mono',monospace; margin-bottom:1rem;">
    &lt;ERROR_TYPE: ROUTE_MISSING&gt;
  </span>
  <h1 style="font-size:2.5rem; font-weight:900; color:#000000; margin:0 0 0.5rem; letter-spacing:-0.02em;">
    NOTHING HERE BUT GLITCHES.
  </h1>
  <p style="font-size:0.9rem; color:#334155; font-weight:600; line-height:1.5; max-width:480px; margin-bottom:1.5rem;">
    Halaman ini menghilang atau belum pernah dibangun. Jangan khawatir, sistem inti tetap beroperasi 100%.
  </p>
  <a href="/" style="display:inline-block; background:#000000; color:#ffffff; font-weight:800; font-size:0.85rem; padding:0.75rem 1.5rem; text-decoration:none; border-radius:8px; box-shadow:3px 3px 0 #06b6d4;">
    KEMBALI KE BERANDA ➔
  </a>
</div>"""

if __name__ == "__main__":
    asyncio.run(server.run_stdio_async())
