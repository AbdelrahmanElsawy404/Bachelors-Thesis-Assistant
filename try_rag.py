from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer
from sentence_transformers import CrossEncoder


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


# 2. Load tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(model_name)


# 3. Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer,
    chunk_size=220,
    chunk_overlap=40,
)

chunks = text_splitter.split_documents(documents)


# 4. Check token lengths
token_lengths = []

for chunk in chunks:
    tokens = tokenizer.encode(
        chunk.page_content,
        add_special_tokens=True,
        truncation=False,
    )

    token_lengths.append(len(tokens))

over_limit = sum(
    1 for length in token_lengths if length > 256
)

print("Number of pages:", len(documents))
print("Number of chunks:", len(chunks))
print("Maximum tokens:", max(token_lengths))
print("Chunks exceeding 256 tokens:", over_limit)

if over_limit > 0:
    raise ValueError("Some chunks exceed the model token limit.")


# 5. Load embeddings model
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    encode_kwargs={"normalize_embeddings": True},
)


# 6. Convert chunks to vectors
texts = [chunk.page_content for chunk in chunks]

vectors = embeddings.embed_documents(texts)

print("\nNumber of vectors:", len(vectors))
print("Vector dimensions:", len(vectors[0]))


# 7. Convert question to vector
query = "Which software testing tasks most commonly use large language models?"

query_vector = embeddings.embed_query(query)


# 8. Calculate similarity
results = []

for chunk, vector in zip(chunks, vectors):
    similarity = sum(
        a * b for a, b in zip(query_vector, vector)
    )

    results.append((chunk, similarity))


# 9. Sort results
results.sort(
    key=lambda item: item[1],
    reverse=True,
)


# 10. Print top 3 results
print("\n--- Top 3 Search Results ---")

for rank, (chunk, score) in enumerate(results[:3], start=1):
    print(f"\n--- Result {rank} ---")
    print(f"Similarity: {score:.3f}")
    print(f"Source: {chunk.metadata['source']}")
    print(f"Page: {chunk.metadata['page'] + 1}")
    print("Text:")
    print(chunk.page_content)


# 11. Select top 20 candidates
candidates = results[:20]


# 12. Load the reranker model
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


# 13. Prepare query-document pairs
pairs = [
    (query, chunk.page_content)
    for chunk, similarity in candidates
]


# 14. Predict reranking scores
rerank_scores = reranker.predict(pairs)


# 15. Combine candidates with reranking scores
reranked_results = []

for (chunk, similarity), rerank_score in zip(
    candidates, rerank_scores
):
    reranked_results.append(
        (chunk, similarity, float(rerank_score))
    )


# 16. Sort by reranking score
reranked_results.sort(
    key=lambda item: item[2],
    reverse=True,
)


# 17. Print top 3 reranked results
print("\n--- Top 3 Reranked Results ---")

for rank, (chunk, similarity, rerank_score) in enumerate(
    reranked_results[:3], start=1
):
    print(f"\n--- Reranked Result {rank} ---")
    print(f"Rerank score: {rerank_score:.3f}")
    print(f"Original similarity: {similarity:.3f}")
    print(f"Source: {chunk.metadata['source']}")
    print(f"Page: {chunk.metadata['page'] + 1}")
    print("Text:")
    print(chunk.page_content)