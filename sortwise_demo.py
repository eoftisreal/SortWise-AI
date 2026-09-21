#!/usr/bin/env python3
"""SortWise AI prototype: text-based waste segregation decision support."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ClassificationResult:
    item_type: str
    material: str
    category: str
    confidence: float
    reason: str
    hazardous: bool = False


CATEGORY_RULES: Dict[str, Dict[str, str]] = {
    "default": {
        "recyclable": "Place in the recyclables stream; rinse/empty if required.",
        "organic": "Place in the organic/compost stream if accepted locally.",
        "residual": "Place in residual/general waste.",
        "hazardous": "Do not place in household bins. Use authorized hazardous-waste drop-off.",
        "special": "Use special collection points as per municipal rules.",
    },
    "campus": {
        "recyclable": "Use campus dry-waste/recyclable bin and keep item clean and empty.",
        "organic": "Use campus wet-waste/organic bin; avoid mixing with plastic.",
        "residual": "Use campus general waste bin.",
        "hazardous": "Contact campus facility/safety desk for hazardous disposal route.",
        "special": "Use campus e-waste or special-waste collection drive.",
    },
}

KEYWORDS: List[tuple[List[str], ClassificationResult]] = [
    (
        ["battery", "paint", "chemical", "medicine", "syringe", "bulb", "tube light"],
        ClassificationResult(
            item_type="hazardous household item",
            material="mixed hazardous material",
            category="hazardous",
            confidence=0.92,
            reason="Matched a known hazardous-waste keyword.",
            hazardous=True,
        ),
    ),
    (
        ["bottle", "can", "paper", "cardboard", "glass", "newspaper", "metal"],
        ClassificationResult(
            item_type="recyclable dry item",
            material="paper/plastic/glass/metal",
            category="recyclable",
            confidence=0.86,
            reason="Matched common recyclable material keywords.",
        ),
    ),
    (
        ["food", "banana peel", "vegetable", "fruit peel", "leftover", "tea leaves"],
        ClassificationResult(
            item_type="organic food waste",
            material="biodegradable organic matter",
            category="organic",
            confidence=0.88,
            reason="Matched common biodegradable waste keywords.",
        ),
    ),
    (
        ["diaper", "sanitary", "ceramic", "dust", "styrofoam", "thermocol"],
        ClassificationResult(
            item_type="residual mixed item",
            material="non-recyclable mixed waste",
            category="residual",
            confidence=0.80,
            reason="Matched common residual-waste keywords.",
        ),
    ),
    (
        ["charger", "wire", "earphone", "keyboard", "phone", "laptop", "electronic"],
        ClassificationResult(
            item_type="electronic waste item",
            material="electronic components",
            category="special",
            confidence=0.89,
            reason="Matched e-waste related keywords.",
        ),
    ),
]


def classify_item(description: str) -> Optional[ClassificationResult]:
    text = description.lower().strip()
    if not text:
        return None

    for words, result in KEYWORDS:
        if any(word in text for word in words):
            return result

    return ClassificationResult(
        item_type="unclear item",
        material="unknown",
        category="residual",
        confidence=0.42,
        reason="No strong keyword match found in the provided description.",
    )


def lookup_rule(category: str, locale: str) -> str:
    locale_rules = CATEGORY_RULES.get(locale, CATEGORY_RULES["default"])
    return locale_rules.get(category, CATEGORY_RULES["default"]["residual"])


def generate_output(description: str, locale: str) -> str:
    result = classify_item(description)
    if result is None:
        return (
            "Could not identify the item because no description was provided. "
            "Please provide a short text description or a clear image."
        )

    if result.hazardous:
        return (
            f"AI IDENTIFICATION: {result.item_type} ({result.material}) — confidence {result.confidence:.0%}.\n"
            f"RULE LOOKUP ({locale}): {lookup_rule(result.category, locale)}\n"
            "OUTPUT: This appears hazardous. Follow official local authority guidance and do not mix with regular bins.\n"
            "NOTE: Local safety rules are authoritative."
        )

    if result.confidence < 0.6:
        return (
            f"AI IDENTIFICATION: {result.item_type} — low confidence ({result.confidence:.0%}).\n"
            "OUTPUT: The item is ambiguous. Please verify with local municipal/campus guidance before disposal.\n"
            "NOTE: AI is decision support, not final authority."
        )

    return (
        f"AI IDENTIFICATION: {result.item_type} ({result.material}) — confidence {result.confidence:.0%}.\n"
        f"REASON: {result.reason}\n"
        f"RULE LOOKUP ({locale}): {lookup_rule(result.category, locale)}\n"
        f"OUTPUT: Recommended category: {result.category}.\n"
        "NOTE: Verify final disposal rules for your locality."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="SortWise AI text demo")
    parser.add_argument("description", help="Item description, e.g. 'empty glass bottle'")
    parser.add_argument(
        "--locale",
        default="default",
        choices=["default", "campus"],
        help="Rule profile for disposal guidance",
    )
    args = parser.parse_args()
    print(generate_output(args.description, args.locale))


if __name__ == "__main__":
    main()
