import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

# Document type keywords and patterns
CLASSIFICATION_RULES = {
    'Invoice': {
        'keywords': [
            'invoice', 'bill', 'amount due', 'payment due', 'total amount',
            'invoice number', 'inv#', 'billing', 'charge', 'payment terms',
            'due date', 'remit to', 'pay to', 'billing address'
        ],
        'patterns': [
            r'invoice\s*#?\s*\d+',
            r'total\s*amount?\s*:?\s*\$?\d+',
            r'amount\s*due\s*:?\s*\$?\d+',
            r'payment\s*due\s*:?\s*\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}'
        ],
        'weight': 1.0
    },
    'Resume': {
        'keywords': [
            'resume', 'curriculum vitae', 'cv', 'experience', 'education',
            'skills', 'objective', 'summary', 'employment', 'work history',
            'qualifications', 'achievements', 'references', 'contact',
            'phone', 'email', 'address', 'linkedin', 'portfolio'
        ],
        'patterns': [
            r'objective\s*:',
            r'education\s*:',
            r'experience\s*:',
            r'skills\s*:',
            r'employment\s*history',
            r'\d{4}\s*-\s*\d{4}',  # Date ranges
            r'bachelor|master|phd|degree',
            r'university|college'
        ],
        'weight': 1.0
    },
    'Contract': {
        'keywords': [
            'contract', 'agreement', 'terms and conditions', 'whereas',
            'party', 'parties', 'obligations', 'hereby', 'executed',
            'witness', 'signature', 'effective date', 'termination',
            'breach', 'liability', 'indemnity', 'governing law'
        ],
        'patterns': [
            r'this\s+agreement',
            r'party\s+of\s+the\s+first\s+part',
            r'whereas',
            r'hereby\s+agree',
            r'in\s+witness\s+whereof',
            r'effective\s+date',
            r'terms?\s+and\s+conditions'
        ],
        'weight': 1.0
    },
    'Bank Statement': {
        'keywords': [
            'bank statement', 'account statement', 'balance', 'transaction',
            'deposit', 'withdrawal', 'checking', 'savings', 'account number',
            'routing number', 'beginning balance', 'ending balance',
            'statement period', 'bank', 'credit', 'debit'
        ],
        'patterns': [
            r'account\s*number\s*:?\s*\d+',
            r'beginning\s*balance',
            r'ending\s*balance',
            r'statement\s*period',
            r'transaction\s*date',
            r'\$\d+\.\d{2}',  # Currency amounts
            r'balance\s*:?\s*\$?\d+'
        ],
        'weight': 1.0
    }
}

def classify_document(text: str) -> Dict[str, any]:
    """
    Classify document based on content using keyword matching and pattern recognition.
    
    Args:
        text: Extracted text from document
        
    Returns:
        Dictionary containing classification results
    """
    if not text or not text.strip():
        return {
            'type': 'Other',
            'confidence': 0.0,
            'scores': {},
            'reasoning': 'No text content found'
        }
    
    text_lower = text.lower()
    scores = {}
    reasoning_details = {}
    
    for doc_type, rules in CLASSIFICATION_RULES.items():
        score = calculate_type_score(text_lower, text, rules)
        scores[doc_type] = score
        reasoning_details[doc_type] = get_matching_elements(text_lower, text, rules)
    
    # Find the best match
    best_type = max(scores.keys(), key=lambda k: scores[k])
    best_score = scores[best_type]
    
    # Apply confidence thresholds
    if best_score < 0.3:
        classification_type = 'Other'
        confidence = 0.5  # Low confidence for "Other"
    else:
        classification_type = best_type
        confidence = min(best_score, 1.0)
    
    return {
        'type': classification_type,
        'confidence': round(confidence, 2),
        'scores': {k: round(v, 2) for k, v in scores.items()},
        'reasoning': reasoning_details.get(classification_type, [])
    }

def calculate_type_score(text_lower: str, original_text: str, rules: Dict) -> float:
    """Calculate score for a specific document type."""
    keyword_score = 0
    pattern_score = 0
    
    # Check keywords
    keywords_found = 0
    for keyword in rules['keywords']:
        if keyword.lower() in text_lower:
            keywords_found += 1
    
    if rules['keywords']:
        keyword_score = (keywords_found / len(rules['keywords'])) * 0.7
    
    # Check patterns
    patterns_found = 0
    for pattern in rules.get('patterns', []):
        if re.search(pattern, original_text, re.IGNORECASE):
            patterns_found += 1
    
    if rules.get('patterns'):
        pattern_score = (patterns_found / len(rules['patterns'])) * 0.3
    
    total_score = (keyword_score + pattern_score) * rules.get('weight', 1.0)
    return total_score

def get_matching_elements(text_lower: str, original_text: str, rules: Dict) -> List[str]:
    """Get list of matching keywords and patterns for reasoning."""
    matches = []
    
    # Find matching keywords
    for keyword in rules['keywords']:
        if keyword.lower() in text_lower:
            matches.append(f"Keyword: '{keyword}'")
    
    # Find matching patterns
    for pattern in rules.get('patterns', []):
        match = re.search(pattern, original_text, re.IGNORECASE)
        if match:
            matches.append(f"Pattern: '{match.group()}'")
    
    return matches[:5]  # Return top 5 matches for brevity

def get_document_types() -> List[str]:
    """Get list of available document types."""
    return list(CLASSIFICATION_RULES.keys()) + ['Other']

def update_classification_rules(doc_type: str, keywords: List[str], patterns: List[str] = None):
    """Update classification rules for a document type (for manual tuning)."""
    if patterns is None:
        patterns = []
    
    CLASSIFICATION_RULES[doc_type] = {
        'keywords': keywords,
        'patterns': patterns,
        'weight': 1.0
    }
    
    logger.info(f"Updated classification rules for {doc_type}")
