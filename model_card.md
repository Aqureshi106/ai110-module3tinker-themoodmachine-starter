# Model Card: Mood Machine

This model card describes the Mood Machine project. The project includes two mood classifiers:

1. A rule-based model in `mood_analyzer.py`
2. A tiny machine learning model in `ml_experiments.py`

Both systems classify short posts as `positive`, `negative`, `neutral`, or `mixed`.

## 1. Intended Use

Mood Machine is intended as a classroom/demo system for exploring how simple mood classifiers work. It is useful for:

- Testing how hand-written rules respond to words, slang, negation, and emojis
- Comparing a transparent rule-based system with a learned bag-of-words model
- Practicing error analysis on examples that are realistic but small enough to inspect manually

It is not intended for production use, mental health monitoring, content moderation, hiring, grading, discipline, or any other high-stakes decision. The dataset is small and personally constructed, and the models are not reliable enough to make decisions about real people.

## 2. Data

The shared dataset lives in `dataset.py`. It contains two parallel lists:

- `SAMPLE_POSTS`: short social-media-style posts
- `TRUE_LABELS`: one human label for each post

The current dataset has 35 posts and 35 labels. I confirmed:

```text
len(SAMPLE_POSTS) == len(TRUE_LABELS)
```

The dataset started with simple examples like:

- `"I love this class so much"` -> `positive`
- `"Today was a terrible day"` -> `negative`
- `"This is fine"` -> `neutral`
- `"I was stressed, but I had fun"` -> `mixed`

I expanded it with posts that include more realistic language:

- Slang: `"lowkey proud but also scared to submit this"`, `"that update is wicked fast"`
- Emojis/emoticons: `"highkey grateful for my friends today :)"`, `"bruh my phone died right before the quiz :("`
- Sarcasm: `"I absolutely love waiting in line for 2 hours 😒"`, `"love when plans change last second... amazing"`
- Mixed emotions: `"kinda proud but completely drained"`, `"Feeling tired but kind of hopeful"`
- Subtle tone: `"lol this meeting could have been an email"`

Labels were assigned manually based on intended meaning, not just keyword matching. Some labels are debatable. For example, `"got the news and honestly don't know how to feel"` is labeled `neutral`, but another annotator might label it `mixed` or `negative` depending on context. `"I'm fine 🙂"` style examples are also tone-dependent because the emoji can be sincere, awkward, or masking discomfort.

## 3. Rule-Based Model

The rule-based model is implemented in `mood_analyzer.py`. Its flow is:

1. `preprocess(text)` normalizes the text and returns tokens.
2. `score_text(text)` converts tokens into a numeric score.
3. `predict_label(text)` maps score and evidence to a final label.

### Preprocessing

The model:

- Lowercases text
- Normalizes curly apostrophes
- Tokenizes words, contractions, emojis, and emoticons

For example:

```text
"I was stressed, but I had fun"
-> ['i', 'was', 'stressed', 'but', 'i', 'had', 'fun']
```

### Scoring Rules

The model starts at score `0`.

Positive signals add points:

- Strong positive words such as `love`, `amazing`, `awesome`, `excited` add `+2`
- Other positive words such as `happy`, `good`, `fun`, `chill`, `proud`, `peace`, `sick`, `fire` add `+1`
- Positive emojis/emoticons such as `:)`, `🎉`, `😂`, `😊`, `😌`, `😍`, `🙂`, `💪` add `+1`

Negative signals subtract points:

- Strong negative words such as `hate`, `terrible`, `awful`, `worst` add `-2`
- Other negative words such as `sad`, `bad`, `tired`, `stressed`, `boring`, `stuck`, `exhausted` add `-1`
- Negative emojis/emoticons such as `:(`, `😒`, `😢`, `😞`, `💀` add `-1`

The model also adds a few dataset-specific vocabulary items inside `MoodAnalyzer`, such as `hopeful`, `grateful`, `win`, `works`, `died`, `scared`, and `violence`.

### Enhancements

The rule-based model includes several small improvements:

- Negation handling: if a negation word such as `not`, `no`, `never`, `don't`, or `can't` appears within the previous few tokens, the sentiment value flips.
- Mixed-label handling: if the model finds both positive and negative evidence and the total score is close to balanced, it predicts `mixed`.
- Emoji logic: emojis and emoticons are treated as sentiment-bearing tokens.
- Limited sarcasm rule: if `love` appears near words like `when`, `getting`, or `waiting`, and the sentence also contains complaint words like `stuck`, `traffic`, `waiting`, `line`, or `crashes`, the model treats `love` as negative evidence.

One example the sarcasm rule fixes:

```text
"I absolutely love waiting in line for 2 hours 😒"
-> predicted negative
```

The rule works because `love` appears in a complaint frame: `love` + `waiting` + `line`.

## 4. Evaluation

I evaluated the rule-based model on all 35 labeled examples in `dataset.py`.

Current rule-based accuracy:

```text
0.83
```

Before the final four added posts, the rule-based model scored:

```text
0.94
```

The drop happened because the new examples intentionally probed weaknesses the rules did not cover.

Current rule-based mismatches:

```text
"lol this meeting could have been an email"
predicted neutral, true negative
```

The model saw no sentiment words, so the score stayed `0`. Humans often read this phrase as a complaint, but the model has no rule for implied annoyance.

```text
"love when plans change last second... amazing"
predicted positive, true negative
```

The model saw `love` and `amazing`, both strong positive words. It did not understand that the whole sentence is sarcastic.

```text
"love when the wifi dies during lecture"
predicted positive, true negative
```

The model saw `love` as `+2`. It did not treat `dies` as a complaint word, so the sarcasm rule did not trigger.

```text
"that update is wicked fast"
predicted neutral, true positive
```

The model does not understand `wicked fast` as praise. Both words were ignored.

```text
"not bad honestly :)"
predicted mixed, true positive
```

The model flips `bad` because of `not`, but then the positive `:)` emoji is also affected by the negation window. This creates confused evidence and a `mixed` label.

```text
"kinda proud but completely drained"
predicted positive, true mixed
```

The model sees `proud` but ignores `drained`, so the negative side of the mixed emotion disappears.

## 5. Detailed Error Analysis

Chosen error:

```text
"love when the wifi dies during lecture"
```

True label:

```text
negative
```

Rule-based prediction:

```text
positive
```

Reasoning walkthrough:

1. The model preprocesses the post into:

```text
['love', 'when', 'the', 'wifi', 'dies', 'during', 'lecture']
```

2. It checks each token against the weighted word lists.

3. `love` is a strong positive word, so it contributes `+2`.

4. The sarcasm rule asks whether `love` appears near a sarcasm starter and whether the rest of the sentence contains a known complaint word.

5. `when` is a sarcasm starter, but `dies` is not in the complaint-word list. The complaint list currently includes words like `crash`, `crashes`, `crashed`, `stuck`, `traffic`, `waiting`, and `line`.

6. Since the sarcasm rule does not trigger, `love` remains positive.

7. No other token changes the score, so the final score is `+2`.

8. A score greater than zero maps to `positive`.

This is not a random bug. It reveals a limitation of hand-written rules: a rule can work on `"love waiting in line"` and still miss `"love when the wifi dies"` because the wording changed slightly. I am documenting this as a limitation rather than adding more words immediately. Adding `dies` would fix this one example, but the same pattern would reappear for `freezes`, `disconnects`, `breaks`, `lags`, and many other complaint words.

## 6. ML Model Comparison

The ML extension is implemented in `ml_experiments.py`.

It uses:

- `CountVectorizer` for bag-of-words features
- `LogisticRegression(max_iter=1000)` for classification

It trains on `SAMPLE_POSTS` and `TRUE_LABELS`, then evaluates on the same examples. Because there is no train/test split, its accuracy is training accuracy, not real generalization accuracy.

Current ML result on the 35-example dataset:

```text
1.00
```

The ML model behaved differently from the rule-based model. It correctly predicted the examples that the rule-based model missed, including:

- `"lol this meeting could have been an email"` -> `negative`
- `"love when plans change last second... amazing"` -> `negative`
- `"love when the wifi dies during lecture"` -> `negative`
- `"that update is wicked fast"` -> `positive`
- `"not bad honestly :)"` -> `positive`
- `"kinda proud but completely drained"` -> `mixed`

This does not mean the ML model is truly better in a broad sense. It was trained and evaluated on the same data, so it can memorize the examples and labels. The result shows that the ML model is very sensitive to the labels I created: when I added new labeled posts, the ML model immediately fit them, while the rule-based model did not change unless I changed the code or word lists.

The ML model may fail differently on unseen text. For example, it might learn that `love` can be negative in the training examples, but it may not generalize correctly to a new sentence like `"love when my laptop decides to update during class"` unless similar words appear in the training data. It also uses bag-of-words features, so it does not truly understand word order, sarcasm, or context.

## 7. Limitations

The rule-based model has several known limitations:

- It misses implied negativity. `"lol this meeting could have been an email"` has no negative keyword, so it becomes `neutral`.
- It only catches narrow sarcasm patterns. `"I absolutely love waiting in line for 2 hours 😒"` is fixed, but `"love when plans change last second... amazing"` still becomes `positive`.
- It depends on exact vocabulary. `"drained"` is ignored even though it clearly contributes negative emotion.
- It can over-apply negation. In `"not bad honestly :)"`, the negation window affects more than intended, producing `mixed`.
- It treats many slang phrases literally or ignores them. `"wicked fast"` is positive in context, but the rule-based model predicts `neutral`.

The ML model has different limitations:

- Its `1.00` accuracy is training accuracy, not proof of real performance.
- It may memorize the dataset instead of learning robust sentiment patterns.
- It depends heavily on the labels I created.
- It uses bag-of-words features, so it loses word order and deeper meaning.
- It can only learn from patterns present in this very small dataset.

Both models are limited by the small, informal, English-only dataset.

## 8. Ethical Considerations, Bias, and Scope

This model is optimized for a narrow slice of language: short, informal, internet-style English posts. The dataset includes slang such as `lowkey`, `highkey`, `no cap`, `bruh`, `wicked`, `fire`, and `sick`, plus emojis and school/coding references.

That means the system is most tuned to posts that sound like casual student messages or social media updates. It may misinterpret:

- Formal or professional writing
- Older users' writing styles
- Users who do not use emojis
- Dialects, slang, or cultural references not represented in the examples
- Code-mixed or non-English posts
- Indirect emotional expression
- Sarcasm that does not match the few patterns I wrote rules for

The labels also reflect my interpretation. For ambiguous posts, another person might reasonably disagree. A model trained on these labels can encode those subjective choices as if they were objective truth.

Because of those limitations, this project should be treated as a learning tool only. It should not be used to infer someone's mental health, judge user behavior, moderate content, rank people, or make decisions that affect access to resources.

## 9. Future Improvements

Possible improvements:

- Add a real train/test split for the ML model.
- Collect more labeled examples from multiple annotators.
- Track disagreements between annotators for ambiguous posts.
- Add more slang and phrase-level examples, not just individual words.
- Improve negation so it does not accidentally flip unrelated later tokens.
- Add phrase features or n-grams for ML so it can distinguish `not bad`, `wicked fast`, and sarcastic `love when`.
- Report per-label metrics, not just overall accuracy.
- Keep a separate breaker set that is never used for training.
