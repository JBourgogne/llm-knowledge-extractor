import json
from typing import Dict, Any
import os

class LLMService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.is_mock = not api_key or api_key == "mock" or api_key == "your_api_key_here"
        
        if not self.is_mock:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key)
                # Test the API key with a minimal request
                self.client.models.list()
            except Exception as e:
                print(f"Warning: OpenAI initialization failed: {e}")
                print("Falling back to mock mode")
                self.is_mock = True
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text - uses mock data if no API key is provided or if API fails.
        """
        if self.is_mock:
            # Return mock data for testing
            words = text.split()[:5]
            return {
                "title": f"Analysis of {' '.join(words[:3])}..." if len(words) > 0 else "Text Analysis",
                "summary": f"This text discusses {words[0] if words else 'various topics'} and related concepts. The content appears to be informative.",
                "topics": [
                    words[0].lower() if len(words) > 0 else "general",
                    words[1].lower() if len(words) > 1 else "content", 
                    words[2].lower() if len(words) > 2 else "analysis"
                ],
                "sentiment": "neutral"
            }
        
        # Real OpenAI implementation
        try:
            from openai import OpenAI
            
            prompt = f"""
            Analyze the following text and return a JSON object with these exact fields:
            - "title": a short title for the text (or null if not applicable)
            - "summary": a 1-2 sentence summary
            - "topics": an array of exactly 3 key topics
            - "sentiment": one of "positive", "neutral", or "negative"
            
            Text to analyze:
            {text[:2000]}
            
            Return ONLY valid JSON, no additional text or formatting.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that returns only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Clean up the response if needed
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            
            result = json.loads(result_text.strip())
            
            # Ensure all required fields exist
            if "topics" not in result or not isinstance(result["topics"], list):
                result["topics"] = ["general", "content", "analysis"]
            if len(result["topics"]) < 3:
                result["topics"].extend(["general"] * (3 - len(result["topics"])))
            elif len(result["topics"]) > 3:
                result["topics"] = result["topics"][:3]
            
            if "sentiment" not in result or result["sentiment"] not in ["positive", "neutral", "negative"]:
                result["sentiment"] = "neutral"
            
            if "summary" not in result:
                result["summary"] = "Summary not available"
            
            if "title" not in result:
                result["title"] = "Untitled Analysis"
                
            return result
            
        except Exception as e:
            print(f"Error in LLM analysis: {e}")
            # Fallback to mock data if API fails
            words = text.split()[:5]
            return {
                "title": "Analysis Failed - Using Fallback",
                "summary": "Analysis could not be completed using the LLM. This is fallback data.",
                "topics": ["error", "fallback", "analysis"],
                "sentiment": "neutral"
            }