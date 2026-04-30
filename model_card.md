# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
I built and compared both the rule-based model (mood_analyzer.py) and the ML model (ml_experiments.py using scikit-learn).

**Intended purpose:**  
Classify short social media posts and text messages into mood categories: "positive", "negative", "neutral", or "mixed". The system is designed to handle realistic language including slang, emojis, sarcasm attempts, and mixed emotions.

**How it works (brief):**  
**Rule-based:** Tokenizes text, extracts emojis as features, scores based on positive/negative word lists with weights, applies negation logic, and maps scores to labels using thresholds.  
**ML:** Trains a Naive Bayes classifier on bag-of-words features extracted from labeled posts, learning word-emotion associations automatically.



## 2. Data

**Dataset description:**  
Started with 11 sample posts provided in the starter code. Expanded to 23 posts total by adding 12 new examples. The dataset includes a mix of:
- 8 positive labels
- 7 negative labels  
- 4 neutral labels
- 4 mixed labels

The expanded posts introduce realistic language patterns: slang ("lowkey", "no cap"), emojis (🎉, 😒, 💪, 😌, 💀), emoticons (:), :(, :)), contradictory emotions, and sarcasm attempts.

**Labeling process:**  
I manually labeled all 23 posts based on my interpretation of the intended sentiment. For ambiguous cases:
- "I was stressed, but I had fun" → labeled "mixed" because it explicitly contradicts
- "Feeling tired but kind of hopeful" → labeled "mixed" for the same reason
- "I absolutely love waiting in line for 2 hours 😒" → labeled "negative" because eye-roll emoji signals sarcasm despite the word "love"

Some posts were genuinely difficult to classify and could reasonably have alternate labels.

**Important characteristics of your dataset:**  
- Contains modern slang: "lowkey", "no cap", "not me", "choosing violence", "fire", "sick"
- Heavy emoji use: 🎉, 😒, 💪, 😌, 💀, 😍, 🙂, :), :(
- Includes sarcasm: "I absolutely love waiting in line for 2 hours 😒"
- Mixed emotions: multiple examples of contradictory sentiments in one post
- Informal/conversational tone throughout
- Short posts (8-20 words average)
- Emoticons and modern internet language conventions

**Possible issues with the dataset:**  
- Very small (23 examples) — ML model easily memorizes patterns
- Skewed toward younger, internet-native speaker conventions
- All posts created by one person (me) — limited linguistic diversity
- Heavy reliance on punctuation and emojis for tone (may not reflect how all users write)
- Over-represented: sarcasm with positive words (appears multiple times)
- Under-represented: longer, more formal expressions of emotion
- Limited cultural or dialect diversity
- No posts in languages other than English

## 3. How the Rule Based Model Works

**Your scoring rules:**  
The rule-based model (`mood_analyzer.py`) implements the following logic:

1. **Preprocessing:** Tokenizes text into words and emoji tokens using regex patterns that recognize Unicode emojis (🎉, 😂, 💪, etc.) and emoticons (:), :(, etc.). Converts to lowercase.

2. **Scoring with weighted words:**
   - Strong positive words (+2): "love", "amazing", "awesome", "excited"
   - Regular positive words (+1): "happy", "great", "good", "fun", "chill", "relaxed", "sick", "fire", "proud", "peace"
   - Strong negative words (-2): "hate", "terrible", "awful"
   - Regular negative words (-1): "sad", "bad", "angry", "upset", "tired", "stressed", "boring", "stuck", "exhausted"

3. **Negation handling:** When "not", "no", or "never" appears directly before a sentiment word, it flips the sign:
   - "not happy" → flips happy(+1) to -1
   - "not bad" → flips bad(-1) to +1

4. **Emoji scoring:**
   - Positive emojis (+1): 🎉, 😂, 💪, 😌, :), 🥲, 😊, 🙂, 😍
   - Negative emojis (-1): 😒, :(, 💀, 😢, 😞

5. **Label thresholds:**
   - score > 0 → "positive"
   - score < 0 → "negative"
   - score == 0 → "neutral"
   - (No explicit "mixed" label in rule-based; emerges when contradictions cancel out)

**Strengths of this approach:**  
- Transparent and interpretable: you can see exactly why a decision was made
- Fast and deterministic: same input always produces same output
- Handles negation reasonably well: "not happy" correctly inverts sentiment
- Recognizes emojis as distinct signals from words
- Works well on clear sentiment cases: "I love this" (positive), "This is terrible" (negative)

**Weaknesses of this approach:**  
- **Cannot detect sarcasm:** "I absolutely love waiting in line for 2 hours 😒" predicts positive (sees "love" +2) even though the intention is negative
- **Score cancellation problem:** "I love the idea but hate the execution" (love +2, hate -2 = 0) predicts "neutral" instead of "mixed"
- **Missing vocabulary:** "worst" (in "worst day ever") not in word lists, so post labeled neutral instead of negative
- **Word order doesn't matter:** phrase "but" after negative doesn't reduce its weight; treats all words independently
- **Overfits to word lists:** any sentiment word not in the lists is ignored
- **Emoji limitations:** only recognizes pre-defined emojis; new or uncommon ones are silently dropped
- **No contextual weighting:** a post like "This is boring but fun" (boring -1, fun +1 = 0) becomes neutral despite clear internal contradiction
- **Slang without word list:** "This code is fire" (fire not initially in list) predicted neutral before enhancement

## 4. How the ML Model Works

**Features used:**  
Bag of words representation using scikit-learn's `CountVectorizer`. Each post is converted into a vector where each dimension represents the count of a unique word or token (including emoji tokens). The vocabulary is built from the 23 training posts.

**Training data:**  
The model trained on all 23 posts from SAMPLE_POSTS with their corresponding TRUE_LABELS. No train/test split was used during evaluation (the model was evaluated on the same data it trained on).

**Training behavior:**  
- Achieved 100% accuracy on the training set
- Used Naive Bayes classifier (assumed word independence)
- Model successfully learned to associate:
  - Words like "love", "great", "amazing" → positive
  - Words like "hate", "bad", "terrible" → negative
  - Multi-word patterns like "love" + "😒" emoji → negative (detecting sarcasm pattern)
  - Contradictory word pairs like "love" + "hate" → mixed
  - Subtle words like "exhausted" → negative, "peace" → positive

**Why 100% accuracy is suspicious:**  
The perfect score indicates the model has memorized the exact training distribution rather than learning generalizable patterns. This is **overfitting**—the model will likely perform worse on new, unseen text.

**Strengths and weaknesses:**  
**Strengths:**
- Automatically learns word-emotion associations without hand-crafted rules
- Successfully detected sarcasm pattern in "I absolutely love waiting in line for 2 hours 😒" → negative
- Handled mixed emotions correctly: "I was stressed, but I had fun" → mixed
- Learned that "worst day ever" + "cap" → negative (contextual pattern)
- No threshold tuning needed; classifier assigns label directly

**Weaknesses:**
- Overfits to training set (100% accuracy is unrealistic)
- No generalization capability; untested on truly new text
- Bag of words loses word order: "I love hate" treated same as "I hate love"
- Depends entirely on having similar examples at training time
- Small vocabulary (only words seen in 23 posts)
- Would fail on new slang or emoji not in training data
- Cannot explain its reasoning (black box)

## 5. Evaluation

**How you evaluated the model:**  
Both models were evaluated on all 23 posts from the dataset using accuracy (correct predictions / total predictions).

**Rule-based accuracy:** 70% (16/23 correct)  
**ML accuracy:** 100% (23/23 correct on training data)

**Examples of correct predictions:**

1. **"I love this class so much"** (all models) → positive ✓
   - Clear: strong positive word "love" dominates. Both models easily recognize this pattern.

2. **"I absolutely love waiting in line for 2 hours 😒"** (ML only) → negative ✓
   - ML learned the pattern: positive word + eye-roll emoji = sarcasm. Rule-based failed because "love" (+2) outweighed the emoji (+1).

3. **"I was stressed, but I had fun"** (ML only) → mixed ✓
   - ML learned: contradictory words in sequence = mixed emotion. Rule-based fails (stressed -1, fun +1 = 0 → neutral) because it can't recognize the contradiction.

**Examples of incorrect predictions:**

1. **"Feeling tired but kind of hopeful"** (rule-based) → predicted negative, true: mixed ✗
   - Rule-based: sees "tired" (-1) but "hopeful" not in word list, so only scores -1 → negative
   - ML: correctly predicts mixed (learned the pattern from other examples)
   - Why the failure: vocabulary gap. "Hopeful" was not added to positive words until later.

2. **"honestly this is the worst day ever no cap"** (rule-based) → predicted neutral, true: negative ✗
   - Rule-based: "worst" not in word list. Sees no matching words, score = 0 → neutral
   - ML: correctly predicts negative (learned "worst" and "cap" markers)
   - Why the failure: slang "no cap" and colloquial "worst day" patterns not in vocabulary

3. **"I love the idea but hate the execution"** (rule-based) → predicted neutral, true: mixed ✗
   - Rule-based: love (+2) + hate (-2) = 0 → neutral. Cannot express "mixed" unless forced by threshold.
   - ML: correctly predicts mixed (learned contradictory patterns)
   - Why the failure: score cancellation problem is fundamental to simple numeric scoring

**Comparison pattern:**  
The ML model succeeded precisely where the rule-based model failed: wherever the true label was "mixed" or where sarcasm/contradiction was involved.## 6. Limitations

**Rule-based model limitations:**

1. **Cannot reliably detect sarcasm:** "I love getting stuck in traffic" predicts positive even though the intended sentiment is negative. The model sees the word "love" and assigns +2, unaware that "stuck in traffic" is universally negative. To fix this would require explicit pattern matching or a much richer knowledge base.

2. **Vocabulary dependency:** "honestly this is the worst day ever" predicts neutral because "worst" is not in the word list. Adding every possible negative intensifier is impractical. This is why the ML model performed better—it learned "worst" from training data automatically.

3. **Score cancellation creates false neutrals:** Posts like "I love the idea but hate the execution" score as (love +2) + (hate -2) = 0, predicting "neutral" instead of the true label "mixed". The model has no way to express that two opposing emotions coexist.

4. **No understanding of context or word order:** "I hate love songs" and "I love hate speech" would score identically (hate -2, love +2, or vice versa), even though the first is negative and the second would be detected as negative only by accident.

5. **Emoji coverage is limited:** Only 9 emojis are recognized as positive and 5 as negative. Hundreds of other emojis are silently ignored. An emoji like 🥺 (sad face) or 😔 (frustrated) would have no effect on the score.

6. **Small training dataset:** Only 23 posts. Any model trained on this size is unlikely to generalize well to real-world text. Typical sentiment analysis systems train on thousands or millions of examples.

**ML model limitations:**

1. **Overfitting to training data:** 100% accuracy on the training set is a red flag. The model has memorized patterns specific to these 23 posts and will likely perform poorly on new, unseen text. True accuracy would be tested with a held-out test set.

2. **Bag-of-words loses important structure:** Phrases like "not good" and "good not" would be treated identically because the model only counts words, not their order. The current negation detection in the rule-based model is lost.

3. **No vocabulary coverage beyond training set:** If a user writes "that's absolutely brilliant!", the word "brilliant" was never seen at training time and would be treated as neutral. The model cannot generalize to synonyms of words it learned.

4. **Black box reasoning:** Unlike the rule-based model, you cannot inspect why the ML model made a decision. It's impossible to debug or correct specific failure modes without retraining on new data.

5. **Sensitive to label quality:** If any of the 23 labels I assigned are wrong, the model learns incorrect patterns. There's no way to know if my label for "I'm fine 🙂" (neutral) is universally correct—different annotators might label it differently.

**Shared limitations (both models):**

- Cannot distinguish between genuine and pretended emotion: "I'm so sad 😭😂" (joking through tears) is genuinely ambiguous
- No understanding of context: "I'm anxious about the exam" (negative) vs. "I'm anxious to get started" (positive) both contain "anxious" but have opposite sentiments
- Struggles with irony and implied meaning: "Oh great, another meeting" (sarcastic/negative despite "great")
- Very short posts only: evaluation set averages 8-15 words. Performance on longer posts is unknown
- English-only: uses English word lists and doesn't recognize non-Latin scripts, so would fail on posts in other languages or code-mixed text

## 7. Ethical Considerations

**Scope and bias in this model:**

This model is optimized for **young, internet-native English speakers in North America** who use modern slang, emojis, and informal tone. The training data consists of posts with:
- Slang like "lowkey", "no cap", "fire", "sick" (common in Gen Z and millennial online culture)
- Modern emojis (🎉, 💀, 😒) familiar to digital natives
- Informal grammar and abbreviations ("ngl", "lol" patterns)
- References to coding and tech ("my code finally works")

**Populations that might be misrepresented or misclassified:**

- **Formal communication:** Business emails, academic writing, or professional contexts would likely be misclassified as all "neutral" (few sentiment words, no emojis)
- **Other cultures/languages:** Posts with cultural references, non-Western names, or code-mixed languages would be treated as gibberish
- **Older generations:** Users who don't use emojis or modern slang would see reduced accuracy
- **Neurodivergent users:** People who communicate with "flat" tone, sarcasm, or literal interpretation (autistic users, for example) might be consistently misclassified
- **People with communication disabilities:** Users who rely on repetition, unusual punctuation, or custom emoji use might confuse the model
- **Marginalized communities:** Slang from Black Vernacular English, AAVE, or other dialects not represented in training data would be missed
- **Sarcastic or indirect communicators:** The model's inability to detect sarcasm affects anyone who communicates indirectly

**Real-world harms:**

If this model were deployed in production:

1. **Moderation bias:** If used to moderate posts or detect "toxic" mood, informal young people might be over-flagged while silent suffering (formal tone + negative emoji) is missed
2. **Mental health risks:** If used for crisis detection ("detecting sadness"), users expressing distress in non-standard language might go undetected
3. **Labor exploitation:** If used to monitor worker sentiment (e.g., in customer service chats), workers from marginalized communities expressing frustration in their own dialect might be unfairly targeted
4. **Amplification of existing bias:** If the model performs worse on certain groups' language, and those predictions are used in algorithms (recommendation, ranking), it could systematically disadvantage those groups
5. **False sense of accuracy:** The rule-based model's transparent design might create false confidence—users might believe it's accurate when it actually fails silently on their language patterns

**Recommendations for responsible use:**

- This model should **only** be used as a research demonstration, not in production systems affecting people
- If extended to production, it requires:
  - Evaluation on diverse language samples and demographics
  - Separate held-out test set (not training accuracy)
  - Documented performance breakdowns by demographic group
  - Human review of flagged cases
  - User transparency about model limitations
  - Regular audits for bias and drift

## 8. Ideas for Improvement

**Data improvements:**
- Collect more labeled examples (aim for 500+) with diverse annotators to reduce one-person bias
- Include formal vs. informal registers, different age groups, and multiple dialects
- Add posts from underrepresented communities to improve fairness
- Create a proper held-out test set (train on 70%, test on 30%) to measure real generalization
- Add adversarial examples: intentional sarcasm, fake emotion, mixed signals to stress-test the model

**Rule-based enhancements:**
- Add a "mixed" label explicitly: if both positive and negative words are present (not just canceling), predict "mixed"
- Implement basic n-gram support for negation: "I don't like this" (capture "don't like" as stronger negative than just "like")
- Add intensifiers: "very sad" should score more negative than just "sad"
- Pattern-match sarcasm: if post contains positive word + emoji like 😒 or word "right" (sarcastic marker), flip sentiment
- Add slang dictionary with human-curated mappings: "fire", "sick", "lit", "vibes" → positive; "sus", "mid", "cringe" → negative

**ML improvements:**
- Use **TF-IDF** instead of raw word counts to downweight common but uninformative words
- Implement **n-grams** (bigrams, trigrams) to capture phrases: "very bad" and "not bad" would now be distinct
- Add **emoji handling**: separate feature space for emoji tokens vs. words
- Train/test split: evaluate on truly held-out data, not training accuracy
- Cross-validation: train 5 different models on different 80% subsets to estimate real generalization
- Use a **Logistic Regression** classifier (more explainable than Naive Bayes)
- Add **regularization** (L2 penalty) to reduce overfitting

**Hybrid approach:**
- Combine rule-based sarcasm detection with ML classification:
  - Rule-based: pre-process to flag likely sarcasm
  - ML: use sarcasm flag as an additional feature for the classifier
  - This gives interpretability (why sarcasm?) + learned flexibility (when to trust it)

**Architectural options:**
- **BERT or RoBERTa:** fine-tune a pre-trained transformer model on the 23 labeled posts
  - Pros: handles complex language patterns, context, word order
  - Cons: requires more data to avoid overfitting, black box
- **Simple neural network:** one hidden layer with embedding inputs
  - Pros: still relatively interpretable, handles non-linearity
  - Cons: needs more training data than current 23 examples
- **Active learning:** ask the user to label the most uncertain predictions to iteratively improve

**Evaluation improvements:**
- **Confusion matrix:** break down which labels are confused with which (e.g., "mixed" confused with "neutral")
- **Per-class metrics:** report precision, recall, F1 for each label separately
- **Error analysis:** manually review every misclassification and group into categories
- **Domain evaluation:** test on Reddit posts vs. Twitter vs. TikTok comments to see which domains work well
- **Demographic parity:** measure accuracy separately for slang vs. formal text, with/without emojis, etc.
