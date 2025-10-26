"""Machine learning component for equipment classification."""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
from pathlib import Path
import json
from typing import Dict, List, Tuple, Optional

class EquipmentClassifierML:
    def __init__(self, model_dir: str = None):
        """Initialize the ML classifier."""
        if model_dir is None:
            model_dir = Path(__file__).parent / 'models'
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.vectorizer = None
        self.classifier = None
        self.load_model()
        
    def load_model(self):
        """Load the trained model and vectorizer if they exist."""
        try:
            self.vectorizer = joblib.load(self.model_dir / 'vectorizer.joblib')
            self.classifier = joblib.load(self.model_dir / 'classifier.joblib')
        except FileNotFoundError:
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=5000,
                stop_words='english'
            )
            self.classifier = MultinomialNB()
            
    def save_model(self):
        """Save the trained model and vectorizer."""
        joblib.dump(self.vectorizer, self.model_dir / 'vectorizer.joblib')
        joblib.dump(self.classifier, self.model_dir / 'classifier.joblib')
        
    def train(self, descriptions: List[str], labels: List[str]):
        """Train the classifier on new data."""
        # Transform text data
        X = self.vectorizer.fit_transform(descriptions)
        
        # Train classifier
        self.classifier.fit(X, labels)
        
        # Save the updated model
        self.save_model()
        
    def predict(self, description: str) -> Tuple[str, float]:
        """Predict equipment type and return confidence score."""
        if not self.vectorizer or not self.classifier:
            return None, 0.0
            
        # Transform input text
        X = self.vectorizer.transform([description])
        
        # Get prediction and probability
        prediction = self.classifier.predict(X)[0]
        proba = np.max(self.classifier.predict_proba(X))
        
        return prediction, float(proba)
        
    def update(self, new_descriptions: List[str], new_labels: List[str]):
        """Update the model with new training data."""
        if not self.vectorizer or not self.classifier:
            self.train(new_descriptions, new_labels)
            return
            
        # Combine new data with existing vocabulary
        X_new = self.vectorizer.transform(new_descriptions)
        
        # Partial fit of the classifier
        self.classifier.partial_fit(X_new, new_labels, classes=np.unique(new_labels))
        
        # Save the updated model
        self.save_model()
        
    def evaluate(self, test_descriptions: List[str], test_labels: List[str]) -> Dict:
        """Evaluate model performance."""
        if not self.vectorizer or not self.classifier:
            return {"error": "Model not trained"}
            
        X_test = self.vectorizer.transform(test_descriptions)
        predictions = self.classifier.predict(X_test)
        
        accuracy = accuracy_score(test_labels, predictions)
        
        return {
            "accuracy": accuracy,
            "n_samples": len(test_labels)
        }