"""
Smart Voice Interruption Handler
Advanced filtering system to prevent false agent interruptions from background sounds
"""
import logging
import os
from typing import Set, Dict, Optional

logger = logging.getLogger("voice-interrupt-handler")


class SmartVoiceInterruptionHandler:
    """
    Intelligent voice interruption management system.
    
    Prevents false agent interruptions caused by conversational fillers
    and background utterances while preserving genuine user interruptions.
    """
    
    # Common utterances to suppress
    BLOCKED_UTTERANCES = {
        "uh", "uhh", "um", "umm", "hmm", "hm",
        "haan", "yeah", "mhm", "mm", "mmm", 
        "err", "ah", "oh", "erm", "uh-huh"
    }
    
    def __init__(
        self, 
        blocked_phrases: Optional[Set[str]] = None,
        minimum_confidence: float = 0.5,
        debug_mode: bool = True,
        use_ml_enhancement: bool = False
    ):
        """
        Initialize the smart voice interruption handler.
        
        Args:
            blocked_phrases: Custom set of phrases to block
            minimum_confidence: Threshold for ASR confidence (0.0-1.0)
            debug_mode: Enable detailed logging
            use_ml_enhancement: Enable ML-based detection (bonus)
        """
        self.blocked_phrases = blocked_phrases or self._load_config_from_env()
        self.minimum_confidence = minimum_confidence
        self.debug_mode = debug_mode
        self.use_ml_enhancement = use_ml_enhancement
        
        # Metrics tracking
        # Metrics tracking
        self._metrics = {
            "suppressed_interrupts": 0,
            "allowed_interrupts": 0,
            "low_confidence_blocks": 0,
            "total_processed": 0,
            "ml_predictions": 0,
        }
        
        # ML enhancement (bonus feature)
        if use_ml_enhancement:
            self._init_ml_detector()
        
        if self.debug_mode:
            logger.info(
                f"SmartVoiceInterruptionHandler initialized: "
                f"blocked_phrases={len(self.blocked_phrases)}, "
                f"ml_enhanced={use_ml_enhancement}"
            )
    
    def _init_ml_detector(self):
        """Initialize ML-based filler detection (bonus)"""
        try:
            from .ml_utterance_classifier import MLUtteranceClassifier
            self.ml_classifier = MLUtteranceClassifier()
            logger.info("✨ ML enhancement activated")
        except ImportError:
            logger.warning("ML classifier not available, using rule-based only")
            self.use_ml_enhancement = False
    
    @classmethod
    def _load_config_from_env(cls) -> Set[str]:
        """Load blocked phrases from environment configuration"""
        env_config = os.getenv("BLOCKED_INTERRUPTION_PHRASES", "")
        if env_config:
            custom_phrases = {phrase.strip().lower() for phrase in env_config.split(",")}
            logger.info(f"Loaded {len(custom_phrases)} custom blocked phrases from config")
            return custom_phrases
        return cls.BLOCKED_UTTERANCES.copy()
    
    def should_ignore_utterance(
        self, 
        utterance: str, 
        confidence_score: float = 1.0
    ) -> bool:
        """
        Determine if an utterance should be ignored to prevent false interruption.
        
        Args:
            utterance: The transcribed text to evaluate
            confidence_score: ASR confidence level (0.0-1.0)
            
        Returns:
            True if utterance should be ignored, False if it's genuine speech
        """
        if not utterance or not utterance.strip():
            return False
        
        self._metrics["total_processed"] += 1
        
        # First filter: Confidence-based blocking
        if confidence_score < self.minimum_confidence:
            self._metrics["low_confidence_blocks"] += 1
            if self.debug_mode:
                logger.debug(
                    f"⚠️ Low confidence utterance blocked: '{utterance}' "
                    f"(score: {confidence_score:.2f})"
                )
            return True
        
        # Second filter: Rule-based phrase matching
        tokens = self._tokenize_utterance(utterance)
        if not tokens:
            return False
        
        is_blocked_rule = all(token in self.blocked_phrases for token in tokens)
        
        # Third filter: ML enhancement (bonus)
        is_blocked_ml = False
        if self.use_ml_enhancement and self.ml_classifier:
            is_blocked_ml = self.ml_classifier.predict_filler(utterance)
            self._metrics["ml_predictions"] += 1
            
            if self.debug_mode and is_blocked_ml != is_blocked_rule:
                logger.debug(
                    f"🤖 ML prediction differs from rules: "
                    f"rule={is_blocked_rule}, ml={is_blocked_ml}"
                )
        
        # Combine predictions (either method can block)
        is_blocked = is_blocked_rule or is_blocked_ml
        
        if is_blocked:
            self._metrics["suppressed_interrupts"] += 1
            if self.debug_mode:
                method = "ML" if is_blocked_ml and not is_blocked_rule else "Rule"
                logger.info(f"🛑 Suppressed interruption ({method}): '{utterance}'")
        else:
            self._metrics["allowed_interrupts"] += 1
            if self.debug_mode:
                logger.info(f"✅ Genuine speech detected: '{utterance}'")
        
        return is_blocked
    
    def has_genuine_content(
        self, 
        utterance: str,
        confidence_score: float = 1.0
    ) -> bool:
        """
        Check if utterance contains genuine speech content.
        Inverse of should_ignore_utterance for clarity.
        """
        if confidence_score < self.minimum_confidence:
            return False
        
        tokens = self._tokenize_utterance(utterance)
        return any(token not in self.blocked_phrases for token in tokens)
    
    def _tokenize_utterance(self, utterance: str) -> list[str]:
        """
        Tokenize utterance into individual words.
        Can be enhanced for better multi-language support.
        """
        return utterance.lower().strip().split()
    
    def get_performance_metrics(self) -> Dict[str, int]:
        """Retrieve performance and filtering metrics"""
        return self._metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset all performance metrics"""
        self._metrics = {
            "suppressed_interrupts": 0,
            "allowed_interrupts": 0,
            "low_confidence_blocks": 0,
            "total_processed": 0,
            "ml_predictions": 0,
            "ml_predictions": 0
        }
        if self.debug_mode:
            logger.debug("Metrics reset to zero")
    
    def update_blocked_phrases(self, new_phrases: Set[str]) -> None:
        """
        Dynamically update the list of blocked phrases.
        Useful for runtime configuration changes.
        """
        old_count = len(self.blocked_phrases)
        self.blocked_phrases = new_phrases
        logger.info(f"Updated blocked phrases: {old_count} → {len(new_phrases)}")
    
    def add_blocked_phrases(self, phrases: Set[str]) -> None:
        """Add new phrases to the blocked list"""
        self.blocked_phrases.update(phrases)
        logger.debug(f"Added {len(phrases)} new blocked phrases")
    
    def remove_blocked_phrases(self, phrases: Set[str]) -> None:
        """Remove phrases from the blocked list"""
        self.blocked_phrases.difference_update(phrases)
        logger.debug(f"Removed {len(phrases)} blocked phrases")