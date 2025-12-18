from langchain_community.vectorstores import FAISS
from src.embeddings.embedder import get_embedding_model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

load_dotenv()

class AssessmentRecommendationEngine:
    def __init__(self, index_path="data/faiss_index"):
        self.embeddings = get_embedding_model()
        try:
            self.vector_store = FAISS.load_local(
                index_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"Loaded FAISS index from {index_path}")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            raise

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=api_key,
                temperature=0.3
            )
        else:
            print("Warning: GEMINI_API_KEY not found. LLM features will be disabled.")
            self.llm = None

    def search(self, query, k=3):
        docs = self.vector_store.similarity_search(query, k=k)
        return docs

    def recommend(self, query):
        retrieved_docs = self.search(query, k=4)
        
        if not retrieved_docs:
            return "I couldn't find any relevant assessments for your request."

        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])

        if self.llm:
            prompt_template = """
            You are an expert consultant for SHL, a global leader in talent acquisition and management.
            Your goal is to recommend the best assessments based on the user's needs.
            
            Use the following context (details about SHL assessments) to answer the user's request.
            If the answer is not in the context, say you don't have enough information.
            
            Context:
            {context}
            
            User Request: {query}
            
            Recommendation:
            """
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "query"]
            )
            
            try:
                chain = prompt | self.llm | StrOutputParser()
                response = chain.invoke({"context": context_text, "query": query})
                return response
            except Exception as e:
                print(f"LLM generation failed (likely rate limit): {e}")
                print("Falling back to raw search results.")
                results = "I couldn't generate a summarized recommendation due to high server load, but here are the most relevant assessments I found:\n\n"
                for i, doc in enumerate(retrieved_docs, 1):
                    results += f"**{i}. {doc.metadata.get('title', 'Unknown Title')}**\n"
                    results += f"{doc.page_content[:300]}...\n\n"
                return results
        
        else:
            results = "Based on your query, here are some relevant assessments:\n"
            for i, doc in enumerate(retrieved_docs, 1):
                results += f"{i}. {doc.metadata.get('title', 'Unknown Title')}\n"
                results += f"   {doc.page_content[:200]}...\n\n"
            return results

if __name__ == "__main__":
    # Test the engine
    engine = AssessmentRecommendationEngine()
    test_query = "I need an assessment for software engineers focusing on coding skills."
    print(f"Query: {test_query}")
    print("-" * 50)
    try:
        recommendation = engine.recommend(test_query)
        print(recommendation)
    except Exception as e:
        print(f"Error during recommendation: {e}")
