import joblib
from typing import List
import math
from symspellpy import SymSpell, Verbosity

# Load saved model components
VOCAB = joblib.load('./ai_models/auto_correct/vocab.pkl')
WORD_COUNTS = joblib.load('./ai_models/auto_correct/word_counts.pkl')

keyboard_rows = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm"
]

key_positions = {}
for y, row in enumerate(keyboard_rows):
    for x, char in enumerate(row):
        key_positions[char] = (x, y)


def key_distance(c1, c2):
    if c1 not in key_positions or c2 not in key_positions:
        return 2  # high penalty for unknown chars
    x1, y1 = key_positions[c1]
    x2, y2 = key_positions[c2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# -----------------------------
# Weighted Edit Distance
# -----------------------------
def keyboard_weighted_edit(word1: str, word2: str) -> float:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = key_distance(word1[i - 1], word2[j - 1])
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # deletion
                dp[i][j - 1] + 1,  # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
    return dp[m][n]


# -----------------------------
# Autocorrect Candidates
# -----------------------------
def get_candidates(word: str) -> List[str]:
    candidates = []
    for vocab_word in VOCAB:
        dist = keyboard_weighted_edit(word, vocab_word)
        score = -dist + math.log(WORD_COUNTS[vocab_word] + 1)
        candidates.append((vocab_word, score))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [w for w, _ in candidates[:5]]


# -----------------------------
# Autocomplete
# -----------------------------
def autocomplete(prefix: str, max_results: int = 5) -> List[str]:
    prefix = prefix.lower()
    return sorted([w for w in VOCAB if w.startswith(prefix)], key=lambda x: -WORD_COUNTS[x])[:max_results]


# ------------
# edit distance
# ------------

def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]

    return set(deletes + transposes + replaces + inserts)


def known(words):
    return set(w for w in words if w in WORD_COUNTS)


def candidates(word):
    return (
            known([word]) or
            known(edits1(word)) or
            known(e2 for e1 in edits1(word) for e2 in edits1(e1)) or
            [word]
    )


def correct(word):
    return max(candidates(word), key=WORD_COUNTS.get)


# ------------

# ------------


sym_spell = SymSpell(max_dictionary_edit_distance=2)
sym_spell.load_dictionary("./data/frequency_dictionary_en_82_765.txt", term_index=0, count_index=1)


# Auto-suggest function
def auto_suggest(word: str, max_dist: int = 2):
    suggestions = sym_spell.lookup(
        word,
        Verbosity.CLOSEST,  # You can also use TOP or ALL
        max_edit_distance=max_dist
    )
    return [s.term for s in suggestions]