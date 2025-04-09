from fpdf import FPDF
from pathlib import Path

class PDF(FPDF):
    # def header(self):
    #     # Rendering logo:
    #     self.image("../docs/fpdf2-logo.png", 10, 8, 33)
    #     # Setting font: helvetica bold 15
    #     self.set_font("helvetica", "B", 15)
    #     # Moving cursor to the right:
    #     self.cell(80)
    #     # Printing title:
    #     self.cell(30, 10, "Title", border=1, align="C")
    #     # Performing a line break:
    #     self.ln(20)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def set_header(self, week=None, semester=None, session=None):
        self.ln()
        # Page header section
        self.image(str(Path(__file__).resolve().parent.parent / 'logo.png'), x=20, y=2)
        self.set_font("Times", "B", 12)
        self.set_y(7)
        # self.set_x(128.5)
        self.cell(0, 5, "BABCOCK UNIVERSITY", 0, 1, 'C')
        self.set_font("Times", "B", 12)
        self.set_y(12)
        # self.set_x(111.5)
        self.cell(0, 5, "ACADEMIC PLANNING DEPARTMENT", 0, 1, "C")
        self.set_font("Times", "B", 12)
        self.set_y(17)
        # self.set_x(113.5)
        self.cell(0, 5, "CLASSROOM MONITORING REPORT", 0, 1, "C")
        self.set_y(24.5)
        # self.set_x(113.5)
        if week is None:
            self.cell(0, 5, f"{session}, {semester} Semester Report", 0, 1, "C")
        else:
            self.cell(0, 5, f"WEEK {week}", 0, 1, "C")

    def display_kpi(self):
        self.image(str(Path(__file__).resolve().parent.parent / 'total_mon.png'), x=20, y=33)
        self.image(str(Path(__file__).resolve().parent.parent / 'total_held.png'), x=111.5, y=33)
        self.image(str(Path(__file__).resolve().parent.parent / 'total_not_held.png'), x=200, y=33)

    def display_by_school(self):
        self.image(str(Path(__file__).resolve().parent.parent / 'monitored_by_school.png'), x=15, y=72)

        self.add_page()
        self.image(str(Path(__file__).resolve().parent.parent / 'monitored_by_day.png'), x=15, y=10)
        # self.output(Path(__file__).resolve().parent.parent / "pdf-with-image.pdf")

    def unheld(self, df, title=None, sec=False):
        # table title
        self.set_x(12)
        self.set_y(10)

        # if sec:
        #     self.set_y(35)
        # else:
        #     self.set_y(10)

        self.set_font("Times", "B", 12)
        self.cell(62, 10, title, 0, 0, "L")

        self.ln()

        df = df.sort_values(by='day_num')
        df = df.drop("day_num", axis=1)

        table_header = df.columns

        # print(f"Table header: {table_header}")

        if sec:
            w = [40.0, 30.0, 25.0, 58.0,28.0, 15.0, 18.0, 55.0]
        else:
            w = [40.0, 25.0, 62.0,28.0, 15.0, 45.0, 55.0]

        height = 7

        self.set_x(10)
        self.set_font("Times", "B", 12)
        for x in range(0, 8):
            self.cell(w[x], height, table_header[x], 0, 0, "L")

        self.set_x(12)
        self.set_font("Times", "", 10)
        self.ln()
        for _, row in df.iterrows():
            self.cell(40, height, str(row["Date & Time"]), 0, 0, "L")
            self.cell(30, height, str(row["Day"]), 0, 0, "L")
            self.cell(25, height, str(row["Class time"]), 0, 0, "C")
            self.cell(58, height, str(row["Lecturer Name"]), 0, 0, "L")
            self.cell(28, height, str(row["Course Code"]), 0, 0, "L")
            self.cell(15, height, str(row["Week"]), 0, 0, "C")
            if sec:
                self.cell(18, height, str(row["School"]), 0, 0, "L")
                self.cell(55, height, str(row["Comment"]), 0, 1, "L")
            else:
                self.cell(45, height, str(row["Reporter"]), 0, 0, "L")
                self.cell(55, height, str(row["Observation"]), 0, 1, "L")
            # self.ln()

        # print(f"Current Y position: {self.get_y()}")
        # if sec:
        #     self.output(Path(__file__).resolve().parent.parent / "weekly monitoring report - sec.pdf")
    
    def display_by_agent(self):
        if self.get_y() > 40:
            self.add_page()
        
        self.ln()
        self.image(str(Path(__file__).resolve().parent.parent / 'monitored_by_agent.png'), x=15, y=self.get_y())

        self.output(Path(__file__).resolve().parent.parent / "weekly monitoring report.pdf")

    def report_download(self,pdf_b64, name, sec=False):
        
        if sec:
            href = f'<button type="button" class="green"><a href="data:application/pdf;base64, {pdf_b64}" download="{name}.pdf">Download Sec Report</a></button>'
        else:
            href = f'<button type="button" class="green"><a href="data:application/pdf;base64, {pdf_b64}" download="{name}.pdf">Download Report</a></button>'

        return href