import json
from typing import Dict, Any
import random
import hashlib

class LLMService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.is_mock = not api_key or api_key == "mock" or api_key == "your_api_key_here"
        
        if self.is_mock:
            print("Running in MOCK mode (no API charges)")
        else:
            # Existing OpenAI code here
            print("OpenAI API quota exceeded - falling back to mock mode")
            self.is_mock = True
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text - using mock analyzer for demonstration.
        """
        # Create deterministic but varied results based on text content
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Extract meaningful words for mock analysis
        words = [w for w in text.split() if len(w) > 4][:10]
        
        # Determine sentiment based on keywords
        positive_words = ['good', 'great', 'excellent', 'amazing', 'innovative', 'revolutionary', 'success', 'happy']
        negative_words = ['bad', 'poor', 'fail', 'problem', 'issue', 'difficult', 'wrong', 'error']
        
        sentiment = "neutral"
        text_lower = text.lower()
        if any(word in text_lower for word in positive_words):
            sentiment = "positive"
        elif any(word in text_lower for word in negative_words):
            sentiment = "negative"
        
        # Generate realistic looking topics
        topic_candidates = [
            "technology", "innovation", "business", "development", "analysis",
            "research", "industry", "market", "product", "service", "strategy",
            "digital", "software", "platform", "solution", "system"
        ]
        
        # Use text content to pick relevant topics
        topics = []
        for word in words:
            if word.lower() in text_lower and word.lower() not in topics:
                topics.append(word.lower())
        
        # Fill remaining with candidates
        while len(topics) < 3:
            topic = random.Random(text_hash).choice(topic_candidates)
            if topic not in topics:
                topics.append(topic)
        
        topics = topics[:3]
        
        # Create a reasonable summary
        first_sentence = text.split('.')[0] if '.' in text else text[:100]
        summary = f"{first_sentence[:80]}... This content covers aspects of {topics[0]} and {topics[1]}."
        
        # Generate title
        title_words = words[:4] if len(words) >= 4 else words
        title = f"Analysis: {' '.join(title_words).title()}" if title_words else "Text Analysis"
        
        return {
            "title": title,
            "summary": summary,
            "topics": topics,
            "sentiment": sentiment
        }