"""
NLP utilities for policy text processing
"""

import re
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
import logging


class PolicyTextProcessor:
    """
    Text processing utilities for policy documents
    """

    def __init__(self):
        """Initialize text processor with patterns and vocabularies"""
        # Country name mappings
        self.country_mappings = {
            "united states": "US",
            "china": "CN",
            "singapore": "SG",
            "malaysia": "MY",
            "thailand": "TH",
            "vietnam": "VN",
            "indonesia": "ID",
            "philippines": "PH",
            "japan": "JP",
            "south korea": "KR",
            "germany": "DE",
            "france": "FR",
            "united kingdom": "UK",
            "canada": "CA",
            "mexico": "MX",
            "brazil": "BR",
            "india": "IN",
            "australia": "AU",
        }

        # Policy type indicators
        self.policy_indicators = {
            "tariff": ["tariff", "duty", "customs", "import tax"],
            "quota": ["quota", "limit", "restriction", "ceiling"],
            "subsidy": ["subsidy", "support", "assistance", "aid"],
            "sanction": ["sanction", "penalty", "embargo", "ban"],
            "agreement": ["agreement", "treaty", "accord", "pact"],
        }

        # Urgency indicators
        self.urgency_patterns = [
            r"immediate(?:ly)?",
            r"urgent(?:ly)?",
            r"emergency",
            r"temporary",
            r"suspension",
            r"retaliation",
            r"response\s+to",
            r"investigation",
            r"anti.?dumping",
            r"safeguard",
        ]

        # Date patterns
        self.date_patterns = [
            r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
            r"\d{4}[/-]\d{1,2}[/-]\d{1,2}",
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}",
        ]

    def clean_text(self, text: str) -> str:
        """Clean and normalize policy text"""
        if not isinstance(text, str):
            return ""

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove special characters but keep punctuation
        text = re.sub(r"[^\w\s\.,;:!?()-]", " ", text)

        # Normalize case
        text = text.strip().lower()

        return text

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from policy text"""
        text_clean = self.clean_text(text)

        entities = {
            "countries": [],
            "dates": [],
            "hs_codes": [],
            "amounts": [],
            "policy_types": [],
        }

        # Extract countries
        for country_name, country_code in self.country_mappings.items():
            if country_name in text_clean:
                entities["countries"].append(country_code)

        # Extract dates
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["dates"].extend(matches)

        # Extract HS codes
        hs_patterns = [
            r"hs\s*(\d{2,10})",
            r"heading\s*(\d{2,4})",
            r"tariff\s*line\s*(\d+)",
            r"classification\s*(\d+)",
        ]
        for pattern in hs_patterns:
            matches = re.findall(pattern, text_clean, re.IGNORECASE)
            entities["hs_codes"].extend(matches)

        # Extract monetary amounts
        amount_patterns = [
            r"\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)",
            r"(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollar|usd|million|billion)",
            r"(\d+(?:\.\d+)?)\s*%",
        ]
        for pattern in amount_patterns:
            matches = re.findall(pattern, text_clean, re.IGNORECASE)
            entities["amounts"].extend(matches)

        # Extract policy types
        for policy_type, keywords in self.policy_indicators.items():
            if any(keyword in text_clean for keyword in keywords):
                entities["policy_types"].append(policy_type)

        return entities

    def calculate_sentiment_score(self, text: str) -> float:
        """Calculate basic sentiment score for policy text"""
        # Simplified sentiment analysis based on word lists
        positive_words = [
            "benefit",
            "growth",
            "increase",
            "improve",
            "support",
            "enhance",
            "strengthen",
            "boost",
            "advantage",
            "opportunity",
        ]

        negative_words = [
            "tariff",
            "penalty",
            "restriction",
            "ban",
            "limit",
            "reduce",
            "decrease",
            "harm",
            "damage",
            "threat",
            "sanction",
            "retaliation",
            "dispute",
            "conflict",
        ]

        neutral_words = [
            "policy",
            "measure",
            "regulation",
            "standard",
            "procedure",
            "implement",
            "establish",
            "maintain",
            "review",
            "monitor",
        ]

        text_clean = self.clean_text(text)
        words = text_clean.split()

        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        neutral_count = sum(1 for word in words if word in neutral_words)

        total_sentiment_words = positive_count + negative_count + neutral_count

        if total_sentiment_words == 0:
            return 0.0

        # Normalize to -1 to 1 scale
        sentiment_score = (positive_count - negative_count) / total_sentiment_words
        return max(-1.0, min(1.0, sentiment_score))

    def extract_numerical_features(self, text: str) -> Dict[str, float]:
        """Extract numerical features from text for ML models"""
        text_clean = self.clean_text(text)

        features = {
            "text_length": len(text),
            "word_count": len(text_clean.split()),
            "sentence_count": len([s for s in re.split(r"[.!?]+", text) if s.strip()]),
            "avg_word_length": (
                np.mean([len(word) for word in text_clean.split()])
                if text_clean.split()
                else 0
            ),
            "punctuation_ratio": (
                sum(1 for char in text if char in ".,;:!?") / len(text) if text else 0
            ),
            "uppercase_ratio": (
                sum(1 for char in text if char.isupper()) / len(text) if text else 0
            ),
            "digit_ratio": (
                sum(1 for char in text if char.isdigit()) / len(text) if text else 0
            ),
            "urgency_score": self._calculate_urgency_score(text_clean),
            "sentiment_score": self.calculate_sentiment_score(text),
            "entity_density": self._calculate_entity_density(text),
        }

        return features

    def _calculate_urgency_score(self, text: str) -> float:
        """Calculate urgency score based on keyword patterns"""
        urgency_count = 0
        for pattern in self.urgency_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            urgency_count += len(matches)

        # Normalize by text length
        words = text.split()
        if not words:
            return 0.0

        return min(urgency_count / len(words) * 100, 1.0)

    def _calculate_entity_density(self, text: str) -> float:
        """Calculate entity density in text"""
        entities = self.extract_entities(text)
        total_entities = sum(len(entity_list) for entity_list in entities.values())

        words = text.split()
        if not words:
            return 0.0

        return total_entities / len(words)

    def identify_policy_scope(self, text: str) -> Dict[str, Any]:
        """Identify the scope and impact level of a policy"""
        text_clean = self.clean_text(text)
        entities = self.extract_entities(text)

        scope_indicators = {
            "bilateral": ["between", "bilateral", "two countries", "agreement with"],
            "multilateral": ["multilateral", "multiple countries", "wto", "regional"],
            "unilateral": ["unilateral", "impose", "implement", "domestic"],
            "global": ["global", "worldwide", "international", "all countries"],
        }

        scope_scores = {}
        for scope_type, indicators in scope_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_clean)
            scope_scores[scope_type] = score

        # Determine primary scope
        primary_scope = (
            max(scope_scores.items(), key=lambda x: x[1])[0]
            if any(scope_scores.values())
            else "unknown"
        )

        return {
            "primary_scope": primary_scope,
            "scope_scores": scope_scores,
            "affected_countries": entities["countries"],
            "policy_types": entities["policy_types"],
            "confidence": (
                max(scope_scores.values()) / sum(scope_scores.values())
                if sum(scope_scores.values()) > 0
                else 0
            ),
        }

    def parse_policy_timeline(self, text: str) -> List[Dict[str, Any]]:
        """Parse timeline information from policy text"""
        timeline_patterns = [
            (
                r"effective\s+(?:from\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
                "effective_date",
            ),
            (r"expires?\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", "expiry_date"),
            (r"review\s+(?:on\s+)?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", "review_date"),
            (r"(?:within\s+)?(\d+)\s+(?:days?|months?|years?)", "duration"),
            (r"immediate(?:ly)?", "immediate"),
        ]

        timeline_events = []
        for pattern, event_type in timeline_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                timeline_events.append(
                    {
                        "type": event_type,
                        "value": match,
                        "text_position": text.lower().find(match.lower()),
                    }
                )

        # Sort by position in text
        timeline_events.sort(key=lambda x: x["text_position"])

        return timeline_events


def extract_policy_triggers(text: str) -> Any:
    """Extract policy triggers from text (stub)."""
    logging.info(f"Extracting policy triggers from text: {text[:30]}...")
    # Placeholder for actual implementation
    return None
