"""
Filler Word Filter for Intelligent Interruption Handling

This module provides filtering of filler words/sounds during voice agent conversations.
When the agent is speaking, filler-only interruptions (like "uh", "umm", "hmm") are
ignored, while real speech causes immediate interruption.
"""
import logging
import os
from typing import Set, Dict

logger = logging.getLogger("filler-filter")


class FillerWordFilter:
    """
    Intelligent filler word filter for voice interruption handling.
    
    Features:
    - Distinguishes filler-only interruptions from real speech
    - Configurable filler word list
    - Tracks statistics for debugging
    - Language-agnostic design
    """
    
    DEFAULT_FILLERS = {
        "uh", "uhh", "um", "umm", "hmm", "hm",
        "haan", "yeah", "mhm", "mm", "mmm", 
        "err", "ah", "oh", "erm"
    }
    
    def __init__(
        self, 
        ignored_words: Set[str] | None = None,
        confidence_threshold: float = 0.5,
        enable_logging: bool = True
    ):
        """
        Initialize filler word filter.
        
        Args:
            ignored_words: Set of filler words to ignore. If None, uses DEFAULT_FILLERS
            confidence_threshold: Minimum confidence to consider filtering (0.0-1.0)
            enable_logging: Whether to log filtering decisions
        """
        self.ignored_words = ignored_words or self._load_from_env()
        self.confidence_threshold = confidence_threshold
        self.enable_logging = enable_logging
        
        # Statistics
        self._stats = {
            "ignored_fillers": 0,
            "valid_interruptions": 0,
            "low_confidence_ignored": 0,
            "total_events": 0
        }
        
        if self.enable_logging:
            logger.info(
                f"FillerWordFilter initialized with {len(self.ignored_words)} filler words"
            )
    
    @classmethod
    def _load_from_env(cls) -> Set[str]:
        """Load filler words from environment variable or use defaults"""
        env_fillers = os.getenv("FILLER_WORDS", "")
        if env_fillers:
            custom_fillers = {word.strip().lower() for word in env_fillers.split(",")}
            logger.info(f"Loaded {len(custom_fillers)} custom filler words from env")
            return custom_fillers
        return cls.DEFAULT_FILLERS.copy()
    
    def update_filler_words(self, words: Set[str]) -> None:
        """
        Dynamically update the filler word list at runtime.
        
        Args:
            words: New set of filler words
        """
        old_count = len(self.ignored_words)
        self.ignored_words = words
        logger.info(
            f"Updated filler words: {old_count} -> {len(words)}"
        )
    
    def add_filler_words(self, words: Set[str]) -> None:
        """Add new filler words to the existing list"""
        self.ignored_words.update(words)
        logger.debug(f"Added {len(words)} new filler words")
    
    def remove_filler_words(self, words: Set[str]) -> None:
        """Remove filler words from the list"""
        self.ignored_words.difference_update(words)
        logger.debug(f"Removed {len(words)} filler words")
    
    def is_filler_only(
        self, 
        text: str, 
        confidence: float = 1.0
    ) -> bool:
        """
        Check if transcript contains ONLY filler words.
        
        Args:
            text: Transcript text to check
            confidence: ASR confidence score (0.0-1.0)
            
        Returns:
            True if text contains only filler words, False otherwise
        """
        if not text or not text.strip():
            return False
        
        self._stats["total_events"] += 1
        
        # Check confidence threshold for background murmur handling
        if confidence < self.confidence_threshold:
            self._stats["low_confidence_ignored"] += 1
            if self.enable_logging:
                logger.debug(
                    f"Low confidence transcript ignored: '{text}' "
                    f"(confidence: {confidence:.2f})"
                )
            return True
        
        # Tokenize and check if all words are fillers
        words = self._tokenize(text)
        if not words:
            return False
        
        is_filler = all(word in self.ignored_words for word in words)
        
        if is_filler:
            self._stats["ignored_fillers"] += 1
            if self.enable_logging:
                logger.info(f"🚫 Filler detected (ignored): '{text}'")
        
        return is_filler
    
    def contains_real_speech(
        self, 
        text: str,
        confidence: float = 1.0
    ) -> bool:
        """
        Check if transcript contains any non-filler words.
        
        Args:
            text: Transcript text to check
            confidence: ASR confidence score
            
        Returns:
            True if text contains real speech, False otherwise
        """
        if not text or not text.strip():
            return False
        
        # Low confidence is treated as non-speech
        if confidence < self.confidence_threshold:
            return False
        
        words = self._tokenize(text)
        has_real = any(word not in self.ignored_words for word in words)
        
        if has_real:
            self._stats["valid_interruptions"] += 1
            if self.enable_logging:
                logger.info(f"✅ Real speech detected: '{text}'")
        
        return has_real
    
    def _tokenize(self, text: str) -> list[str]:
        """
        Tokenize text into words.
        TODO: Improve for multi-language support
        """
        return text.lower().strip().split()
    
    def get_stats(self) -> Dict[str, int]:
        """Get filtering statistics"""
        return self._stats.copy()
    
    def reset_stats(self) -> None:
        """Reset statistics counters"""
        self._stats = {
            "ignored_fillers": 0,
            "valid_interruptions": 0,
            "low_confidence_ignored": 0,
            "total_events": 0
        }
        logger.debug("Statistics reset")