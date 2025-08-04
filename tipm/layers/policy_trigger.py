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

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass
import re
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

from ..utils.nlp_utils import PolicyTextProcessor
from ..config.layer_configs import PolicyLayerConfig


@dataclass 
class TariffPolicyFeatures:
    """Structured features extracted from tariff policy"""
    policy_id: str
    hs_codes: List[str]
    tariff_rates: List[float]
    affected_countries: List[str]
    policy_type: str  # 'bilateral', 'multilateral', 'unilateral'
    urgency_score: float  # 0-1 scale
    policy_embedding: np.ndarray
    temporal_features: Dict[str, Any]


class PolicyTriggerLayer:
    """
    Layer 1: Policy Trigger Input Processing
    
    Transforms raw policy announcements into structured features
    for downstream impact modeling.
    """
    
    def __init__(self, config: PolicyLayerConfig):
        """Initialize policy trigger layer"""
        self.config = config
        self.text_processor = PolicyTextProcessor()
        
        # NLP components
        self.tokenizer = None
        self.policy_model = None
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 3)
        )
        
        # Feature processing
        self.scaler = StandardScaler()
        self.is_fitted = False
        
        # Policy classification patterns
        self.hs_code_patterns = [
            r'HS\s*(\d{2,10})',
            r'heading\s*(\d{2,4})',
            r'tariff\s*line\s*(\d+)'
        ]
        
        self.rate_patterns = [
            r'(\d+(?:\.\d+)?)\s*%',
            r'(\d+(?:\.\d+)?)\s*percent',
            r'rate\s*of\s*(\d+(?:\.\d+)?)'
        ]
    
    def fit(self, policy_data: pd.DataFrame) -> "PolicyTriggerLayer":
        """
        Train the policy trigger layer on historical policy data
        
        Args:
            policy_data: DataFrame with columns:
                - policy_text: Raw policy announcement text
                - effective_date: Policy effective date
                - hs_codes: Known HS codes (for training)
                - tariff_rates: Known tariff rates (for training)
                - countries: Affected countries
        """
        if policy_data is None or policy_data.empty:
            # Initialize with default configuration
            self._initialize_components()
            self.is_fitted = True
            return self
            
        # Initialize NLP components
        self._initialize_components()
        
        # Extract and vectorize policy texts
        policy_texts = policy_data['policy_text'].fillna('')
        self.tfidf_vectorizer.fit(policy_texts)
        
        # Train policy embedding model
        self._train_policy_embeddings(policy_texts)
        
        # Fit scalers on extracted features
        features = []
        for _, row in policy_data.iterrows():
            extracted_features = self._extract_numerical_features(row['policy_text'])
            features.append(extracted_features)
        
        if features:
            feature_matrix = np.array(features)
            self.scaler.fit(feature_matrix)
        
        self.is_fitted = True
        return self
    
    def _initialize_components(self):
        """Initialize NLP and ML components"""
        try:
            # Use a lightweight transformer for policy embedding
            model_name = "distilbert-base-uncased"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.policy_model = AutoModel.from_pretrained(model_name)
        except Exception:
            # Fallback to None if transformers not available
            self.tokenizer = None
            self.policy_model = None
    
    def _train_policy_embeddings(self, texts: pd.Series):
        """Train policy text embeddings"""
        # Implementation for training custom policy embeddings
        # This would involve fine-tuning on policy-specific vocabulary
        pass
    
    def transform(self, tariff_shock) -> TariffPolicyFeatures:
        """
        Transform raw tariff shock into structured features
        
        Args:
            tariff_shock: TariffShock object with policy information
            
        Returns:
            TariffPolicyFeatures: Structured feature representation
        """
        if not self.is_fitted:
            raise ValueError("Layer must be fitted before transform")
        
        # Extract HS codes from policy text
        hs_codes = self._extract_hs_codes(tariff_shock.policy_text)
        if not hs_codes and hasattr(tariff_shock, 'hs_codes'):
            hs_codes = tariff_shock.hs_codes
        
        # Extract tariff rates
        tariff_rates = self._extract_tariff_rates(tariff_shock.policy_text)
        if not tariff_rates and hasattr(tariff_shock, 'rate_change'):
            tariff_rates = [tariff_shock.rate_change]
        
        # Extract affected countries
        countries = self._extract_countries(tariff_shock.policy_text)
        if not countries:
            countries = [tariff_shock.origin_country, tariff_shock.destination_country]
        
        # Classify policy type
        policy_type = self._classify_policy_type(tariff_shock.policy_text, countries)
        
        # Calculate urgency score
        urgency_score = self._calculate_urgency_score(tariff_shock.policy_text)
        
        # Generate policy embedding
        policy_embedding = self._generate_policy_embedding(tariff_shock.policy_text)
        
        # Extract temporal features
        temporal_features = self._extract_temporal_features(tariff_shock.effective_date)
        
        return TariffPolicyFeatures(
            policy_id=tariff_shock.tariff_id,
            hs_codes=hs_codes,
            tariff_rates=tariff_rates,
            affected_countries=countries,
            policy_type=policy_type,
            urgency_score=urgency_score,
            policy_embedding=policy_embedding,
            temporal_features=temporal_features
        )
    
    def _extract_hs_codes(self, policy_text: str) -> List[str]:
        """Extract HS codes from policy text using regex patterns"""
        hs_codes = []
        for pattern in self.hs_code_patterns:
            matches = re.findall(pattern, policy_text, re.IGNORECASE)
            hs_codes.extend(matches)
        return list(set(hs_codes))  # Remove duplicates
    
    def _extract_tariff_rates(self, policy_text: str) -> List[float]:
        """Extract tariff rates from policy text"""
        rates = []
        for pattern in self.rate_patterns:
            matches = re.findall(pattern, policy_text, re.IGNORECASE)
            for match in matches:
                try:
                    rates.append(float(match))
                except ValueError:
                    continue
        return rates
    
    def _extract_countries(self, policy_text: str) -> List[str]:
        """Extract country names/codes from policy text"""
        # Simplified implementation - would use NER in production
        country_keywords = [
            'china', 'united states', 'singapore', 'malaysia', 'thailand',
            'vietnam', 'indonesia', 'philippines', 'japan', 'south korea',
            'germany', 'france', 'united kingdom', 'canada', 'mexico',
            'brazil', 'india', 'australia'
        ]
        
        found_countries = []
        text_lower = policy_text.lower()
        for country in country_keywords:
            if country in text_lower:
                found_countries.append(country.title())
        
        return found_countries
    
    def _classify_policy_type(self, policy_text: str, countries: List[str]) -> str:
        """Classify policy as bilateral, multilateral, or unilateral"""
        if len(countries) <= 1:
            return 'unilateral'
        elif len(countries) == 2:
            return 'bilateral'
        else:
            return 'multilateral'
    
    def _calculate_urgency_score(self, policy_text: str) -> float:
        """Calculate policy urgency score based on language patterns"""
        urgency_keywords = [
            'immediate', 'urgent', 'emergency', 'temporary', 'suspension',
            'retaliation', 'response', 'investigation', 'dumping'
        ]
        
        text_lower = policy_text.lower()
        urgency_count = sum(1 for keyword in urgency_keywords if keyword in text_lower)
        
        # Normalize to 0-1 scale
        max_urgency = len(urgency_keywords)
        return min(urgency_count / max_urgency, 1.0)
    
    def _generate_policy_embedding(self, policy_text: str) -> np.ndarray:
        """Generate semantic embedding for policy text"""
        if self.tokenizer and self.policy_model:
            try:
                # Tokenize and encode
                inputs = self.tokenizer(
                    policy_text,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=512
                )
                
                with torch.no_grad():
                    outputs = self.policy_model(**inputs)
                    # Use mean pooling of last hidden states
                    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
                
                return embedding
            except Exception:
                pass
        
        # Fallback to TF-IDF if transformer fails
        if hasattr(self.tfidf_vectorizer, 'vocabulary_'):
            tfidf_vec = self.tfidf_vectorizer.transform([policy_text])
            return tfidf_vec.toarray().flatten()
        
        # Final fallback to zero vector
        return np.zeros(768)  # Standard BERT dimension
    
    def _extract_temporal_features(self, effective_date: str) -> Dict[str, Any]:
        """Extract temporal features from effective date"""
        try:
            date_obj = pd.to_datetime(effective_date)
            return {
                'month': date_obj.month,
                'quarter': date_obj.quarter,
                'year': date_obj.year,
                'day_of_week': date_obj.dayofweek,
                'days_until_effective': (date_obj - pd.Timestamp.now()).days
            }
        except Exception:
            return {
                'month': 1,
                'quarter': 1,
                'year': 2024,
                'day_of_week': 0,
                'days_until_effective': 0
            }
    
    def _extract_numerical_features(self, policy_text: str) -> np.ndarray:
        """Extract numerical features for scaler training"""
        # Extract basic text statistics
        features = [
            len(policy_text),
            len(policy_text.split()),
            policy_text.count(','),
            policy_text.count('.'),
            len(self._extract_hs_codes(policy_text)),
            len(self._extract_tariff_rates(policy_text)),
            self._calculate_urgency_score(policy_text)
        ]
        return np.array(features)
    
    def get_policy_similarity(self, policy1: str, policy2: str) -> float:
        """Calculate semantic similarity between two policies"""
        if hasattr(self.tfidf_vectorizer, 'vocabulary_'):
            vec1 = self.tfidf_vectorizer.transform([policy1])
            vec2 = self.tfidf_vectorizer.transform([policy2])
            
            # Cosine similarity
            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(vec1, vec2)[0][0]
            return similarity
        
        return 0.0
