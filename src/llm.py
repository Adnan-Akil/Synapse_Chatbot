"""LLM module for generating final answers based on retrieved documents"""

from config.config import Config
from langchain_groq import ChatGroq

from typing import List
from langchain_core.documents import Document

def final_answer(retrieved_docs: List[Document], user_query: str) -> str:
    """Generate a final answer using the retrieved documents and user query"""
    llm_model = ChatGroq(
        model=Config.LLM_MODEL_NAME, temperature=0.3, api_key=Config.GROQ_API_KEY
    )

    prompt = f"""
  You are a highly reliable, context‑driven assistant. Your goal is to answer user questions **only** using the information in the retrieved context.  

  1. ROLE  
    • Use the provided CONTEXT to craft your answer.  
    • Never introduce external information, assumptions, or hallucinations.  

  2. PROCESS  
    • **Step 1:** Check if the CONTEXT contains explicit information answering the question.  
    • **Step 2:** If it does, extract the relevant passages, and present them.  
    • **Step 3:** If the CONTEXT is incomplete or ambiguous, ask a clarifying question or say:  
      “I’m sorry, but the context doesn’t give enough information to answer that. Could you clarify or provide more details?”  

  3. STYLE & FORMAT  
    • Use a one‑line heading summarizing your answer.  
    • Use bullet points (one per line) for each distinct fact or step.  
    • Keep each bullet concise (1–2 sentences).  

  4. FORMAT
    If context is sufficient, provide a clear, structured, or conversational answer, optionally referencing document titles or sections if helpful. Use bullets, short paragraphs, or quotes as needed — whichever feels most appropriate.

    If context is lacking, politely explain that there’s not enough information to answer confidently. Encourage clarification or suggest possible directions.

    Avoid overly formal tone unless required. Keep it natural, helpful, and direct.

  ---  
  **CONTEXT:**  
  {retrieved_docs}

  **USER QUESTION:**  
  {user_query}

  """

    try:
        llm_response = llm_model.invoke(prompt)
        return llm_response.content
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}. Please check your API key and internet connection."
