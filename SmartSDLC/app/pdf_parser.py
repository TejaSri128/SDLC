import PyPDF2
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text = ""
        for page_num in range(len(pdf_reader.pages)):
            try:
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text() + "\n"
            except:
                continue
        return extracted_text.strip() or "No text"
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_file(file_bytes: bytes, file_type: str) -> str:
    if file_type.lower() == "pdf":
        return extract_text_from_pdf(file_bytes)
    else:
        try:
            return file_bytes.decode(errors="ignore")
        except:
            return "Error"
