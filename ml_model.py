"""
ML Model for Digital Awareness Platform
Predicts user knowledge levels and provides personalized recommendations
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os

class DigitalAwarenessML:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_columns = []
        
    def load_survey_data(self, csv_path='survey_data_backup.csv'):
        """Load survey data from CSV file"""
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(df)} survey responses from {csv_path}")
            
            # Try to calculate knowledge scores if not present
            if 'Knowledge_Score' not in df.columns and 'Score' not in df.columns:
                print("   Calculating knowledge scores from True/False questions...")
                knowledge_scores = []
                for idx, row in df.iterrows():
                    score = 0
                    total = 0
                    
                    # Check for knowledge check columns
                    for col in df.columns:
                        col_lower = str(col).lower()
                        if 'incognito' in col_lower and 'isp' in col_lower:
                            total += 1
                            answer = str(row[col]).strip().lower()
                            if answer in ['false', 'b', 'incorrect', 'no']:
                                score += 1
                        elif 'anonymous' in col_lower and ('trace' in col_lower or 'impossible' in col_lower):
                            total += 1
                            answer = str(row[col]).strip().lower()
                            if answer in ['false', 'b', 'incorrect', 'no']:
                                score += 1
                        elif 'social media' in col_lower and 'messages' in col_lower:
                            total += 1
                            answer = str(row[col]).strip().lower()
                            if answer in ['true', 'a', 'correct', 'yes']:
                                score += 1
                    
                    if total > 0:
                        knowledge_scores.append((score / total) * 100)
                    else:
                        knowledge_scores.append(0)
                
                df['Knowledge_Score'] = knowledge_scores
                df['Score'] = knowledge_scores
                print(f"   Calculated scores: Average = {np.mean(knowledge_scores):.1f}%")
            
            return df
        else:
            print(f"⚠️  Warning: {csv_path} not found. Using sample data.")
            return self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate sample data for training if survey data is not available"""
        np.random.seed(42)
        n_samples = 100
        
        data = {
            'Age_Range': np.random.choice(['18-21', '22-25', '26-30'], n_samples),
            'Gender': np.random.choice(['Male', 'Female', 'Other'], n_samples),
            'Academic_Stream': np.random.choice(['B.Tech', 'BCA', 'B.Sc', 'B.A'], n_samples),
            'Year_of_Study': np.random.choice(['1st year', '2nd year', '3rd year', '4th year'], n_samples),
            'Privacy_Policy_Reading': np.random.choice(['Never', 'Rarely', 'Sometimes', 'Often', 'Always'], n_samples),
            'App_Permissions_Review': np.random.choice(['Never', 'Rarely', 'Sometimes', 'Often', 'Always'], n_samples),
            'Different_Passwords': np.random.choice(['Yes', 'No', 'Sometimes'], n_samples),
            'Knowledge_Score': np.random.randint(0, 100, n_samples)
        }
        
        return pd.DataFrame(data)
    
    def preprocess_data(self, df):
        """Preprocess data for ML model"""
        # Select features
        feature_cols = ['Age_Range', 'Gender', 'Academic_Stream', 'Year_of_Study',
                       'Privacy_Policy_Reading', 'App_Permissions_Review', 'Different_Passwords']
        
        # Filter available columns
        available_cols = [col for col in feature_cols if col in df.columns]
        
        if len(available_cols) == 0:
            print("Warning: No feature columns found. Using sample data.")
            df = self.generate_sample_data()
            available_cols = feature_cols
        
        # Encode categorical variables
        X = df[available_cols].copy()
        
        for col in available_cols:
            if X[col].dtype == 'object':
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
                else:
                    # Handle unseen categories
                    X[col] = X[col].astype(str)
                    known_classes = set(self.label_encoders[col].classes_)
                    X[col] = X[col].apply(lambda x: x if x in known_classes else self.label_encoders[col].classes_[0])
                    X[col] = self.label_encoders[col].transform(X[col])
        
        # Create target variable (knowledge level: Low, Medium, High)
        if 'Knowledge_Score' in df.columns:
            y = pd.cut(df['Knowledge_Score'], bins=[0, 40, 70, 100], labels=['Low', 'Medium', 'High'])
        elif 'Score' in df.columns:
            y = pd.cut(df['Score'], bins=[0, 40, 70, 100], labels=['Low', 'Medium', 'High'])
        else:
            # Generate synthetic target based on features
            y = np.random.choice(['Low', 'Medium', 'High'], len(X))
        
        self.feature_columns = available_cols
        
        return X, y
    
    def train_model(self, X, y):
        """Train the ML model"""
        # Encode target variable
        if 'Knowledge_Level' not in self.label_encoders:
            self.label_encoders['Knowledge_Level'] = LabelEncoder()
        y_encoded = self.label_encoders['Knowledge_Level'].fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
        
        # Train model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Model trained successfully!")
        print(f"Training accuracy: {train_score:.2%}")
        print(f"Test accuracy: {test_score:.2%}")
        
        return self.model
    
    def predict_knowledge_level(self, user_data):
        """Predict knowledge level for a user"""
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        # Prepare user data
        X = pd.DataFrame([user_data])
        
        # Encode features
        for col in self.feature_columns:
            if col in X.columns and col in self.label_encoders:
                X[col] = X[col].astype(str)
                # Handle unseen categories
                known_classes = set(self.label_encoders[col].classes_)
                X[col] = X[col].apply(lambda x: x if x in known_classes else self.label_encoders[col].classes_[0])
                X[col] = self.label_encoders[col].transform(X[col])
        
        # Ensure all feature columns are present
        for col in self.feature_columns:
            if col not in X.columns:
                X[col] = 0
        
        X = X[self.feature_columns]
        
        # Predict
        prediction = self.model.predict(X)[0]
        knowledge_level = self.label_encoders['Knowledge_Level'].inverse_transform([prediction])[0]
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(X)[0]
        confidence = max(probabilities)
        
        return knowledge_level, confidence
    
    def get_recommendations(self, knowledge_level):
        """Get personalized recommendations based on knowledge level"""
        recommendations = {
            'Low': [
                'Review privacy settings on all your social media accounts',
                'Read privacy policies before installing new apps',
                'Use different passwords for different accounts',
                'Learn about data collection practices',
                'Understand how incognito mode works'
            ],
            'Medium': [
                'Regularly review app permissions',
                'Learn about AI ethics and data usage',
                'Understand anonymous data and de-anonymization',
                'Explore advanced privacy tools',
                'Stay updated with privacy news'
            ],
            'High': [
                'Help others understand digital privacy',
                'Explore advanced security practices',
                'Learn about privacy regulations (GDPR, etc.)',
                'Consider privacy-focused alternatives',
                'Contribute to privacy advocacy'
            ]
        }
        
        return recommendations.get(knowledge_level, recommendations['Medium'])
    
    def save_model(self, filepath='ml_model.pkl'):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='ml_model.pkl'):
        """Load a trained model"""
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            self.model = model_data['model']
            self.label_encoders = model_data['label_encoders']
            self.feature_columns = model_data['feature_columns']
            print(f"Model loaded from {filepath}")
            return True
        else:
            print(f"Model file {filepath} not found")
            return False

def train_and_save_model():
    """Main function to train and save the ML model"""
    ml = DigitalAwarenessML()
    
    # Load data
    df = ml.load_survey_data()
    
    # Preprocess
    X, y = ml.preprocess_data(df)
    
    # Train
    ml.train_model(X, y)
    
    # Save
    ml.save_model()
    
    return ml

if __name__ == '__main__':
    print("Training ML model...")
    ml = train_and_save_model()
    print("Model training complete!")

