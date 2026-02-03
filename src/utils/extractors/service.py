"""
Provide keyword extraction service implementation.
"""
import re
from difflib import SequenceMatcher
from typing import TypeVar

T = TypeVar('T')


class PhraseExtractionService:
    """
    Service for extracting and normalizing phrases from text.
    """

    def __init__(
            self,
            phrases_mapping: dict[T, list[str]],
            noise_words: list | set | None = None,
            similarity_threshold: float = 0.75,
    ):
        """
        Initialize the service.

        Args:
            phrases_mapping: phrases mapping to extract from text.
            noise_words: list of words to exclude in matching.
            similarity_threshold: Minimum similarity ratio for fuzzy matching (0.0 to 1.0)
        """
        self._similarity_threshold = similarity_threshold
        self._phrases_mapping = phrases_mapping
        self._noise_words = noise_words or set()
        self._build_reverse_mapping()

    def _build_reverse_mapping(self) -> None:
        """
        Build reverse mapping from all variations to keywords.
        """
        self._variation_to_phrase: dict[str, str] = {}
        for keyword, variations in self._phrases_mapping.items():
            for variation in variations:
                self._variation_to_phrase[variation.lower()] = keyword

        self._variation_to_phrase = dict(sorted(self._variation_to_phrase.items(), reverse=True))

    def _normalize_text(self, text: str) -> str:
        """
        Normalize text by removing extra spaces and converting to lowercase.
        """
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text

    def _split_preserving_phrases(self, text: str) -> list[str]:
        """Split text but preserve multi-word genre phrases."""
        # Try to match all known genre variations first
        matched_phrases = []
        remaining_text = text

        # Sort variations by length (longest first) to match longer phrases first
        sorted_variations = sorted(self._variation_to_phrase.keys(), key=len, reverse=True)

        for variation in sorted_variations:
            if variation in remaining_text:
                matched_phrases.append(variation)
                remaining_text = remaining_text.replace(variation, ' ')

        # Clean up remaining text and split
        remaining_words = [w for w in remaining_text.split() if w and w not in self._noise_words]

        return matched_phrases + remaining_words

    def _fuzzy_match(self, text: str) -> list[T]:
        """Find genres using fuzzy string matching."""
        matched_phrases = []

        for variation, phrase in self._variation_to_phrase.items():
            similarity = SequenceMatcher(None, text, variation).ratio()
            if similarity >= self._similarity_threshold:
                matched_phrases.append(phrase)

        return matched_phrases

    def _exact_match(self, text: str) -> list[T]:
        """Find genres using exact matching."""
        matched_phrases = []

        # Check full text
        if text in self._variation_to_phrase:
            matched_phrases.append(self._variation_to_phrase[text])

        # Check if text contains any variation
        for variation, phrase in self._variation_to_phrase.items():
            if variation in text:
                matched_phrases.append(phrase)

        return matched_phrases

    def extract_phrases(self, text: str, use_fuzzy: bool = True) -> list[T]:
        """
        Extract phrases from a single text string.

        Args:
            text: input text with phrase.
            use_fuzzy: whether to use fuzzy matching in addition to exact matching

        Returns:
            List of extracted phrases
        """
        normalized = self._normalize_text(text)
        matches = set()

        # Try exact matching on full text
        matches.update(self._exact_match(normalized))

        # Split text preserving multi-word phrases
        phrases = self._split_preserving_phrases(normalized)
        for phrase in phrases:
            matches.update(self._exact_match(phrase))

        # Try fuzzy matching if enabled and no exact matches found
        if use_fuzzy and not matches:
            matches.update(self._fuzzy_match(normalized))
            for phrase in phrases:
                matches.update(self._fuzzy_match(phrase))

        return list(matches)
