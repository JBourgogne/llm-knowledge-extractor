# LLM Knowledge Extractor

A FastAPI-based service that analyzes text using LLM to extract summaries and structured metadata.

## Setup and Run Instructions

Clone the repository

git clone <repository-url>
cd llm-knowledge-extractor

Create virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Configure environment

# Copy .env.example or create .env file
# Add OPENAI_API_KEY=your_key_here (or use "mock" for testing)

Run the server

uvicorn app.main:app --reload


Access the API

API endpoint: http://localhost:8000
Interactive docs: http://localhost:8000/docs
Alternative docs: http://localhost:8000/redoc


API Endpoints
POST /analyze
Analyze text and extract structured data.
Request:
json{
  "text": "Your text content here..."
}
Response:
json{
  "id": 1,
  "summary": "1-2 sentence summary",
  "metadata": {
    "title": "Extracted title",
    "topics": ["topic1", "topic2", "topic3"],
    "sentiment": "positive",
    "keywords": ["keyword1", "keyword2", "keyword3"]
  }
}

GET /search?topic=xyz
Search stored analyses by topic/keyword.

POST /analyze_batch
Process multiple texts in a single request (bonus feature).


Design Choices
Built with FastAPI for rapid API development with automatic documentation and validation. SQLite provides zero-configuration persistence perfect for prototypes. Implemented a mock LLM service to enable testing without API costs while maintaining the same interface for easy swapping with real OpenAI/Claude APIs. JSON column storage allows flexible metadata schema evolution without migrations. Local keyword extraction using simple frequency analysis avoids heavy NLP dependencies while providing accurate results.
Trade-offs

Used mock LLM for demonstration to avoid API costs, but architecture supports real LLM with just an API key change
Simplified keyword extraction without POS tagging to minimize dependencies and setup time
SQLite instead of PostgreSQL for easier setup, though less suitable for production scale
No authentication/rate limiting to focus on core functionality within time constraints