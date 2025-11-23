"""
Enhanced ML Model Training with Survey Data
Uses real survey responses to improve model accuracy
"""

import pandas as pd
import numpy as np
from ml_model import DigitalAwarenessML
from app import app, db, QuizAttempt, User
import os

def calculate_knowledge_score_from_survey(row):
    """
    Calculate knowledge score from survey responses
    Based on True/False knowledge check questions
    """
    score = 0
    total = 0
    
    # Knowledge Check 1: Incognito mode (False is correct)
    if 'Knowledge_Incognito_ISP' in row:
        total += 1
        answer = str(row['Knowledge_Incognito_ISP']).strip().lower()
        if answer in ['false', 'b', 'incorrect']:
            score += 1
    
    # Knowledge Check 2: Anonymous data (False is correct)
    if 'Knowledge_Anonymous_Trace' in row:
        total += 1
        answer = str(row['Knowledge_Anonymous_Trace']).strip().lower()
        if answer in ['false', 'b', 'incorrect']:
            score += 1
    
    # Knowledge Check 3: Social media messages (True is correct)
    if 'Knowledge_SocialMedia_Messages' in row:
        total += 1
        answer = str(row['Knowledge_SocialMedia_Messages']).strip().lower()
        if answer in ['true', 'a', 'correct']:
            score += 1
    
    return score, total

def prepare_survey_data_for_ml(csv_path='survey_data_backup.csv'):
    """
    Prepare survey data for ML model training
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"📊 Loaded {len(df)} survey responses")
        
        # Column mapping from Analysis.ipynb
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower()
            if 'age' in col_lower and 'range' in col_lower:
                column_mapping[col] = 'Age_Range'
            elif 'gender' in col_lower:
                column_mapping[col] = 'Gender'
            elif ('educational' in col_lower or 'academic' in col_lower) and 'background' in col_lower:
                column_mapping[col] = 'Academic_Stream'
            elif 'level of study' in col_lower or 'year' in col_lower:
                column_mapping[col] = 'Year_of_Study'
            elif 'privacy policy' in col_lower and ('read' in col_lower or 'install' in col_lower):
                column_mapping[col] = 'Privacy_Policy_Reading'
            elif 'app permissions' in col_lower or ('review' in col_lower and 'permissions' in col_lower):
                column_mapping[col] = 'App_Permissions_Review'
            elif 'uninstalled' in col_lower and ('permissions' in col_lower or 'privacy' in col_lower):
                column_mapping[col] = 'Uninstall_Due_Privacy'
            elif 'different passwords' in col_lower:
                column_mapping[col] = 'Different_Passwords'
            elif 'incognito' in col_lower and 'isp' in col_lower:
                column_mapping[col] = 'Knowledge_Incognito_ISP'
            elif 'anonymous' in col_lower and 'trace' in col_lower:
                column_mapping[col] = 'Knowledge_Anonymous_Trace'
            elif 'social media' in col_lower and 'messages' in col_lower:
                column_mapping[col] = 'Knowledge_SocialMedia_Messages'
        
        # Rename columns
        df = df.rename(columns=column_mapping)
        
        # Calculate knowledge scores
        knowledge_scores = []
        for idx, row in df.iterrows():
            score, total = calculate_knowledge_score_from_survey(row)
            if total > 0:
                percentage = (score / total) * 100
                knowledge_scores.append(percentage)
            else:
                knowledge_scores.append(0)
        
        df['Knowledge_Score'] = knowledge_scores
        df['Score'] = knowledge_scores  # Also add as 'Score' for compatibility
        
        print(f"✅ Prepared data with knowledge scores")
        print(f"   Average knowledge score: {np.mean(knowledge_scores):.1f}%")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Survey data file not found: {csv_path}")
        print("   Please ensure the file exists or update the path")
        return None
    except Exception as e:
        print(f"❌ Error preparing data: {e}")
        import traceback
        traceback.print_exc()
        return None

def train_enhanced_model():
    """
    Train ML model with survey data
    """
    print("\n" + "=" * 70)
    print("ENHANCING ML MODEL WITH SURVEY DATA")
    print("=" * 70)
    
    # Prepare survey data
    df = prepare_survey_data_for_ml()
    
    if df is None:
        print("\n⚠️  Using sample data instead")
        df = None
    
    # Initialize and train model
    ml = DigitalAwarenessML()
    
    if df is not None:
        # Use survey data
        X, y = ml.preprocess_data(df)
        print(f"\n📈 Training with {len(X)} real survey responses")
    else:
        # Use sample data
        df = ml.load_survey_data()
        X, y = ml.preprocess_data(df)
        print(f"\n📈 Training with sample data")
    
    # Train model
    ml.train_model(X, y)
    
    # Save model
    ml.save_model('ml_model.pkl')
    
    print("\n✅ Model training complete!")
    print("   Model saved to: ml_model.pkl")
    print("   The application will now use this enhanced model")
    
    return ml

def add_public_datasets():
    """
    Instructions and functions to add public datasets
    """
    print("\n" + "=" * 70)
    print("ADDING PUBLIC DATASETS")
    print("=" * 70)
    
    print("""
    To enhance the model with public datasets, you can:
    
    1. **Privacy Awareness Datasets**:
       - Search for "privacy awareness survey data"
       - "digital literacy datasets"
       - "cybersecurity knowledge datasets"
    
    2. **Academic Sources**:
       - Research papers with survey data
       - University research datasets
       - Published privacy studies
    
    3. **Public Repositories**:
       - Kaggle datasets
       - UCI Machine Learning Repository
       - Google Dataset Search
    
    4. **Format Requirements**:
       - CSV format
       - Should have similar columns (age, gender, privacy behaviors, knowledge scores)
       - Can be mapped to our format using column mapping
    
    Example usage:
        python enhance_model.py --add-dataset path/to/dataset.csv
    """)

if __name__ == '__main__':
    # Train enhanced model
    ml = train_enhanced_model()
    
    # Show instructions for adding more data
    add_public_datasets()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Ensure survey_data_backup.csv is in the project directory")
    print("2. Run: python enhance_model.py")
    print("3. The model will be retrained with your survey data")
    print("4. Add more datasets using the import functions")
    print("=" * 70)

