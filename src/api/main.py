from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.rag.engine import AssessmentRecommendationEngine
import uvicorn

app = FastAPI(title="SHL Assessment Recommendation Engine")

try:
    engine = AssessmentRecommendationEngine()
except Exception as e:
    print(f"Failed to initialize RAG engine: {e}")
    engine = None

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>SHL Assessment Recommender</title>
            <style>
                body { font-family: Segoe UI, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; background-color: #f5f5f5; }
                .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; margin-top: 0; }
                textarea { width: 100%; height: 100px; margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: inherit; box-sizing: border-box;}
                button { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: background 0.2s; }
                button:hover { background: #0056b3; }
                #result { margin-top: 25px; white-space: pre-wrap; background: #f8f9fa; padding: 20px; border-radius: 5px; border-left: 4px solid #007bff; display: none; }
                .loading { color: #666; font-style: italic; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SHL Assessment Recommendation Engine</h1>
                <p>Describe the role or skills you are looking for to get AI-powered assessment recommendations.</p>
                
                <textarea id="query" placeholder="Example: I need a python coding test for a senior backend developer with SQL skills..."></textarea>
                <button onclick="getRecommendation()">Get Recommendations</button>
                
                <div id="result"></div>
            </div>

            <script>
                async function getRecommendation() {
                    const query = document.getElementById('query').value;
                    if (!query) return;
                    
                    const resultDiv = document.getElementById('result');
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'loading';
                    resultDiv.textContent = "Analyzing requirements and searching catalog...";
                    
                    try {
                        const response = await fetch('/recommend', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ query: query })
                        });
                        const data = await response.json();
                        resultDiv.className = '';
                        if (data.recommendation) {
                            resultDiv.textContent = data.recommendation;
                        } else {
                            resultDiv.textContent = "Error: " + (data.detail || "Unknown error");
                        }
                    } catch (e) {
                        resultDiv.className = '';
                        resultDiv.textContent = "Network Error: " + e;
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/recommend")
def get_recommendation(request: QueryRequest):
    if not engine:
        raise HTTPException(status_code=503, detail="Recommendation engine is not initialized.")
    
    try:
        result = engine.recommend(request.query)
        return {"recommendation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)
