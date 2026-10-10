from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load the embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True},
)

# 2. Example texts
texts = [
    "Large language models can generate unit tests for software.",
    "Automated testing helps developers detect software defects.",
    "Plants need sunlight and water to grow.",
]

# 3. Convert texts to vectors
vectors = embeddings.embed_documents(texts)

# 4. Convert a question to a vector
query = "How can AI help with software testing?"
query_vector = embeddings.embed_query(query)

# 5. Print results
print("Number of vectors:", len(vectors))
print("Vector dimensions:", len(vectors[0]))
print("First 5 numbers:", vectors[0][:5])
print("Query vector dimensions:", len(query_vector))


# 6. Calculate similarity scores
results = []

for text, vector in zip(texts, vectors):
    similarity = sum(
        a * b for a, b in zip(query_vector, vector)
    )

    results.append((text, similarity))

# 7. Sort by similarity (highest first)
results.sort(key=lambda item: item[1], reverse=True)

# 8. Print ranked results
print("\nSimilarity Results:")

for text, score in results:
    print(f"\nScore: {score:.3f}")
    print(f"Text: {text}")