from src.models.recommendation import Recommendation
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors


class PDFFormatter:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()

    def generate_pdf(self, recommendation: Recommendation) -> Path:
        filename = f"{recommendation.patient_name}_{recommendation.patient_surname}_supplements.pdf"
        filepath = self.output_dir / filename

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=2.5 * cm,
            leftMargin=2.5 * cm,
            topMargin=2.5 * cm,
            bottomMargin=2.5 * cm,
        )

        elements = []

        elements.append(Paragraph("Rekomendacja Suplementacji", self.styles["Title"]))
        elements.append(Spacer(1, 1 * cm))

        patient_info = f"<b>Pacjent:</b> {recommendation.patient_name} {recommendation.patient_surname}<br/>"
        patient_info += f"<b>Data:</b> {recommendation.date.strftime('%Y-%m-%d %H:%M')}"
        elements.append(Paragraph(patient_info, self.styles["Normal"]))
        elements.append(Spacer(1, 1 * cm))

        if not recommendation.supplements:
            elements.append(
                Paragraph("Brak rekomendacji suplementacji.", self.styles["Normal"])
            )
        else:
            elements.append(
                Paragraph("Rekomendowane Suplementy:", self.styles["Heading2"])
            )
            elements.append(Spacer(1, 0.5 * cm))

            table_data = [
                [
                    "Lp.",
                    "Suplement",
                    "Dawkowanie",
                    "Pora przyjmowania",
                    "Priorytet",
                    "Powód",
                ]
            ]

            for idx, supplement in enumerate(recommendation.supplements, 1):
                priority_display = self._get_priority_display(supplement.priority)
                row = [
                    str(idx),
                    supplement.name,
                    supplement.dosage,
                    supplement.timing,
                    priority_display,
                    supplement.reason,
                ]
                table_data.append(row)

            table = Table(
                table_data,
                colWidths=[0.8 * cm, 3.5 * cm, 3.2 * cm, 3.2 * cm, 2 * cm, 5.5 * cm],
                repeatRows=1,
                hAlign="LEFT",
            )
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
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
        priority_translations = {
            "critical": "Krytyczny",
            "high": "Wysoki",
            "medium": "Średni",
            "low": "Niski",
        }
        return priority_translations.get(priority, priority)
