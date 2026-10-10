from pypdf import PdfReader
from langchain_core.documents import Document


file_path = "docs/ai_software_testing.pdf"
reader = PdfReader(file_path)
documents = []



for page_number, page in enumerate(reader.pages):
    text = page.extract_text() or ""

    document = Document(
        page_content=text,
        metadata={
            "source": file_path,
            "page": page_number,
            "total_pages": len(reader.pages),
        },
    )

    documents.append(document)

print("Number of pages:", len(documents))

print("\nFirst 500 characters:")
print(documents[0].page_content[:500])

print("\nFirst page metadata:")
print(documents[0].metadata)