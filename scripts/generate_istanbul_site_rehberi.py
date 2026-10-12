#!/usr/bin/env python3
"""İstanbul Site ve Yönetim Rehberi PDF üretici."""

from pathlib import Path
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)

# Fontlar
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

NAVY = colors.HexColor("#1a365d")
TEAL = colors.HexColor("#0d9488")
LIGHT = colors.HexColor("#f0fdfa")
GRAY = colors.HexColor("#64748b")
ROW_ALT = colors.HexColor("#f8fafc")
WHITE = colors.white

# Veri: bölge -> ilçe -> kayıtlar
# tip: "site" | "firma"
DATA = {
    "Avrupa Yakası — Batı İstanbul": {
        "Başakşehir": [
            {"ad": "Başakşehir 1. Etap Site Yönetimi", "telefon": "0212 485 12 06 / 07", "not": "Cep: 0533 744 35 41", "tip": "site"},
            {"ad": "Başakşehir 2. Etap Site Yönetimi", "telefon": "0212 485 17 40", "not": "Güvenlik: 0212 485 45 12", "tip": "site"},
            {"ad": "Başakşehir 4. Etap Site Yönetimi", "telefon": "0212 487 12 00", "not": "Güvenlik: 0212 487 40 00", "tip": "site"},
            {"ad": "Başakşehir 5. Etap Site Yönetimi", "telefon": "0212 487 30 39", "not": "", "tip": "site"},
            {"ad": "Onurkent Site Yönetimi", "telefon": "0212 488 09 10", "not": "", "tip": "site"},
            {"ad": "Göçmen Konutları Site Yönetimi", "telefon": "0212 486 00 19", "not": "", "tip": "site"},
            {"ad": "Kalıcı Afet Konutları Site Yönetimi", "telefon": "0212 487 64 43", "not": "", "tip": "site"},
            {"ad": "Kayabaşı Kiptaş Konutları Site Yönetimi", "telefon": "0212 688 10 10", "not": "İstiklal Cad. 202/1A", "tip": "site"},
        ],
        "Küçükçekmece / Halkalı": [
            {"ad": "Emlak Yönetim Hizmetleri A.Ş. (TOKİ)", "telefon": "444 84 34", "not": "Halkalı Atakent — Türkiye geneli TOKİ siteleri", "tip": "firma"},
            {"ad": "Emlak Yönetim (sabit hat)", "telefon": "0212 669 83 91", "not": "info@emlakyonetim.com.tr", "tip": "firma"},
            {"ad": "Öncü Profesyonel Apartman & Site Yönetimi", "telefon": "0212 729 02 22", "not": "Başkomutan Cad. No:74", "tip": "firma"},
        ],
        "Beylikdüzü": [
            {"ad": "SMC Yapısal Yönetim Danışmanlık", "telefon": "0212 877 95 64", "not": "Cep: 0541 109 51 52 — Perlavista Residence", "tip": "firma"},
            {"ad": "İstanbul Site Yönetimi A.Ş.", "telefon": "0850 224 85 75", "not": "Hürriyet Bulvarı", "tip": "firma"},
            {"ad": "Projemax Tesis Yönetim A.Ş.", "telefon": "0850 305 88 65", "not": "Yakuplu Mah. — İstanbul geneli", "tip": "firma"},
            {"ad": "Vural Group Tesis Yönetimi", "telefon": "0850 346 01 12", "not": "Cep: 0544 174 34 34 — Büyükçekmece/Beykent", "tip": "firma"},
            {"ad": "Akel Bina & Site Yönetimi", "telefon": "0537 710 06 56", "not": "Beylikdüzü / Esenyurt / Kadıköy", "tip": "firma"},
        ],
        "Esenyurt": [
            {"ad": "Delta Profesyonel Yapı Yönetim", "telefon": "0533 661 40 47", "not": "Fatih Mah. Ünverdi Cad.", "tip": "firma"},
            {"ad": "Live Şelale Sitesi (Parga Yönetim)", "telefon": "0546 762 00 02", "not": "Parga Yönetim referansı", "tip": "site"},
            {"ad": "Akel Bina & Site Yönetimi", "telefon": "0537 710 06 56", "not": "Esenyurt hizmet bölgesi", "tip": "firma"},
        ],
        "Büyükçekmece": [
            {"ad": "Vural Group", "telefon": "0850 346 01 12", "not": "Pınartepe / Beykent Plaza", "tip": "firma"},
            {"ad": "Palmiye Konakları (Parga Yönetim)", "telefon": "0212 993 59 59", "not": "Parga Yönetim referansı", "tip": "site"},
        ],
    },
    "Avrupa Yakası — Merkez & Kuzey": {
        "Bahçelievler / Bakırköy": [
            {"ad": "Parga Yönetim", "telefon": "0546 762 00 02", "not": "Santral: 0212 993 59 59 — Mahmutbey Cad.", "tip": "firma"},
            {"ad": "Parga Yönetim Muhasebe", "telefon": "0533 778 50 80", "not": "", "tip": "firma"},
            {"ad": "Destek Site Yönetimi (Bakırköy)", "telefon": "0212 567 22 58", "not": "Cep: 0532 698 02 18", "tip": "firma"},
            {"ad": "O.116–O.117 Blokları (Bakırköy)", "telefon": "0546 762 00 02", "not": "Parga Yönetim", "tip": "site"},
            {"ad": "Orkide Apartmanı (Bakırköy)", "telefon": "0546 762 00 02", "not": "Parga Yönetim", "tip": "site"},
            {"ad": "Raftoz Argun Sitesi", "telefon": "0546 762 00 02", "not": "Parga Yönetim", "tip": "site"},
        ],
        "Bayrampaşa / Eyüpsultan": [
            {"ad": "Destek Site Yönetimi Danışmanlık", "telefon": "0212 567 22 58", "not": "Yenidoğan Mah. Abdi İpekçi Cad. — Kartal dahil", "tip": "firma"},
            {"ad": "Yönetim Firmaları", "telefon": "0212 534 70 86", "not": "Merkez Avrupa yakası", "tip": "firma"},
        ],
        "Kağıthane / Şişli / Beyoğlu": [
            {"ad": "Bengisu Evleri B Blok", "telefon": "0546 762 00 02", "not": "Parga Yönetim — Kağıthane", "tip": "site"},
            {"ad": "Akbaytugan Apartmanı", "telefon": "0546 762 00 02", "not": "Parga Yönetim — Beyoğlu", "tip": "site"},
            {"ad": "MY Yönetim ve Danışmanlık", "telefon": "0501 278 95 61", "not": "Yurt Sok. No:12", "tip": "firma"},
        ],
        "Sarıyer / Maslak": [
            {"ad": "S.S. Mashattan Site İşletme Kooperatifi", "telefon": "0212 330 46 00", "not": "Maslak Mah. Anka Sk. No:2", "tip": "site"},
            {"ad": "Mashattan Cake Gallery / Hizmet", "telefon": "0212 330 43 00", "not": "Site içi hizmet hattı", "tip": "site"},
        ],
    },
    "Anadolu Yakası — Kadıköy Aksı": {
        "Kadıköy": [
            {"ad": "Alo Yönetim (Genel Müdürlük)", "telefon": "0216 550 48 48", "not": "Osmanağa, Misak-ı Milli Sok. No:94A", "tip": "firma"},
            {"ad": "Akel Bina & Site Yönetimi", "telefon": "0537 710 06 56", "not": "Kadıköy bina & site yönetimi", "tip": "firma"},
            {"ad": "Lila Yönetim", "telefon": "0216 551 02 00", "not": "Kadıköy / Suadiye / Çengelköy hizmet", "tip": "firma"},
            {"ad": "FAYDA Yönetim", "telefon": "0532 284 37 38", "not": "Hızırbey Cad. — Kadıköy", "tip": "firma"},
        ],
        "Maltepe": [
            {"ad": "Daimi Apartman ve Site Yönetimi", "telefon": "0216 388 63 63", "not": "Bağdat Cad. Nefes Plaza — Anadolu yakası", "tip": "firma"},
            {"ad": "Alo Yönetim (Maltepe Saha)", "telefon": "0216 550 48 48", "not": "Bağlarbaşı Mah. Bağdat Cad. No:310 — 29+ proje", "tip": "firma"},
        ],
        "Ataşehir": [
            {"ad": "Emlak Konut GYO Genel Müdürlük", "telefon": "444 36 55", "not": "Batı Ataşehir — proje/satış hattı", "tip": "firma"},
            {"ad": "Projemax Tesis Yönetim", "telefon": "0850 305 88 65", "not": "Ataşehir site yönetimi", "tip": "firma"},
            {"ad": "Lila Yönetim", "telefon": "0216 551 02 00", "not": "Ataşehir referans bölgesi", "tip": "firma"},
            {"ad": "Daimi Yönetim", "telefon": "0216 388 63 63", "not": "Ataşehir hizmet bölgesi", "tip": "firma"},
        ],
        "Üsküdar": [
            {"ad": "Ağaoğlu My Dream Site Yönetmenliği", "telefon": "0216 557 86 02", "not": "Burhaniye Mah. Tunuslu Mahmut Paşa Cad. No:25", "tip": "site"},
            {"ad": "Lila Yönetim", "telefon": "0216 551 02 00", "not": "Üsküdar / Çamlıca / Çengelköy", "tip": "firma"},
            {"ad": "Nil Apartmanı (Parga Yönetim)", "telefon": "0546 762 00 02", "not": "Parga Yönetim referansı", "tip": "site"},
        ],
    },
    "Anadolu Yakası — Doğu & Kuzey": {
        "Ümraniye": [
            {"ad": "Lila Yönetim", "telefon": "0216 551 02 00", "not": "Ümraniye merkez ofis", "tip": "firma"},
            {"ad": "NFS Tesis Yönetim Hizmetleri", "telefon": "0216 594 64 00", "not": "Royal Plaza D:16", "tip": "firma"},
            {"ad": "Ağaoğlu Eltes Güneşi Site Yönetimi", "telefon": "0216 526 41 66", "not": "Esenşehir Mah. Baraj Yolu Cad. No:17", "tip": "site"},
            {"ad": "Ağaoğlu My City Yönetim", "telefon": "0216 526 00 91", "not": "Sosyal tesisler: 0216 526 00 92 — Tavukçuyolu Cad.", "tip": "site"},
            {"ad": "Zirve Konakları Sitesi", "telefon": "0546 762 00 02", "not": "Parga Yönetim", "tip": "site"},
            {"ad": "Armağanevler Sitesi", "telefon": "0546 762 00 02", "not": "Parga Yönetim", "tip": "site"},
        ],
        "Kartal": [
            {"ad": "Destek Site Yönetimi (Kartal)", "telefon": "0212 567 22 58", "not": "Cep: 0532 698 02 18", "tip": "firma"},
            {"ad": "Daimi Yönetim", "telefon": "0216 388 63 63", "not": "Kartal hizmet bölgesi", "tip": "firma"},
        ],
        "Pendik": [
            {"ad": "Sky Tesis Yönetim Hizmetleri", "telefon": "0216 222 07 05", "not": "Genel merkez: 0216 766 15 55 — Osmanlı Bulvarı", "tip": "firma"},
            {"ad": "Projemax Tesis Yönetim", "telefon": "0850 305 88 65", "not": "Pendik site yönetimi", "tip": "firma"},
            {"ad": "Daimi Yönetim", "telefon": "0216 388 63 63", "not": "Pendik hizmet bölgesi", "tip": "firma"},
        ],
        "Sancaktepe / Çekmeköy": [
            {"ad": "Projemax Tesis Yönetim", "telefon": "0850 305 88 65", "not": "Sancaktepe hizmet bölgesi", "tip": "firma"},
            {"ad": "Daimi Yönetim", "telefon": "0216 388 63 63", "not": "Anadolu yakası geneli", "tip": "firma"},
        ],
    },
}


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            fontName="DejaVuBold",
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            textColor=NAVY,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            fontName="DejaVu",
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=GRAY,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="RegionTitle",
            fontName="DejaVuBold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="DistrictTitle",
            fontName="DejaVuBold",
            fontSize=11,
            leading=14,
            textColor=TEAL,
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTR",
            fontName="DejaVu",
            fontSize=9,
            leading=13,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#334155"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CellAd",
            fontName="DejaVu",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#0f172a"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="CellBold",
            fontName="DejaVuBold",
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#0f172a"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="CellSmall",
            fontName="DejaVu",
            fontSize=7.5,
            leading=10,
            textColor=GRAY,
        )
    )
    styles.add(
        ParagraphStyle(
            name="FooterNote",
            fontName="DejaVu",
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=GRAY,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TOCItem",
            fontName="DejaVu",
            fontSize=10,
            leading=16,
            textColor=NAVY,
            leftIndent=10,
        )
    )
    return styles


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.2)
    canvas.line(1.5 * cm, A4[1] - 1.2 * cm, A4[0] - 1.5 * cm, A4[1] - 1.2 * cm)
    canvas.setFont("DejaVu", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(1.5 * cm, A4[1] - 1.0 * cm, "İstanbul Site ve Yönetim Rehberi")
    canvas.drawRightString(A4[0] - 1.5 * cm, A4[1] - 1.0 * cm, "Kamuya açık kaynak derlemesi")
    canvas.line(1.5 * cm, 1.3 * cm, A4[0] - 1.5 * cm, 1.3 * cm)
    canvas.drawCentredString(A4[0] / 2, 0.8 * cm, f"Sayfa {doc.page}  |  {date.today().strftime('%d.%m.%Y')}")
    canvas.restoreState()


def make_table(records, styles):
    header = [
        Paragraph("<b>Ad / Unvan</b>", styles["CellBold"]),
        Paragraph("<b>Telefon</b>", styles["CellBold"]),
        Paragraph("<b>Tür</b>", styles["CellBold"]),
        Paragraph("<b>Not / Adres</b>", styles["CellBold"]),
    ]
    rows = [header]
    for r in records:
        tip_label = "Site Yönetimi" if r["tip"] == "site" else "Yönetim Firması"
        rows.append(
            [
                Paragraph(r["ad"], styles["CellAd"]),
                Paragraph(r["telefon"], styles["CellBold"]),
                Paragraph(tip_label, styles["CellSmall"]),
                Paragraph(r["not"] or "—", styles["CellSmall"]),
            ]
        )

    col_widths = [6.8 * cm, 3.6 * cm, 2.6 * cm, 5.0 * cm]
    table = Table(rows, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "DejaVuBold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("BOX", (0, 0), (-1, -1), 0.8, NAVY),
    ]
    for i in range(1, len(rows)):
        bg = LIGHT if i % 2 == 0 else ROW_ALT
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
        # Site satırlarında sol kenar vurgusu için tip sütununa hafif renk
        if records[i - 1]["tip"] == "site":
            style_cmds.append(("BACKGROUND", (2, i), (2, i), colors.HexColor("#ccfbf1")))
        else:
            style_cmds.append(("BACKGROUND", (2, i), (2, i), colors.HexColor("#e0e7ff")))
    table.setStyle(TableStyle(style_cmds))
    return table


def build_pdf(output_path: Path):
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="İstanbul Site ve Yönetim Rehberi",
        author="Kamuya açık kaynak derlemesi",
    )

    story = []

    # Kapak
    story.append(Spacer(1, 3.5 * cm))
    story.append(Paragraph("İSTANBUL", styles["CoverTitle"]))
    story.append(Paragraph("Site ve Yönetim Rehberi", styles["CoverTitle"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(HRFlowable(width="60%", thickness=2, color=TEAL, spaceBefore=4, spaceAfter=12, hAlign="CENTER"))
    story.append(Paragraph("Bölge ve ilçe bazlı sınıflandırma", styles["CoverSub"]))
    story.append(Paragraph("Site yönetimleri • Profesyonel yönetim firmaları • Telefon numaraları", styles["CoverSub"]))
    story.append(Spacer(1, 1.2 * cm))
    story.append(
        Paragraph(
            f"Derleme tarihi: {date.today().strftime('%d.%m.%Y')}<br/>"
            "Kaynak: Kamuya açık web siteleri, kurumsal iletişim sayfaları ve yerel rehberler",
            styles["CoverSub"],
        )
    )
    story.append(Spacer(1, 2 * cm))
    story.append(
        Paragraph(
            "<b>Önemli uyarı:</b> İstanbul’da on binlerce site bulunmaktadır. Bu belge, kamuya açık "
            "kaynaklardan derlenen örnek bir rehberdir; eksiksiz bir envanter değildir. Telefon "
            "numaraları değişebilir; kullanım öncesi ilgili yönetimle teyit ediniz.",
            styles["BodyTR"],
        )
    )
    story.append(PageBreak())

    # İçindekiler
    story.append(Paragraph("İçindekiler", styles["RegionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceBefore=2, spaceAfter=10))
    for region in DATA:
        story.append(Paragraph(f"• {region}", styles["TOCItem"]))
        for district in DATA[region]:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;— {district}", styles["CellSmall"]))
    story.append(Spacer(1, 0.6 * cm))
    story.append(
        Paragraph(
            "<b>Renk anahtarı:</b> "
            "<font color='#0d9488'>■</font> Site Yönetimi &nbsp;&nbsp; "
            "<font color='#4338ca'>■</font> Yönetim Firması",
            styles["BodyTR"],
        )
    )
    story.append(PageBreak())

    # Bölümler
    for region, districts in DATA.items():
        story.append(Paragraph(region, styles["RegionTitle"]))
        story.append(HRFlowable(width="100%", thickness=1.5, color=NAVY, spaceBefore=2, spaceAfter=8))
        for district, records in districts.items():
            block = [
                Paragraph(district, styles["DistrictTitle"]),
                make_table(records, styles),
                Spacer(1, 0.35 * cm),
            ]
            story.append(KeepTogether(block))
        story.append(Spacer(1, 0.3 * cm))

    # Kaynaklar
    story.append(PageBreak())
    story.append(Paragraph("Kaynaklar ve Notlar", styles["RegionTitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceBefore=2, spaceAfter=8))
    sources = [
        "Emlak Yönetim Hizmetleri A.Ş. (emlakyonetim.com.tr) — TOKİ siteleri genel hattı",
        "Emlak Konut GYO (emlakkonut.com.tr) — Ataşehir genel müdürlük",
        "Başakşehir 1. Etap (basaksehir1.com) ve BaŞakHaber yerel telefon listesi",
        "Daimi Yönetim, Lila Yönetim, Alo Yönetim, Projemax, Sky Yönetim, Parga Yönetim, SMC Yönetim kurumsal siteleri",
        "Destek Site Yönetimi, Delta Yönetim, Akel Bina Yönetimi, Vural Group, NFS Tesis Yönetim",
        "Mashattan Site İşletme Kooperatifi (mashattan.org.tr)",
        "Ağaoğlu My Dream / My City / Eltes Güneşi — harita ve rehber kayıtları",
        "Kayabaşı Kiptaş Konutları Site Yönetimi — harita kaydı",
    ]
    for s in sources:
        story.append(Paragraph(f"• {s}", styles["BodyTR"]))

    story.append(Spacer(1, 0.8 * cm))
    story.append(
        Paragraph(
            "Bu PDF yalnızca bilgilendirme amaçlıdır. Ticari, pazarlama veya istenmeyen arama "
            "(spam) amaçlı kullanım önerilmez. Güncel bilgi için ilgili site yönetimi veya "
            "belediye / kat malikleri kurulu ile iletişime geçiniz.",
            styles["FooterNote"],
        )
    )

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return output_path


def main():
    out_docs = Path("/workspace/docs/Istanbul_Site_ve_Yonetim_Rehberi.pdf")
    out_art = Path("/opt/cursor/artifacts/Istanbul_Site_ve_Yonetim_Rehberi.pdf")
    out_docs.parent.mkdir(parents=True, exist_ok=True)
    out_art.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(out_docs)
    # Kopya artifact
    out_art.write_bytes(out_docs.read_bytes())
    print(f"PDF oluşturuldu: {out_docs}")
    print(f"Artifact: {out_art}")
    print(f"Boyut: {out_docs.stat().st_size} bayt")


if __name__ == "__main__":
    main()
