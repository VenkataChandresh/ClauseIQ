import fitz


def extract_text_from_pdf(file_path: str) -> dict:
    document = fitz.open(file_path)

    full_text = ""

    for page_number in range(len(document)):
        page = document[page_number]
        full_text += page.get_text()

    page_count = len(document)
    document.close()

    return {
        "page_count": page_count,
        "text": full_text,
        "text_length": len(full_text),
    }
