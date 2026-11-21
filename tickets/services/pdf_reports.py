
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_admin_report_pdf(report_data):
    """
    Generate a company-wide complaint report.

    report_data contains the same statistics
    calculated by the Admin Reports view.
    """
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    elements = []

    elements.append(
        Paragraph('IssueInsight - Complaint Report', title_style)
    )

    elements.append(
        Paragraph(
            f"Reporting Period: {report_data['period_label']}",
            styles['Normal'],
        )
    )

    elements.append(Spacer(1, 0.2 * inch))

    elements.append(
        Paragraph(
            f"Total Complaints: {report_data['total']}",
            styles['Heading2'],
        )
    )

    elements.append(Spacer(1, 0.15 * inch))

    def add_table(title, rows):
        elements.append(
            Paragraph(title, styles['Heading3'])
        )

        table_data = [['Description', 'Count']]

        for label, count in rows:
            table_data.append([str(label), str(count)])

        table = Table(
            table_data,
            colWidths=[330, 120],
            repeatRows=1,
            hAlign='LEFT',
        )

        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.2 * inch))

    add_table('Complaints by Status', report_data['status'])
    add_table('Complaints by Department', report_data['departments'])
    add_table('Complaints by Source', report_data['sources'])
    add_table('Complaints by Urgency', report_data['urgencies'])
    add_table('Complaints by Category', report_data['categories'])

    elements.append(
        Paragraph('Resolution Performance', styles['Heading3'])
    )

    performance = [
        ['Metric', 'Value'],
        ['Resolved or Closed', str(report_data['completed_count'])],
        ['Resolution Rate', f"{report_data['resolution_rate']}%"],
        [
            'Average First Response',
            report_data['average_response'],
        ],
        [
            'Average Resolution Time',
            report_data['average_resolution'],
        ],
    ]

    performance_table = Table(
        performance,
        colWidths=[330, 120],
        repeatRows=1,
        hAlign='LEFT',
    )

    performance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(performance_table)

    document.build(elements)

    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content
