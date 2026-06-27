# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class keeps the model flow simple:
  - Preprocess raw text into consistent tokens
  - Score each token as positive, negative, or neutral
  - Convert the final score into a mood label
"""

import re
from typing import Dict, List, Optional, Tuple

from dataset import NEGATIVE_WORDS, POSITIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    TOKEN_PATTERN = re.compile(
        "[\U0001F300-\U0001FAFF]|:\\)+|:\\(+|[a-z0-9]+(?:'[a-z0-9]+)?"
    )

    NEGATION_WORDS = {
        "not",
        "no",
        "never",
        "don't",
        "can't",
        "won't",
        "isn't",
        "wasn't",
        "aren't",
    }

    WORD_WEIGHTS: Dict[str, int] = {
        "love": 2,
        "amazing": 2,
        "awesome": 2,
        "excited": 2,
        "hate": -2,
        "terrible": -2,
        "awful": -2,
        "worst": -2,
    }

    EMOJI_WEIGHTS: Dict[str, int] = {
        ":)": 1,
        ":))": 1,
        ":(": -1,
        ":((": -1,
        "\U0001F389": 1,
        "\U0001F602": 1,
        "\U0001F60A": 1,
        "\U0001F60C": 1,
        "\U0001F60D": 1,
        "\U0001F642": 1,
        "\U0001F4AA": 1,
        "\U0001F612": -1,
        "\U0001F622": -1,
        "\U0001F61E": -1,
        "\U0001F480": -1,
    }

    SARCASM_STARTERS = {"when", "getting", "waiting"}
    COMPLAINT_WORDS = {
        "crash",
        "crashes",
        "crashed",
        "stuck",
        "traffic",
        "waiting",
        "line",
    }

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

        # A few dataset-specific words that carry sentiment but are not in
        # the starter lists. Keeping them here lets the original data stay simple.
        self.positive_words.update({"best", "grateful", "hopeful", "win", "works"})
        self.negative_words.update({"died", "scared", "violence", "worst"})

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        Improvements:
          - Converts to lowercase
          - Normalizes curly apostrophes
          - Tokenizes words, contractions, emojis, and emoticons
        """
        cleaned = (
            text.strip()
            .lower()
            .replace("\u2019", "'")
            .replace("\u2018", "'")
        )
        return self.TOKEN_PATTERN.findall(cleaned)

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def _score_tokens(self, tokens: List[str]) -> Tuple[int, Dict[str, List[str]]]:
        """
        Score already-tokenized text and return both the score and debug details.
        """
        score = 0
        matches: Dict[str, List[str]] = {
            "positive": [],
            "negative": [],
            "emoji": [],
        }

        for i, token in enumerate(tokens):
            value = 0

            following_tokens = tokens[i + 1:]
            looks_sarcastic = (
                token == "love"
                and any(word in self.SARCASM_STARTERS for word in following_tokens[:3])
                and any(word in self.COMPLAINT_WORDS for word in following_tokens)
            )

            if looks_sarcastic:
                value = -2
            elif token in self.WORD_WEIGHTS:
                value = self.WORD_WEIGHTS[token]
            elif token in self.positive_words:
                value = 1
            elif token in self.negative_words:
                value = -1
            elif token in self.EMOJI_WEIGHTS:
                value = self.EMOJI_WEIGHTS[token]

            if value == 0:
                continue

            recent_tokens = tokens[max(0, i - 3):i]
            if any(previous in self.NEGATION_WORDS for previous in recent_tokens):
                value *= -1

            score += value

            if token in self.EMOJI_WEIGHTS:
                direction = "pos" if value > 0 else "neg"
                matches["emoji"].append(f"{token} ({direction})")
            elif value > 0:
                matches["positive"].append(token)
            else:
                matches["negative"].append(token)

        return score, matches

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.

        Enhancements:
          - Negation handling: "not happy" flips the positive signal
          - Small word weights for strong words like "love" and "hate"
          - Emoji/emoticon signals such as :) and :(
        """
        tokens = self.preprocess(text)
        score, _matches = self._score_tokens(tokens)
        return score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.

        Mapping:
          - balanced positive and negative evidence -> "mixed"
          - score > 0 -> "positive"
          - score < 0 -> "negative"
          - no score -> "neutral"
        """
        tokens = self.preprocess(text)
        score, matches = self._score_tokens(tokens)
        has_positive = bool(matches["positive"]) or any(
            "(pos)" in hit for hit in matches["emoji"]
        )
        has_negative = bool(matches["negative"]) or any(
            "(neg)" in hit for hit in matches["emoji"]
        )

        if has_positive and has_negative and abs(score) <= 1:
            return "mixed"
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
        Return a short string explaining why the model chose its label.
        """
        tokens = self.preprocess(text)
        score, matches = self._score_tokens(tokens)
        label = self.predict_label(text)
        return (
            f"Tokens={tokens} | Score={score} Label={label} | "
            f"Positive: {matches['positive'] or '[]'}, "
            f"Negative: {matches['negative'] or '[]'}, "
            f"Emojis: {matches['emoji'] or '[]'}"
        )
