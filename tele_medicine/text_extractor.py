# tele_medicine/text_extractor.py
"""
Robust text -> feature extractor.

Features:
- Loads FEATURES and SYNONYMS from files at same directory.
- Expands synonyms programmatically (layman phrasing + small paraphrase patterns).
- Uses heuristics (regex) + direct token match + synonym match + fuzzy match.
- Returns (keys, vector) aligned to FEATURES (same order).
- Uses only Python stdlib (difflib, re, json, os, numpy).

Deploy: replace your existing text_extractor.py with this file.
"""

import os
import re
import json
import numpy as np
from difflib import get_close_matches

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FEATURE_PATH = os.path.join(BASE_DIR, "features.json")
SYNONYM_PATH = os.path.join(BASE_DIR, "synonyms.json")

# ---- Load FEATURES ----
with open(FEATURE_PATH, "r", encoding="utf-8") as f:
    FEATURES = json.load(f)

# ---- Load existing SYNONYMS (if any) ----
if os.path.exists(SYNONYM_PATH):
    with open(SYNONYM_PATH, "r", encoding="utf-8") as f:
        ORIGINAL_SYNONYMS = json.load(f)
else:
    ORIGINAL_SYNONYMS = {}

# -----------------------------
# Text utilities
# -----------------------------
def _normalize_text(s: str) -> str:
    s = s.lower()
    # keep letters, digits and spaces; replace others with space
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

# -----------------------------
# Programmatic synonym expander
# -----------------------------
def _variants_for_feature(feat: str):
    """
    Given feature key like 'knee_pain' produce common layman paraphrases.
    Keeps them short and realistic.
    """
    parts = feat.split("_")
    joined = " ".join(parts)
    variants = set()

    # base tokens
    variants.add(joined)
    variants.add(joined.replace("  ", " ").strip())
    variants.add(joined.replace("_", " "))

    # simple expansions for pain-like tokens
    if "pain" in feat or feat.endswith("pain") or "ache" in feat:
        # if feature already contains 'pain', also add "pain in my X" forms and "X ache"
        if feat.endswith("pain"):
            base = " ".join(parts[:-1]) if len(parts) > 1 else parts[0]
            base = base.strip()
            if base:
                variants.add(f"pain in my {base}")
                variants.add(f"{base} pain")
                variants.add(f"{base} ache")
                variants.add(f"ache in {base}")
                variants.add(f"my {base} hurts")
                variants.add(f"my {base} is hurting")
        else:
            # general
            variants.add(f"{joined} pain")
            variants.add(f"{joined} ache")
    else:
        # generic helpful paraphrases
        variants.add(f"have {joined}")
        variants.add(f"{joined} problem")
        variants.add(f"{joined} issue")

    # generate plural/singular where relevant
    if joined.endswith("s"):
        variants.add(joined.rstrip("s"))
    else:
        variants.add(joined + "s")

    # small set of common rephrasings for some tokens
    if "fever" in feat:
        variants.update({"fever", "i have a fever", "high temperature", "temperature is", "feeling feverish", "feverish"})
    if "nausea" in feat or "vomit" in feat:
        variants.update({"nausea", "i feel nauseous", "throwing up", "i vomited", "vomiting"})
    if "cough" in feat:
        variants.update({"cough", "i am coughing", "dry cough", "productive cough", "have a cough"})
    if "headache" in feat:
        variants.update({"headache", "my head hurts", "migraine", "head pain"})
    if "dizziness" in feat or "vertigo" in feat:
        variants.update({"dizzy", "i feel dizzy", "vertigo", "spinning sensation", "i am unsteady", "can't keep balance"})
    if "rash" in feat or "itch" in feat or "skin" in feat:
        variants.update({"rash", "skin rash", "itching", "itchy skin", "red spots", "red bumps"})
    if "urine" in feat or "urination" in feat:
        variants.update({"urine", "peeing problem", "pain while urinating", "burn while peeing", "foul smelling urine"})

    # trim and normalize results
    cleaned = set()
    for v in variants:
        cv = _normalize_text(v)
        if cv:
            cleaned.add(cv)

    return sorted(cleaned)


# -----------------------------
# Build a merged expanded synonyms dictionary
# -----------------------------
EXPANDED_SYNONYMS = {}

# First, copy any existing synonyms from ORIGINAL_SYNONYMS
for k, v in ORIGINAL_SYNONYMS.items():
    EXPANDED_SYNONYMS.setdefault(k, set()).update([_normalize_text(s) for s in v])

# Then programmatically add paraphrases for every feature
for feat in FEATURES:
    # only add if not already present
    cand = set(_variants_for_feature(feat))
    EXPANDED_SYNONYMS.setdefault(feat, set()).update(cand)

# Convert sets -> sorted lists for stability
for k in list(EXPANDED_SYNONYMS.keys()):
    EXPANDED_SYNONYMS[k] = sorted(list(EXPANDED_SYNONYMS[k]))

# OPTIONAL: write expanded file for inspection (commented out by default)
# expanded_out = os.path.join(BASE_DIR, "expanded_synonyms.json")
# with open(expanded_out, "w", encoding="utf-8") as f:
#     json.dump(EXPANDED_SYNONYMS, f, indent=2, ensure_ascii=False)


# -----------------------------
# Heuristics (regex rules) - extend as needed
# -----------------------------
def _rx(s): return re.compile(s, re.I)

HEURISTICS = {}

def _add_heur(key, regexes):
    if key in FEATURES:
        HEURISTICS.setdefault(key, []).extend(regexes)

# Fever
_add_heur("high_fever", [
    _rx(r"\b(high|very|really)\s+fever\b"),
    _rx(r"\btemperature\s+(is|of|around)?\s*(1\d{2}|[89]\d)\b"),  # rough
    _rx(r"\bfever(ish)?\b"),
])
_add_heur("mild_fever", [
    _rx(r"\b(slight|low|mild)\s+fever\b"),
    _rx(r"\b(a\s+)?fever\b"),
])

# Pain cluster examples
_add_heur("knee_pain", [
    _rx(r"\bknee\s+pain\b"),
    _rx(r"\bpain\s+in\s+(my\s+)?knees?\b"),
    _rx(r"\bmy\s+knees?\s+hurt\b"),
])
_add_heur("back_pain", [
    _rx(r"\b(back|lower\s+back|spine)\s+pain\b"),
    _rx(r"\bmy\s+back\s+hurts\b"),
])
_add_heur("chest_pain", [
    _rx(r"\bchest\s+pain\b"),
    _rx(r"\bpain\s+in\s+(my\s+)?chest\b"),
])

# Respiratory
_add_heur("cough", [ _rx(r"\bcough(ing)?\b"), ])
_add_heur("throat_irritation", [ _rx(r"\bsore\s+throat\b"), ])

# GI
_add_heur("vomiting", [ _rx(r"\bvomit(ing)?|throwing\s+up\b"), ])
_add_heur("nausea", [ _rx(r"\bnausea|nauseous|queasy\b"), ])
_add_heur("diarrhoea", [ _rx(r"\b(diarrhea|diarrhoea|loose\s+motions?)\b"), ])

# Neurological / general
_add_heur("dizziness", [ _rx(r"\bdizzy|dizziness|lightheaded\b"), _rx(r"\bvertigo\b") ])
_add_heur("fatigue", [ _rx(r"\bfatigue|tired|exhausted\b") ])
_add_heur("weakness_in_limbs", [ _rx(r"\bweak(ness)?\s+(in|of)\s+(my\s+)?(legs|arms|limbs?)\b") ])
_add_heur("loss_of_balance", [ _rx(r"\bloss\s+of\s+balance|unsteady\b") ])

# Skin related
_add_heur("skin_rash", [ _rx(r"\brash\b"), _rx(r"\brashes\b") ])
_add_heur("itching", [ _rx(r"\bitch(ing)?\b"), _rx(r"\bitchy\b") ])

# urinary
_add_heur("burning_micturition", [ _rx(r"\bburning\s+(while|during)?\s*urination\b"), _rx(r"\bburn\s+while\s+peeing\b") ])

# (Add/extend heuristics above as you see fit)


# -----------------------------
# Fuzzy helper using difflib (stdlib)
# -----------------------------
def _fuzzy_match_tokens(text_norm, syn_list, cutoff=0.85, max_matches=3):
    """
    Given text_norm and a list of candidate synonyms, return a set of
    syns that closely match any token/phrase in text_norm.
    We attempt matches against the words and short n-grams.
    """
    found = set()
    # create tokens and small ngrams from text_norm
    tokens = text_norm.split()
    ngrams = tokens[:]  # 1-grams
    # add 2-gram and 3-gram windows
    for n in (2, 3):
        for i in range(len(tokens) - n + 1):
            ngrams.append(" ".join(tokens[i:i+n]))

    # match each candidate with difflib against ngrams
    for syn in syn_list:
        # direct substring (fast)
        if syn in text_norm:
            found.add(syn)
            continue
        # get close matches against ngrams
        matches = get_close_matches(syn, ngrams, n=max_matches, cutoff=cutoff)
        if matches:
            found.add(syn)
    return found


# -----------------------------
# Main extraction function
# -----------------------------
def extract_features(text: str):
    """
    Return (keys, vector) aligned to FEATURES.
    Approach:
    1) normalize
    2) apply heuristics (strict regex)
    3) exact/synonym match (from EXPANDED_SYNONYMS)
    4) fuzzy matching (difflib) for tolerant matching
    5) direct token match (feature name as readable token)
    6) handle simple negation patterns (no/without)
    """
    text_norm = _normalize_text(text)
    found = set()

    # 1) heuristics
    for feat, regexes in HEURISTICS.items():
        if any(r.search(text_norm) for r in regexes):
            found.add(feat)

    # 2) exact / synonym match (fast)
    for feat, syns in EXPANDED_SYNONYMS.items():
        for s in syns:
            # word-boundary check (but quicker: substring)
            if f" {s} " in f" {text_norm} " or text_norm.startswith(s + " ") or text_norm.endswith(" " + s):
                found.add(feat)
                break

    # 3) synonym loop with exact word boundaries
    for feat, syns in EXPANDED_SYNONYMS.items():
        for s in syns:
            if re.search(rf"\b{re.escape(s)}\b", text_norm):
                found.add(feat)
                break

    # 4) fuzzy matching (moderate tolerance)
    # build a mapping of feature->synlist flattened
    flat_map = {feat: syns for feat, syns in EXPANDED_SYNONYMS.items()}
    # To keep it efficient, attempt fuzzy only if we have few matches so far
    if len(found) < 6:
        # gather all synonyms into a list for fuzzy scanning per-feature
        for feat, syns in flat_map.items():
            matches = _fuzzy_match_tokens(text_norm, syns, cutoff=0.85, max_matches=2)
            if matches:
                found.add(feat)

    # 5) direct token match (feature key spelled out)
    for feat in FEATURES:
        token = feat.replace("_", " ")
        if re.search(rf"\b{re.escape(token)}\b", text_norm):
            found.add(feat)

    # 6) negation handling (drop features preceded by no/not/without)
    for feat in list(found):
        token = feat.replace("_", " ")
        if re.search(rf"\b(no|not|without|never)\s+{re.escape(token)}\b", text_norm):
            found.discard(feat)

    # Build sorted keys and vector aligned to FEATURES order
    keys = sorted(found)
    vector = np.array([1 if f in found else 0 for f in FEATURES], dtype=int)

    return keys, vector
