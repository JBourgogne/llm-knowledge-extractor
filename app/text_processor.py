import re
from collections import Counter
from typing import List

def extract_keywords(text: str, n: int = 3) -> List[str]:
    """
    Extract the n most frequent nouns/keywords from text.
    Simple implementation without heavy NLP dependencies.
    """
    # Convert to lowercase for processing
    text_lower = text.lower()
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what',
        'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every',
        'both', 'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own',
        'same', 'so', 'than', 'too', 'very', 'just', 'if', 'then', 'else'
    }
    
    # Extract words (alphanumeric, length > 3)
    words = re.findall(r'\b[a-z]+\b', text_lower)
    
    # Filter out stop words and short words
    meaningful_words = [
        word for word in words 
        if len(word) > 3 and word not in stop_words
    ]
    
    # Count frequencies
    word_counts = Counter(meaningful_words)
    
    # Return top n words
    top_words = [word for word, _ in word_counts.most_common(n)]
    
    # If we don't have enough words, return what we have
    return top_words if top_words else ["no", "keywords", "found"][:n]