import os
import subprocess
from fpdf import FPDF
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class PDFWithBorder(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'NITK Surathkal', 0, 0, 'L')
        self.cell(0, 10, '242CS017', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Dept of Civil CV742', 0, 0, 'L')
        self.cell(0, 10, 'CV742', 0, 0, 'R')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_code(self, title, code):
        self.add_page()
        self.chapter_title(title)
        self.chapter_body(code)


def generate_pdf_from_files(directory):
    pdf = PDFWithBorder()

    for root, dirs, files in os.walk(directory):
        if 'Assign' in dirs:
            dirs.remove('Assign')  # Ignore 'Assign' directory

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                    formatted_code = highlight(code, PythonLexer(), HtmlFormatter())
                    pdf.add_code(file, code)

                    # Generate output by running the Python file
                    try:
                        output = subprocess.check_output(['python', file_path], stderr=subprocess.STDOUT).decode('utf-8')
                    except subprocess.CalledProcessError as e:
                        output = e.output.decode('utf-8')

                    pdf.chapter_body("Output:\n" + output)

    pdf_file_path = os.path.join(directory, 'output.pdf')
    pdf.output(pdf_file_path)
    print(f'PDF generated at {pdf_file_path}')


# Specify the directory containing the Python files
directory = './'
generate_pdf_from_files(directory)
