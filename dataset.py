"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "sick",
    "fire",
    "proud",
    "peace",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "stuck",
    "exhausted",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
    "I was stressed, but I had fun",
    "The lecture is so boring",
    "It is a good day to be alive",
    "It's chill, but I'm sad",
    "I seem great",
    "lowkey stressed but trying my best 💪",
    "I absolutely love waiting in line for 2 hours 😒",
    "my code finally works!! 🎉",
    "not me scrolling at 3am again :(",
    "waking up and choosing violence 💀",
    "finally some peace and quiet 😌",
    "honestly this is the worst day ever no cap",
    "ngl i'm feeling kinda empty today",
    "this project turned out awesome 😍",
    "I love the idea but hate the execution",
    "I'm so tired of this",
    "it just happened",
    "lowkey proud but also scared to submit this",
    "lol this meeting could have been an email",
    "highkey grateful for my friends today :)",
    "i'm fine i guess, just tired of pretending",
    "got the news and honestly don't know how to feel",
    "bruh my phone died right before the quiz :(",
    "small win today, finally cleaned my room",
    "love when plans change last second... amazing",
    "love when the wifi dies during lecture",
    "that update is wicked fast",
    "not bad honestly :)",
    "kinda proud but completely drained"
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
    "mixed",     # "I was stressed, but I had fun"
    "negative",  # "The lecture is so boring"
    "positive",  # "It is a good day to be alive"
    "mixed",     # "It's chill, but I'm sad"
    "positive",  # "I seem great"
    "mixed",     # "lowkey stressed but trying my best 💪"
    "negative",  # "I absolutely love waiting in line for 2 hours 😒" (sarcasm)
    "positive",  # "my code finally works!! 🎉"
    "negative",  # "not me scrolling at 3am again :("
    "negative",  # "waking up and choosing violence 💀" (joking but frustrated)
    "positive",  # "finally some peace and quiet 😌"
    "negative",  # "honestly this is the worst day ever no cap"
    "neutral",   # "ngl i'm feeling kinda empty today"
    "positive",  # "this project turned out awesome 😍"
    "mixed",     # "I love the idea but hate the execution"
    "negative",  # "I'm so tired of this"
    "neutral",   # "it just happened"
    "mixed",     # "lowkey proud but also scared to submit this"
    "negative",  # "lol this meeting could have been an email"
    "positive",  # "highkey grateful for my friends today :)"
    "negative",  # "i'm fine i guess, just tired of pretending"
    "neutral",   # "got the news and honestly don't know how to feel"
    "negative",  # "bruh my phone died right before the quiz :("
    "positive",  # "small win today, finally cleaned my room"
    "negative",  # "love when plans change last second... amazing" (sarcasm)
    "negative",  # "love when the wifi dies during lecture" (sarcasm)
    "positive",  # "that update is wicked fast"
    "positive",  # "not bad honestly :)"
    "mixed",     # "kinda proud but completely drained"
]

# TODO: Add 5-10 more posts and labels.
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)
