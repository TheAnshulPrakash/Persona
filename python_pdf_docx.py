  # PyMuPDF
import fitz
def extract_pdf_text(path):
    
    doc = fitz.open(path)
    data="\n".join(page.get_text("text") for page in doc)
    print(extract_pdf_text(data))
#extract_pdf_text("sample.pdf")

