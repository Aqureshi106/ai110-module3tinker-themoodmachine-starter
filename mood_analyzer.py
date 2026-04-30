# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements:
          - Extracts and preserves emojis as separate tokens
          - Converts to lowercase
          - Tokenizes words and contractions
          - Keeps emoticons like :) and :(
        """
        tokens = []
        cleaned = text.strip().lower()

        # Extract emoji patterns: Unicode emoji, emoticons like :) :( :(
        emoji_pattern = r'[\U0001F300-\U0001F9FF]|:\)+|:\(+|😂|🎉|💪|😌|😒|🥲|💀'
        word_pattern = r"[a-z0-9]+(?:'[a-z0-9]+)?"

        pos = 0
        while pos < len(cleaned):
            # Try to match an emoji first
            emoji_match = re.match(emoji_pattern, cleaned[pos:])
            if emoji_match:
                tokens.append(emoji_match.group())
                pos += len(emoji_match.group())
                continue

            # Try to match a word
            word_match = re.match(word_pattern, cleaned[pos:])
            if word_match:
                tokens.append(word_match.group())
                pos += len(word_match.group())
                continue

            # Skip non-matching character
            pos += 1

        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Enhancements:
          - Negation handling: "not happy" flips sentiment
          - Word weighting: "hate"/"love" worth more than others
          - Emoji signals: Positive emojis add score, negative emojis subtract
          - Running score to detect conflicting signals
        """
        tokens = self.preprocess(text)
        score = 0
        negation_words = {"not", "no", "never"}

        # Word weights: strong sentiment words get +2/-2, others get +1/-1
        strong_positive = {"love", "amazing", "awesome", "excited"}
        strong_negative = {"hate", "terrible", "awful"}

        # Emoji mappings
        positive_emojis = {"🎉", "😂", "💪", "😌", ":)", "🥲", "😊", "🙂", "😍"}
        negative_emojis = {"😒", ":(", "💀", "😢", "😞"}

        for i, token in enumerate(tokens):
            previous_token = tokens[i - 1] if i > 0 else None
            is_negated = previous_token in negation_words

            # Check for positive words with weighting
            if token in strong_positive:
                score += -2 if is_negated else 2
            elif token in self.positive_words:
                score += -1 if is_negated else 1

            # Check for negative words with weighting
            elif token in strong_negative:
                score += 2 if is_negated else -2
            elif token in self.negative_words:
                score += 1 if is_negated else -1

            # Check for emojis
            elif token in positive_emojis:
                score += 1
            elif token in negative_emojis:
                score -= 1

        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Mapping:
          - score >= 1  -> "positive" (at least one positive signal)
          - score <= -1 -> "negative" (at least one negative signal)
          - score == 0  -> "neutral" (no sentiment signals detected)
          
        For now, we don't use "mixed" label actively. The model
        naturally creates mixed cases when positive and negative words
        cancel each other out (score close to 0).
        """
        score = self.score_text(text)
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        Shows:
          - Which positive/negative words matched and their weights
          - Which emojis were detected
          - The final score and resulting label
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        emoji_hits: List[str] = []
        score = 0

        strong_positive = {"love", "amazing", "awesome", "excited"}
        strong_negative = {"hate", "terrible", "awful"}
        positive_emojis = {"🎉", "😂", "💪", "😌", ":)", "🥲", "😊", "🙂", "😍"}
        negative_emojis = {"😒", ":(", "💀", "😢", "😞"}
        negation_words = {"not", "no", "never"}

        for i, token in enumerate(tokens):
            previous_token = tokens[i - 1] if i > 0 else None
            is_negated = previous_token in negation_words

            if token in strong_positive:
                positive_hits.append(token)
                score += -2 if is_negated else 2
            elif token in self.positive_words:
                positive_hits.append(token)
                score += -1 if is_negated else 1
            elif token in strong_negative:
                negative_hits.append(token)
                score += 2 if is_negated else -2
            elif token in self.negative_words:
                negative_hits.append(token)
                score += 1 if is_negated else -1
            elif token in positive_emojis:
                emoji_hits.append(token + " (pos)")
                score += 1
            elif token in negative_emojis:
                emoji_hits.append(token + " (neg)")
                score -= 1

        label = self.predict_label(text)
        return (
            f"Score={score} Label={label} | "
            f"Positive: {positive_hits or '[]'}, "
            f"Negative: {negative_hits or '[]'}, "
            f"Emojis: {emoji_hits or '[]'}"
        )
