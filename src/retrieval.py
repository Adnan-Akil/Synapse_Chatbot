"""Retrieval module for handling document retrieval and reranking"""

from config.config import Config
from langchain_classic.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from langchain_core.documents import Document



llm_model = ChatGroq(model=Config.LLM_MODEL_NAME, temperature=0.3, api_key=Config.GROQ_API_KEY)

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
)
vectordb = Chroma(persist_directory=None, embedding_function=embedding_model)

encoder_model = HuggingFaceCrossEncoder(
    model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", model_kwargs={"device": "cpu"}
)
reranker = CrossEncoderReranker(model=encoder_model, top_n=15)



def retrieve_similar_docs(user_query_text: str) -> List[Document]:
    """Retrieve and rerank similar documents based on the user query"""
    base_retriever = vectordb.as_retriever(
        search_type="mmr", search_kwargs={"k": 35, "fetch_k": 80, "lambda_mult": 0.3}
    )

    multi_query = MultiQueryRetriever.from_llm(retriever=base_retriever, llm=llm_model)

    all_candidate_docs = multi_query.invoke(user_query_text)
    unique_docs = list({doc.page_content: doc for doc in all_candidate_docs}.values())
    reranked_docs = reranker.compress_documents(unique_docs, user_query_text)

    relevance_threshold = 0.075

    source_scores = {}
    for doc in reranked_docs:
        source = doc.metadata.get("source", "unknown")
        score = doc.metadata.get("score", 0.0)
        if score > relevance_threshold:
            if source not in source_scores or score > source_scores[source][1]:
                source_scores[source] = (doc, score)

    final_docs = []
    seen_sources = set()
    for source, (doc, score) in source_scores.items():
        final_docs.append(doc)
        seen_sources.add(source)

    for doc in reranked_docs:
        if len(final_docs) >= 15:
            break
        if doc not in final_docs:
            final_docs.append(doc)

    return final_docs
