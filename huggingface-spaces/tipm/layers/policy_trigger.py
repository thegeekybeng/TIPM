"""
Layer 1: Policy Trigger Input (Tariff Shock Layer)
=================================================

Processes tariff announcements and policy changes to create structured
input for downstream impact modeling.

Features:
- NLP parsing of policy documents
- HS code-level tariff extraction
- Temporal policy tracking
- Policy similarity analysis
"""

from typing import Dict, List, Any, Optional, Union
import logging
import pandas as pd
import numpy as np
from dataclasses import dataclass
import re
from datetime import datetime, timedelta

# Optional imports with fallbacks
try:
    from transformers import AutoTokenizer, AutoModel
    import torch

    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics.pairwise import cosine_similarity

    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False


@dataclass
class TariffPolicyFeatures:
    """Structured features extracted from tariff policy"""

    policy_id: str
    hs_codes: List[str]
    tariff_rates: List[float]
    affected_countries: List[str]
    country_tariff_map: Dict[str, float]  # Map of country -> tariff rate
    policy_type: str  # 'bilateral', 'multilateral', 'unilateral'
    urgency_score: float  # 0-1 scale
    policy_embedding: np.ndarray
    temporal_features: Dict[str, Any]
    confidence: float  # Prediction confidence score


@dataclass
class TariffShock:
    """Input data structure for tariff shock events"""

    tariff_id: str
    policy_text: str
    origin_country: str
    destination_country: str
    effective_date: Union[str, datetime]
    rate_change: Optional[float] = None
    hs_codes: Optional[List[str]] = None
    country_tariff_map: Optional[Dict[str, float]] = (
        None  # Map of country -> tariff rate
    )


class PolicyTriggerLayer:
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for policy layer"""
        return {
            "max_text_length": 512,
            "embedding_dim": 768,
            "tfidf_max_features": 1000,
            "urgency_threshold": 0.7,
            "confidence_threshold": 0.6,
        }

    def _setup_logging(self) -> logging.Logger:
        """Setup layer-specific logging"""
        logger = logging.getLogger(f"TIPM.{self.__class__.__name__}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _initialize_components(self):
        """Initialize NLP and ML components with error handling"""
        # Initialize TF-IDF vectorizer if sklearn available
        if HAS_SKLEARN:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=self.config.get("tfidf_max_features", 1000),
                stop_words="english",
                ngram_range=(1, 3),
                lowercase=True,
                strip_accents="unicode",
            )
            self.scaler = StandardScaler()
            self.logger.info("Initialized sklearn components")
        else:
            self.tfidf_vectorizer = None
            self.scaler = None
            self.logger.warning("sklearn not available, using fallback methods")

        # Initialize transformer components if available
        if HAS_TRANSFORMERS:
            try:
                model_name = "distilbert-base-uncased"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.policy_model = AutoModel.from_pretrained(model_name)
                self.logger.info(f"Initialized transformer model: {model_name}")
            except Exception as e:
                self.logger.warning(f"Transformer model initialization failed: {e}")
                self.tokenizer = None
                self.policy_model = None
        else:
            self.tokenizer = None
            self.policy_model = None
            self.logger.warning("transformers not available, using TF-IDF embeddings")

    """
    Layer 1: Policy Trigger Input Processing

    Transforms raw policy announcements into structured features
    for downstream impact modeling.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize policy trigger layer with configuration"""
        self.config = config or self._get_default_config()
        self.logger = self._setup_logging()

        # Initialize components with error handling
        self._initialize_components()

        # State tracking
        self.is_fitted = False
        self._training_stats = {}

        # Policy classification patterns
        self.hs_code_patterns = [
            r"HS\s*(\d{2,10})",
            r"heading\s*(\d{2,4})",
            r"tariff\s*line\s*(\d+)",
            r"harmonized\s*system\s*(\d+)",
            r"chapter\s*(\d{1,2})",
        ]

        self.rate_patterns = [
            r"(\d+(?:\.\d+)?)\s*%",
            r"(\d+(?:\.\d+)?)\s*percent",
            r"rate\s*of\s*(\d+(?:\.\d+)?)",
            r"increase\s*to\s*(\d+(?:\.\d+)?)\s*%",
            r"tariff\s*of\s*(\d+(?:\.\d+)?)",
        ]

        # Country pattern mapping for better extraction
        self.country_patterns = {
            "china": ["china", "chinese", "prc", "people's republic of china"],
            "united states": ["usa", "us", "united states", "america"],
            "singapore": ["singapore", "sg"],
            "malaysia": ["malaysia", "my"],
            "thailand": ["thailand", "th", "thai"],
            # ...add other countries as needed...
        }

    # ...existing code...

    def fit(
        self, training_data: Optional[Dict[str, Any]] = None
    ) -> "PolicyTriggerLayer":
        """
        Train the policy trigger layer on historical policy data

        Args:
            training_data: Dictionary containing:
                - policy_texts: List of policy announcement texts
                - features: Optional pre-extracted features
                - labels: Optional ground truth labels for validation
        """
        self.logger.info("Starting policy trigger layer training...")

        try:
            if training_data is None or not training_data:
                self.logger.info("No training data provided, using synthetic data")
                training_data = self._generate_synthetic_training_data()

            policy_texts = training_data.get("policy_texts", [])
            if not policy_texts:
                self.logger.warning("No policy texts found, generating synthetic data")
                policy_texts = self._generate_synthetic_policy_texts()

            # Train TF-IDF vectorizer if available
            if self.tfidf_vectorizer is not None:
                self.tfidf_vectorizer.fit(policy_texts)
                self.logger.info(f"Trained TF-IDF on {len(policy_texts)} texts")

            # Extract and scale numerical features
            numerical_features = []
            for text in policy_texts:
                features = self._extract_numerical_features(text)
                numerical_features.append(features)

            if numerical_features and self.scaler is not None:
                feature_matrix = np.array(numerical_features)
                self.scaler.fit(feature_matrix)
                self.logger.info("Fitted feature scaler")

            # Store training statistics
            self._training_stats = {
                "num_texts": len(policy_texts),
                "avg_text_length": np.mean([len(text) for text in policy_texts]),
                "vocabulary_size": (
                    getattr(self.tfidf_vectorizer, "vocabulary_", {}).get("__len__", 0)
                    if self.tfidf_vectorizer
                    else 0
                ),
            }

            self.is_fitted = True
            self.logger.info("Policy trigger layer training completed successfully")

        except Exception as e:
            self.logger.error(f"Training failed: {e}")
            # Set fallback fitted state
            self.is_fitted = True

        return self

    def predict(self, policy_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process policy input and generate structured features

        Args:
            policy_features: Dictionary containing policy information

        Returns:
            Dictionary with extracted features and confidence scores
        """
        if not self.is_fitted:
            self.logger.warning("Layer not fitted, fitting with default data")
            self.fit()

        try:
            # Create TariffShock object from input
            tariff_shock = self._create_tariff_shock(policy_features)

            # Transform to structured features
            structured_features = self.transform(tariff_shock)

            # Calculate overall confidence
            confidence = self._calculate_prediction_confidence(structured_features)

            return {
                "policy_features": structured_features,
                "confidence": confidence,
                "extraction_stats": {
                    "hs_codes_found": len(structured_features.hs_codes),
                    "tariff_rates_found": len(structured_features.tariff_rates),
                    "countries_found": len(structured_features.affected_countries),
                    "urgency_score": structured_features.urgency_score,
                },
            }

        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            return {"policy_features": None, "confidence": 0.0, "error": str(e)}

    def transform(self, tariff_shock: TariffShock) -> TariffPolicyFeatures:
        """
        Transform raw tariff shock into structured features

        Args:
            tariff_shock: TariffShock object with policy information

        Returns:
            TariffPolicyFeatures: Structured feature representation
        """
        # Extract HS codes from policy text
        hs_codes = self._extract_hs_codes(tariff_shock.policy_text)
        if not hs_codes and tariff_shock.hs_codes:
            hs_codes = tariff_shock.hs_codes

        # Extract tariff rates
        tariff_rates = self._extract_tariff_rates(tariff_shock.policy_text)
        if not tariff_rates and tariff_shock.rate_change is not None:
            tariff_rates = [tariff_shock.rate_change]

        # Extract affected countries
        countries = self._extract_countries(tariff_shock.policy_text)
        if not countries:
            countries = [
                country
                for country in [
                    tariff_shock.origin_country,
                    tariff_shock.destination_country,
                ]
                if country and country.strip()
            ]

        # Classify policy type
        policy_type = self._classify_policy_type(tariff_shock.policy_text, countries)

        # Calculate urgency score
        urgency_score = self._calculate_urgency_score(tariff_shock.policy_text)

        # Generate policy embedding
        policy_embedding = self._generate_policy_embedding(tariff_shock.policy_text)

        # Extract temporal features
        temporal_features = self._extract_temporal_features(tariff_shock.effective_date)

        # Calculate confidence score
        confidence = self._calculate_extraction_confidence(
            hs_codes, tariff_rates, countries, urgency_score
        )

        # Create country_tariff_map from available information
        country_tariff_map = {}
        if countries and tariff_rates:
            # Map each country to the first available tariff rate
            for country in countries:
                country_tariff_map[country] = tariff_rates[0] if tariff_rates else 0.0
        elif tariff_shock.origin_country and tariff_shock.rate_change is not None:
            country_tariff_map[tariff_shock.origin_country] = tariff_shock.rate_change

        return TariffPolicyFeatures(
            policy_id=tariff_shock.tariff_id,
            hs_codes=hs_codes,
            tariff_rates=tariff_rates,
            affected_countries=countries,
            country_tariff_map=country_tariff_map,
            policy_type=policy_type,
            urgency_score=urgency_score,
            policy_embedding=policy_embedding,
            temporal_features=temporal_features,
            confidence=confidence,
        )

    def _create_tariff_shock(self, policy_features: Dict[str, Any]) -> TariffShock:
        """Create TariffShock object from input dictionary"""
        return TariffShock(
            tariff_id=policy_features.get(
                "policy_id", f"policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            ),
            policy_text=policy_features.get("policy_text", ""),
            origin_country=policy_features.get("origin_country", ""),
            destination_country=policy_features.get("destination_country", ""),
            effective_date=policy_features.get("effective_date", datetime.now()),
            rate_change=policy_features.get("rate_change"),
            hs_codes=policy_features.get("hs_codes"),
        )

    def _extract_hs_codes(self, policy_text: str) -> List[str]:
        """Extract HS codes from policy text using enhanced regex patterns"""
        if not policy_text:
            return []

        hs_codes = []
        for pattern in self.hs_code_patterns:
            matches = re.findall(pattern, policy_text, re.IGNORECASE)
            hs_codes.extend(matches)

        # Clean and validate HS codes
        valid_codes = []
        for code in hs_codes:
            # Ensure HS codes are 2-10 digits
            if code.isdigit() and 2 <= len(code) <= 10:
                valid_codes.append(code)

        return list(set(valid_codes))  # Remove duplicates

    def _extract_tariff_rates(self, policy_text: str) -> List[float]:
        """Extract tariff rates from policy text with validation"""
        if not policy_text:
            return []

        rates = []
        for pattern in self.rate_patterns:
            matches = re.findall(pattern, policy_text, re.IGNORECASE)
            for match in matches:
                try:
                    rate = float(match)
                    # Validate reasonable tariff rate range (0-200%)
                    if 0 <= rate <= 200:
                        rates.append(rate)
                except (ValueError, TypeError):
                    continue

        return list(set(rates))  # Remove duplicates

    def _extract_countries(self, policy_text: str) -> List[str]:
        """Extract country names from policy text using enhanced patterns"""
        if not policy_text:
            return []

        found_countries = []
        text_lower = policy_text.lower()

        for country, patterns in self.country_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    found_countries.append(country.title())
                    break  # Found this country, move to next

        return list(set(found_countries))  # Remove duplicates

    def _classify_policy_type(self, policy_text: str, countries: List[str]) -> str:
        """Classify policy as bilateral, multilateral, or unilateral"""
        text_lower = policy_text.lower() if policy_text else ""

        # Check for multilateral keywords
        multilateral_keywords = ["multilateral", "wto", "agreement", "treaty", "bloc"]
        if any(keyword in text_lower for keyword in multilateral_keywords):
            return "multilateral"

        # Check country count
        if len(countries) <= 1:
            return "unilateral"
        elif len(countries) == 2:
            return "bilateral"
        else:
            return "multilateral"

    def _calculate_urgency_score(self, policy_text: str) -> float:
        """Calculate policy urgency score based on language patterns"""
        if not policy_text:
            return 0.0

        urgency_keywords = {
            "immediate": 3.0,
            "urgent": 2.5,
            "emergency": 3.0,
            "temporary": 1.5,
            "suspension": 2.0,
            "retaliation": 2.5,
            "response": 1.5,
            "investigation": 1.0,
            "dumping": 2.0,
            "safeguard": 2.0,
            "countervailing": 2.0,
        }

        text_lower = policy_text.lower()
        urgency_score = 0.0

        for keyword, weight in urgency_keywords.items():
            if keyword in text_lower:
                urgency_score += weight

        # Normalize to 0-1 scale
        max_possible_score = sum(urgency_keywords.values())
        return min(urgency_score / max_possible_score, 1.0)

    def _generate_policy_embedding(self, policy_text: str) -> np.ndarray:
        """Generate semantic embedding for policy text with fallbacks"""
        if not policy_text:
            return np.zeros(getattr(self.config, "embedding_dim", 768))

        # Try transformer embedding first
        if self.tokenizer and self.policy_model:
            try:
                inputs = self.tokenizer(
                    policy_text,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=getattr(self.config, "max_text_length", 512),
                )

                with torch.no_grad():
                    outputs = self.policy_model(**inputs)
                    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

                return embedding
            except Exception as e:
                self.logger.warning("Transformer embedding failed: %s", e)

        # Fallback to TF-IDF if available and fitted
        if self.tfidf_vectorizer and getattr(
            self.tfidf_vectorizer, "vocabulary_", None
        ):
            try:
                tfidf_vec = self.tfidf_vectorizer.transform([policy_text])
                # tfidf_vec is a scipy sparse matrix with toarray() method
                embedding = tfidf_vec.toarray().flatten()  # type: ignore

                # Pad or truncate to standard size
                target_dim = getattr(self.config, "embedding_dim", 768)
                if len(embedding) < target_dim:
                    embedding = np.pad(embedding, (0, target_dim - len(embedding)))
                elif len(embedding) > target_dim:
                    embedding = embedding[:target_dim]

                return embedding
            except ValueError as e:
                self.logger.warning("TF-IDF transform failed: %s", e)
                return np.zeros(getattr(self.config, "embedding_dim", 768))

        # Final fallback to simple text statistics
        return self._simple_text_embedding(policy_text)

    def _simple_text_embedding(self, policy_text: str) -> np.ndarray:
        """Generate simple embedding based on text statistics"""
        features = [
            len(policy_text),
            len(policy_text.split()),
            policy_text.count(","),
            policy_text.count("."),
            policy_text.count("%"),
            len(self._extract_hs_codes(policy_text)),
            len(self._extract_tariff_rates(policy_text)),
            self._calculate_urgency_score(policy_text),
        ]

        # Pad to standard dimension
        target_dim = getattr(self.config, "embedding_dim", 768)
        while len(features) < target_dim:
            features.extend([0.0] * min(len(features), target_dim - len(features)))

        return np.array(features[:target_dim])

    def _extract_temporal_features(
        self, effective_date: Union[str, datetime]
    ) -> Dict[str, Any]:
        """Extract temporal features from effective date with robust handling"""
        try:
            if isinstance(effective_date, str):
                date_obj = pd.to_datetime(effective_date)
            elif isinstance(effective_date, datetime):
                date_obj = effective_date
            else:
                date_obj = datetime.now()

            now = datetime.now()
            days_until = (date_obj - now).days if hasattr(date_obj, "date") else 0

            return {
                "month": date_obj.month,
                "quarter": (date_obj.month - 1) // 3 + 1,
                "year": date_obj.year,
                "day_of_week": date_obj.weekday(),
                "days_until_effective": days_until,
                "is_future": days_until > 0,
                "is_weekend": date_obj.weekday() >= 5,
            }
        except Exception as e:
            self.logger.warning(f"Temporal feature extraction failed: {e}")
            return {
                "month": 1,
                "quarter": 1,
                "year": 2024,
                "day_of_week": 0,
                "days_until_effective": 0,
                "is_future": False,
                "is_weekend": False,
            }

    def _extract_numerical_features(self, policy_text: str) -> np.ndarray:
        """Extract numerical features for scaling"""
        if not policy_text:
            return np.zeros(7)

        features = [
            len(policy_text),
            len(policy_text.split()),
            policy_text.count(","),
            policy_text.count("."),
            len(self._extract_hs_codes(policy_text)),
            len(self._extract_tariff_rates(policy_text)),
            self._calculate_urgency_score(policy_text),
        ]
        return np.array(features)

    def _calculate_extraction_confidence(
        self,
        hs_codes: List[str],
        tariff_rates: List[float],
        countries: List[str],
        urgency_score: float,
    ) -> float:
        """Calculate confidence score for feature extraction"""
        confidence_factors = []

        # HS codes confidence
        confidence_factors.append(
            min(len(hs_codes) / 3.0, 1.0)
        )  # Up to 3 codes is good

        # Tariff rates confidence
        confidence_factors.append(
            min(len(tariff_rates) / 2.0, 1.0)
        )  # Up to 2 rates is good

        # Countries confidence
        confidence_factors.append(
            min(len(countries) / 2.0, 1.0)
        )  # Up to 2 countries is good

        # Urgency score confidence (higher urgency = higher confidence for action)
        confidence_factors.append(urgency_score)

        return float(np.mean(confidence_factors))

    def _calculate_prediction_confidence(self, features: TariffPolicyFeatures) -> float:
        """Calculate overall prediction confidence"""
        return features.confidence

    def _generate_synthetic_training_data(self) -> Dict[str, Any]:
        """Generate synthetic training data for initial fitting"""
        synthetic_texts = self._generate_synthetic_policy_texts()
        return {"policy_texts": synthetic_texts, "features": [], "labels": []}

    def _generate_synthetic_policy_texts(self) -> List[str]:
        """Generate synthetic policy texts for training"""
        templates = [
            "The United States will impose a {rate}% tariff on imports from {country} under HS code {hs_code} effective {date}.",
            "Emergency tariff of {rate}% implemented on {country} products in response to unfair trade practices.",
            "Temporary suspension of tariffs on HS {hs_code} from {country} pending investigation.",
            "Multilateral agreement reached to reduce tariffs by {rate}% on technology imports.",
            "Retaliation tariff of {rate}% imposed on {country} agricultural products under chapter {hs_code}.",
        ]

        countries = ["China", "Germany", "Japan", "South Korea", "Mexico"]
        rates = ["15", "25", "30", "50", "100"]
        hs_codes = ["8517", "8471", "8528", "2710", "1001"]
        dates = ["January 2024", "March 2024", "June 2024"]

        synthetic_texts = []
        for template in templates:
            for i in range(5):  # Generate 5 variations per template
                text = template.format(
                    rate=np.random.choice(rates),
                    country=np.random.choice(countries),
                    hs_code=np.random.choice(hs_codes),
                    date=np.random.choice(dates),
                )
                synthetic_texts.append(text)

        return synthetic_texts

    def get_policy_similarity(self, policy1: str, policy2: str) -> float:
        """Calculate semantic similarity between two policies"""
        if not policy1 or not policy2:
            return 0.0

        try:
            if (
                self.tfidf_vectorizer
                and hasattr(self.tfidf_vectorizer, "vocabulary_")
                and HAS_SKLEARN
            ):
                vec1 = self.tfidf_vectorizer.transform([policy1])
                vec2 = self.tfidf_vectorizer.transform([policy2])
                similarity = cosine_similarity(vec1, vec2)[0][0]
                return float(similarity)
        except Exception as e:
            self.logger.warning(f"Similarity calculation failed: {e}")

        # Fallback to simple text overlap
        words1 = set(policy1.lower().split())
        words2 = set(policy2.lower().split())
        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return intersection / union if union > 0 else 0.0

    def get_training_stats(self) -> Dict[str, Any]:
        """Get training statistics"""
        return {
            "is_fitted": self.is_fitted,
            "training_stats": self._training_stats,
            "config": self.config,
            "has_transformers": HAS_TRANSFORMERS,
            "has_sklearn": HAS_SKLEARN,
        }
