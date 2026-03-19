"""Sensitive word filter utility module.

Provides efficient sensitive word detection and filtering using the Aho-Corasick algorithm.
"""

import json

import ahocorasick
from log import logger
from settings.config import settings


class SensitiveWordFilter:
    """Sensitive word filter.

    Uses the Aho-Corasick algorithm for efficient sensitive word detection.
    """

    def __init__(self):
        """Initialize the sensitive word filter."""
        self.automaton = None
        self.enabled = settings.ENABLE_SENSITIVE_WORD_FILTER
        self.response_message = settings.SENSITIVE_WORD_RESPONSE
        self._build_automaton()

    def _build_automaton(self) -> None:
        """Build the Aho-Corasick automaton.

        Constructs an automaton from the configured sensitive word list for fast matching.
        """
        if not self.enabled:
            logger.info("Sensitive word filtering is disabled")
            return

        try:
            self.automaton = ahocorasick.Automaton()

            # Add sensitive words to the automaton
            for idx, word in enumerate(settings.SENSITIVE_WORDS):
                if word.strip():  # Ignore empty strings
                    # Convert to lowercase for matching to improve accuracy
                    self.automaton.add_word(word.strip().lower(), (idx, word.strip()))

            # Build the automaton
            self.automaton.make_automaton()

            logger.info(
                f"Sensitive word filter initialized, loaded {len(settings.SENSITIVE_WORDS)} sensitive words"
            )

        except Exception as e:
            logger.error(f"Failed to build sensitive word automaton: {str(e)}")
            self.enabled = False

    def contains_sensitive_word(self, text: str) -> tuple[bool, str | None]:
        """Check if text contains sensitive words.

        Args:
            text: The text to check.

        Returns:
            A tuple of (contains_sensitive_word, matched_word).
        """
        if not self.enabled or not self.automaton or not text:
            return False, None

        try:
            # Convert to lowercase for matching
            text_lower = text.lower()

            # Use the automaton for matching
            for end_index, (
                _,
                original_word,
            ) in self.automaton.iter(text_lower):
                logger.warning(
                    f"Sensitive word detected: {original_word} at position {end_index - len(original_word) + 1}"
                )
                return True, original_word

            return False, None

        except Exception as e:
            logger.error(f"Sensitive word detection failed: {str(e)}")
            return False, None

    def filter_text(self, text: str) -> str:
        """Filter sensitive words from text.

        Args:
            text: The text to filter.

        Returns:
            The filtered text, or a warning message if sensitive words are found.
        """
        if not text:
            return text

        contains_sensitive, matched_word = self.contains_sensitive_word(text)

        if contains_sensitive:
            logger.info(
                f"Text contains sensitive word '{matched_word}', returning warning message"
            )
            return self.response_message

        return text

    def filter_streaming_chunk(self, chunk: str) -> str | None:
        """Filter streaming output data chunks.

        Args:
            chunk: The streaming output data chunk.

        Returns:
            The filtered chunk, or None if blocked due to sensitive word detection.
        """
        if not chunk or not self.enabled:
            return chunk

        try:
            # Parse streaming data
            if chunk.startswith("data:"):
                json_content_str = chunk[len("data:") :].strip()
                if json_content_str and json_content_str != "[DONE]":
                    try:
                        event_data = json.loads(json_content_str)

                        # Check text content in different event types
                        text_to_check = ""

                        # Check answer field (typically contains AI response content)
                        if "answer" in event_data:
                            text_to_check += event_data["answer"]

                        # Check other fields that may contain text
                        if "text" in event_data:
                            text_to_check += event_data["text"]

                        if "content" in event_data:
                            text_to_check += str(event_data["content"])

                        # If there is text content to check
                        if text_to_check:
                            (
                                contains_sensitive,
                                matched_word,
                            ) = self.contains_sensitive_word(text_to_check)

                            if contains_sensitive:
                                logger.warning(
                                    f"Sensitive word '{matched_word}' detected in streaming output, blocking"
                                )
                                # Return None to block output
                                return None

                    except json.JSONDecodeError:
                        # If not JSON format, check raw text directly
                        contains_sensitive, matched_word = self.contains_sensitive_word(
                            json_content_str
                        )
                        if contains_sensitive:
                            logger.warning(
                                f"Sensitive word '{matched_word}' detected in streaming output, blocking"
                            )
                            return None

            return chunk

        except Exception as e:
            logger.error(f"Failed to filter streaming data chunk: {str(e)}")
            return chunk

    def reload_sensitive_words(self) -> bool:
        """Reload the sensitive word list.

        Returns:
            True if reload was successful, False otherwise.
        """
        try:
            logger.info("Reloading sensitive word list")
            self._build_automaton()
            return True
        except Exception as e:
            logger.error(f"Failed to reload sensitive word list: {str(e)}")
            return False


# Global sensitive word filter instance
sensitive_word_filter = SensitiveWordFilter()
