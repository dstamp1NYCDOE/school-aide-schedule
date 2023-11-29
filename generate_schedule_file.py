import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import Paragraph, PageBreak, Spacer, Image, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, landscape

styles = getSampleStyleSheet()


def main(data):
    TWRF_filename = data["TWRF_filename"]

    TWRF_df = pd.read_csv(TWRF_filename).fillna("")
    TWRF_df["Assigned School Aide"] = ""
    assignment_cols = [
        "Period 0",
        "Period 1",
        "Period 2",
        "Period 3",
        "Period 4 - A",
        "Period 4 - B",
        "Period 5 - A",
        "Period 5 - B",
        "Period 6 - A",
        "Period 6 - B",
        "Period 7 - A",
        "Period 7 - B",
        "Period 8 - A",
        "Period 8 - B",
        "Period 9 - A",
        "Period 9 - B",
    ]

    long_df = pd.melt(
        TWRF_df,
        id_vars=["SA"],
        value_vars=assignment_cols,
        var_name="Period",
        value_name="Assignment",
    )

    TWRF_Times_filename = data["TWRF_Times_filename"]
    TWRF_Times_df = pd.read_csv(TWRF_Times_filename).fillna("")

    long_df = long_df.merge(TWRF_Times_df, on="Period")

    schedule_cols = [
        "Period",
        "Start",
        "End",
        "Assignment",
    ]

    flowables = []

    paragraph = Paragraph(f"School Aide Assignments - Date:___________", styles["Title"])
    flowables.append(paragraph)
    cols = [
        "SA",
        "Start Time",
        "End Time",
        "Assigned School Aide",
    ]
    
    table = return_df_as_table(TWRF_df, cols=cols)
    flowables.append(table)
    flowables.append(PageBreak())

    for SA, assignments_df in long_df.groupby("SA"):
        assignments_df = assignments_df[schedule_cols]
        paragraph = Paragraph(f"TWRF", styles["BodyText"])
        flowables.append(paragraph)

        paragraph = Paragraph(f"{SA}", styles["Title"])
        flowables.append(paragraph)
        paragraph = Paragraph(
            f"Name:______________________ Date:__________", styles["Title"]
        )
        flowables.append(paragraph)

        table = return_df_as_table(assignments_df, cols=schedule_cols)
        flowables.append(table)
        flowables.append(PageBreak())

    output_pdf_filename = f"output/SchoolAideSchedule_TWRF.pdf"

    my_doc = SimpleDocTemplate(
        output_pdf_filename,
        pagesize=letter,
        topMargin=0.5 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        bottomMargin=0.25 * inch,
    )
    my_doc.build(flowables)

    return True


def return_df_as_table(df, cols=None, colWidths=None):
    if cols:
        pass
    else:
        cols = df.columns
    table_data = df[cols].values.tolist()
    table_data.insert(0, cols)
    t = Table(table_data, colWidths=colWidths, repeatRows=1, rowHeights=35)
    t.setStyle(
        TableStyle(
            [
                ("FONTSIZE", (0, 0), (100, 100), 18),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("ALIGN", (0, 0), (100, 100), "CENTER"),
                ("VALIGN", (0, 0), (100, 100), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (100, 100), 10),
                ("RIGHTPADDING", (0, 0), (100, 100), 10),
                ("BOTTOMPADDING", (0, 0), (100, 100), 5),
                ("TOPPADDING", (0, 0), (100, 100), 5),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), (0xD0D0FF, None)),
            ]
        )
    )
    return t


if __name__ == "__main__":
    data = {
        "TWRF_filename": "data/TWRF.csv",
        "TWRF_Times_filename": "data/TWRF-Times.csv",
        "M_filename": "",
    }
    main(data)
