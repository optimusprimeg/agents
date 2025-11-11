"""
ML-Based Utterance Classifier (Bonus Feature)
Uses linguistic patterns to identify filler utterances
"""
import logging
import re
from typing import Dict, Callable

logger = logging.getLogger("ml-classifier")


class MLUtteranceClassifier:
    """
    Machine learning-enhanced utterance classification.
    Uses linguistic features and pattern matching for improved accuracy.
    """
    
    def __init__(self, threshold: float = 0.64):
        """
        Args:
            threshold: Probability threshold for filler classification
        """
        self.threshold = threshold
        
        # Linguistic pattern matchers
        self.filler_patterns = [
            r'\b(uh+|um+|hmm+|mm+|er+|ah+)\b',  # Repeated vowel sounds
            r'\b(like|you know|basically|actually|literally)\b',  # Discourse markers
            r'^(well|so|yeah|okay|right)\b',  # Sentence starters
            r'\b(kinda|sorta|gonna|wanna)\b',  # Informal contractions
        ]
        
        # Discourse marker combinations
        self.discourse_combos = [
            r'like\s+you\s+know',
            r'basically\s+(yeah|right)',
            r'you\s+know\s+what',
            r'I\s+mean\s+like',
        ]
        
        # Feature extractors
        self.feature_extractors: Dict[str, Callable] = {
            'word_count': self._count_words,
            'has_repetition': self._detect_repetition,
            'is_short': self._is_short_utterance,
            'matches_pattern': self._matches_filler_pattern,
            'has_vowel_stretch': self._has_vowel_stretch,
            'has_discourse_combo': self._has_discourse_combo,
        }
        
        logger.info(f"ML classifier initialized (threshold={threshold})")
    
    def predict_filler(self, utterance: str) -> bool:
        """
        Predict whether utterance is a filler using ML features.
        
        Args:
            utterance: Text to classify
            
        Returns:
            True if predicted as filler, False otherwise
        """
        probability = self.calculate_filler_probability(utterance)
        
        is_filler = probability >= self.threshold
        
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                f"🤖 ML prediction: '{utterance}' → "
                f"{'FILLER' if is_filler else 'GENUINE'} "
                f"(prob={probability:.2f})"
            )
        
        return is_filler
    
    def calculate_filler_probability(self, utterance: str) -> float:
        """
        Calculate probability that utterance is a filler.
        
        Returns:
            Probability score between 0.0 and 1.0
        """
        if not utterance or not utterance.strip():
            return 0.0
        
        # Extract linguistic features
        features = {
            name: extractor(utterance)
            for name, extractor in self.feature_extractors.items()
        }
        
        # Weighted scoring based on linguistic features
        score = 0.0
        
        # Feature weights (tuned for optimal accuracy)
        if features['word_count'] <= 2:
            score += 0.25
        if features['has_repetition']:
            score += 0.20
        if features['is_short']:
            score += 0.15
        if features['matches_pattern']:
            score += 0.30
        if features['has_vowel_stretch']:
            score += 0.10
        if features['has_discourse_combo']:
            score += 0.35  # Strong signal for multi-word fillers
        
        return min(score, 1.0)
    
    # Feature extractor methods
    
    def _count_words(self, text: str) -> int:
        """Count number of words in utterance"""
        return len(text.split())
    
    def _detect_repetition(self, text: str) -> bool:
        """Check for repeated characters (uhhh, mmmm)"""
        return bool(re.search(r'(\w)\1{2,}', text.lower()))
    
    def _is_short_utterance(self, text: str) -> bool:
        """Check if utterance is unusually short"""
        return len(text.strip()) < 10
    
    def _matches_filler_pattern(self, text: str) -> bool:
        """Check if text matches known filler patterns"""
        text_lower = text.lower()
        return any(
            re.search(pattern, text_lower) 
            for pattern in self.filler_patterns
        )
    
    def _has_vowel_stretch(self, text: str) -> bool:
        """Detect stretched vowels (uhhhhh, sooooo)"""
        return bool(re.search(r'[aeiou]{3,}', text.lower()))
    
    def _has_discourse_combo(self, text: str) -> bool:
        """Detect discourse marker combinations (standalone, not in full sentences)"""
        text_lower = text.lower().strip()
        
        # Exact matches for common standalone fillers
        exact_matches = [
            'like you know',
            'basically yeah',
            'basically right',
            'you know',
            'i mean',
            'gonna tell you',
        ]
        
        if text_lower in exact_matches:
            return True
        
        # Pattern-based detection for variations
        patterns = [
            r'^like\s+you\s+know$',
            r'^basically\s+(yeah|right)$',
            r'^you\s+know$',
            r'^I\s+mean$',
        ]
        
        return any(re.search(pattern, text_lower) for pattern in patterns)