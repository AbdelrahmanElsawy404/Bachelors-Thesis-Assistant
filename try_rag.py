from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



# =========================
# 1. Read the File
# =========================
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


# =========================
# 2. Split the File into Chunks
# =========================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

chunks = text_splitter.split_documents(documents)




print("Number of pages:", len(documents))
print("Number of chunks:", len(chunks))

for index, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {index + 1}")
    print("Length:", len(chunk.page_content))
    print("Metadata:", chunk.metadata)

for index, chunk in enumerate(chunks[:2]):
    print(f"\n--- Full text of Chunk {index + 1} ---")
    print(chunk.page_content)