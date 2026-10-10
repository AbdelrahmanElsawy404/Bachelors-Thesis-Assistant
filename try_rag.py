from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer


# 1. Read the PDF
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


# 2. Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# 3. Split documents based on tokens
text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer,
    chunk_size=220,
    chunk_overlap=40,
)

chunks = text_splitter.split_documents(documents)


# 4. Count tokens in each chunk
token_lengths = []

for chunk in chunks:
    tokens = tokenizer.encode(
        chunk.page_content,
        add_special_tokens=True,
        truncation=False,
    )

    token_lengths.append(len(tokens))


# 5. Print token statistics
print("\n--- Token Statistics ---")

print("Minimum tokens:", min(token_lengths))
print("Maximum tokens:", max(token_lengths))

over_limit = sum(
    1 for length in token_lengths if length > 256
)

print("Chunks exceeding 256 tokens:", over_limit)

print("\nFirst 3 chunks token lengths:")

for index, length in enumerate(token_lengths[:3]):
    print(f"Chunk {index + 1}: {length} tokens")


# 6. Print document and chunk statistics
print("\nNumber of pages:", len(documents))
print("Number of chunks:", len(chunks))


# 7. Inspect the first 3 chunks
for index, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {index + 1}")
    print("Length:", len(chunk.page_content))
    print("Metadata:", chunk.metadata)


# 8. Print the complete text of the first 2 chunks
for index, chunk in enumerate(chunks[:2]):
    print(f"\n--- Full text of Chunk {index + 1} ---")
    print(chunk.page_content)