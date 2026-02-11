import os
import re
from pathlib import Path
from typing import Tuple

from src.models.recommendation import Recommendation
from src.utils.i18n import t
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_polish_fonts():
    """Register fonts with Polish character support."""
    # Try to find a font with Polish character support
    font_paths = [
        # Linux paths
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
        (
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ),
        # macOS paths
        ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Helvetica.ttc"),
        ("/System/Library/Fonts/ArialHB.ttc", "/System/Library/Fonts/ArialHB.ttc"),
        # Windows paths
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
        ("C:/Windows/Fonts/tahoma.ttf", "C:/Windows/Fonts/tahomabd.ttf"),
    ]

    for regular_path, bold_path in font_paths:
        try:
            pdfmetrics.registerFont(TTFont("CustomFont", regular_path))
            pdfmetrics.registerFont(TTFont("CustomFont-Bold", bold_path))
            return "CustomFont", "CustomFont-Bold"
        except:
            continue

    # Fallback to standard fonts (may not support Polish characters)
    return "Helvetica", "Helvetica-Bold"


def sanitize_filename(name: str) -> str:
    invalid_chars = r"[<>:\"/\\|?*\x00-\x1f]"
    sanitized = re.sub(invalid_chars, "_", name)
    return sanitized[:100]


class PDFFormatter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self.font_name, self.font_name_bold = register_polish_fonts()
        self._configure_styles()

    def _configure_styles(self):
        for style_name in ["Normal", "Title", "Heading2"]:
            if style_name in self.styles:
                self.styles[style_name].fontName = self.font_name

    def generate_pdf(self, recommendation: Recommendation) -> Path:
        safe_name = sanitize_filename(recommendation.patient_name)
        safe_surname = sanitize_filename(recommendation.patient_surname)
        filename = f"{safe_name}_{safe_surname}_supplements.pdf"
        filepath = self.output_dir / filename

        counter = 1
        original_filepath = filepath
        while filepath.exists():
            filename = f"{safe_name}_{safe_surname}_{counter}_supplements.pdf"
            filepath = self.output_dir / filename
            counter += 1
            if counter > 1000:
                raise IOError("Cannot generate unique filename")

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=2.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=2.5 * cm,
            bottomMargin=2.5 * cm,
        )

        elements = []

        # Medical disclaimer - prominently displayed at the top
        disclaimer_style = ParagraphStyle(
            "Disclaimer",
            parent=self.styles["Normal"],
            fontSize=7,
            textColor=colors.red,
            alignment=TA_CENTER,
            leading=10,
        )
        disclaimer_text = t("pdf.disclaimer")
        elements.append(Paragraph(disclaimer_text, disclaimer_style))
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(Paragraph("─" * 60, self.styles["Normal"]))
        elements.append(Spacer(1, 0.5 * cm))

        elements.append(Paragraph(t("pdf.title"), self.styles["Title"]))
        elements.append(Spacer(1, 1 * cm))

        patient_info = f"<b>{t('pdf.patient')}:</b> {recommendation.patient_name} {recommendation.patient_surname}<br/>"
        patient_info += f"<b>{t('pdf.date')}:</b> {recommendation.date.strftime('%Y-%m-%d %H:%M')}"
        elements.append(Paragraph(patient_info, self.styles["Normal"]))
        elements.append(Spacer(1, 1 * cm))

        if not recommendation.supplements:
            elements.append(
                Paragraph(t("pdf.no_supplements"), self.styles["Normal"])
            )
        else:
            elements.append(
                Paragraph(t("pdf.recommended_supplements"), self.styles["Heading2"])
            )
            elements.append(Spacer(1, 0.5 * cm))

            # Create cell style for text wrapping - LTR wraps only at word boundaries
            cell_style = ParagraphStyle(
                "TableCell",
                parent=self.styles["Normal"],
                fontName=self.font_name,
                fontSize=9,
                leading=12,
                wordWrap="LTR",
            )

            # Header style - no word wrapping, keep on single line
            header_style = ParagraphStyle(
                "TableHeader",
                parent=self.styles["Normal"],
                fontName=self.font_name_bold,
                fontSize=9,
                leading=12,
                textColor=colors.whitesmoke,
                wordWrap="LTR",
            )

            table_data = [
                [
                    Paragraph("Lp.", header_style),
                    Paragraph(t("pdf.supplement"), header_style),
                    Paragraph(t("pdf.dosage"), header_style),
                    Paragraph(t("pdf.timing"), header_style),
                    Paragraph(t("pdf.priority"), header_style),
                    Paragraph(t("pdf.reason"), header_style),
                ]
            ]

            for idx, supplement in enumerate(recommendation.supplements, 1):
                priority_display = self._get_priority_display(supplement.priority)
                row = [
                    Paragraph(str(idx), cell_style),
                    Paragraph(supplement.name, cell_style),
                    Paragraph(supplement.dosage, cell_style),
                    Paragraph(supplement.timing, cell_style),
                    Paragraph(priority_display, cell_style),
                    Paragraph(supplement.reason, cell_style),
                ]
                table_data.append(row)

            # Calculate column widths based on page width
            # Ensure headers fit on single line
            page_width = A4[0] - 5 * cm
            col_widths = [
                0.8 * cm,
                3.0 * cm,
                2.8 * cm,
                3.0 * cm,
                2.0 * cm,
                page_width - 11.6 * cm,
            ]

            table = Table(
                table_data,
                colWidths=col_widths,
                repeatRows=1,
                hAlign="LEFT",
            )
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("FONTNAME", (0, 0), (-1, 0), self.font_name_bold),
                        ("FONTNAME", (0, 1), (-1, -1), self.font_name),
                        ("FONTSIZE", (0, 0), (-1, 0), 9),
                        ("FONTSIZE", (0, 1), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                        ("TOPPADDING", (0, 0), (-1, 0), 8),
                        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                        ("TOPPADDING", (0, 1), (-1, -1), 6),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ]
                )
            )

            elements.append(table)
            elements.append(Spacer(1, 1 * cm))

            elements.append(
                Paragraph(
                    "<b>UWAGA:</b> Powyższe rekomendacje mają charakter informacyjny i nie zastępują profesjonalnej porady medycznej.",
                    ParagraphStyle(
                        "Warning",
                        parent=self.styles["Normal"],
                        fontSize=8,
                        textColor=colors.red,
                        alignment=TA_LEFT,
                    ),
                )
            )

        doc.build(elements)
        return filepath

    def _get_priority_display(self, priority: str) -> str:
        return t(f"pdf.priority_{priority}")
