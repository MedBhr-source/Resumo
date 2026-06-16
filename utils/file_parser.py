import PyPDF2 
import docx
import os

class FileParser :
    @staticmethod
    def extract_text(file_path) :
        ext = os.path.splitext(file_path)[1].lower() # [1] for extension 

        try:
            if ext == '.pdf' :
                return FileParser._parse_pdf(file_path) , None
            elif ext == '.docx' :
                return FileParser._parse_docx(file_path) , None
            elif ext == '.txt' :
                return FileParser._parse_txt(file_path) , None
            else :
                return None , f"Unsupported file format: {ext} , only .pdf, .docx, and .txt are supported."
        
        except Exception as exp :
            return None , f"Error parsing file: {str(exp)}"
        
    @staticmethod
    def _parse_pdf(file_path):
        text = ""
        with open(file_path , 'rb') as f :
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages :
                text += page.extract_text()  + "\n" 
        return text.strip()     # Remove trailing newline

    @staticmethod
    def _parse_docx(file_path):
        doc = docx.Document(file_path)
        full_txt = [para.text for para in doc.paragraphs]
        return "\n".join(full_txt).strip()  # Join paragraphs and remove trailing newline
    
    @staticmethod
    def _parse_txt(file_path):
        with open(file_path, "r", encoding="utf-8") as f :
            return f.read().strip()  # Read entire file and remove trailing newline
        



