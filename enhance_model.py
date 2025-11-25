"""
Enhanced ML Model Training with Survey Data
Uses real survey responses to improve model accuracy
"""

import pandas as pd
import numpy as np
from ml_model import DigitalAwarenessML
from app import app, db, QuizAttempt, User
import os


def load_primary_survey_dataframe(
    csv_path='survey_data_backup.csv',
    excel_path='Project Survey (Responses).xlsx'
):
    """
    Load survey responses from CSV, or convert from Excel if needed.
    """
    if os.path.exists(csv_path):
        print(f"[INFO] Loading survey CSV: {csv_path}")
        return pd.read_csv(csv_path)

    if os.path.exists(excel_path):
        print(f"[INFO] Converting Excel survey file '{excel_path}' to CSV")
        try:
            df = pd.read_excel(excel_path)
        except ImportError as exc:
            raise ImportError(
                "Reading Excel files requires the 'openpyxl' package. "
                "Install it with 'pip install openpyxl' and re-run the script."
            ) from exc
        df.to_csv(csv_path, index=False)
        print(f"[INFO] Saved converted CSV to {csv_path}")
        return df

    raise FileNotFoundError(
        f"No survey sources found. Missing '{csv_path}' and '{excel_path}'."
    )

def interpret_boolean_response(value):
    """
    Normalize survey responses (textual or numeric) to boolean True/False.
    Returns None when the value cannot be interpreted.
    """
    if pd.isna(value):
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value == 1:
            return True
        if value == 0:
            return False

    normalized = str(value).strip().lower()
    true_tokens = {'true', 't', 'a', 'correct', 'yes', 'y', '1', '1.0'}
    false_tokens = {'false', 'f', 'b', 'incorrect', 'no', 'n', '0', '0.0'}

    if normalized in true_tokens:
        return True
    if normalized in false_tokens:
        return False

    return None


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
        answer = interpret_boolean_response(row['Knowledge_Incognito_ISP'])
        if answer is False:
            score += 1
    
    # Knowledge Check 2: Anonymous data (False is correct)
    if 'Knowledge_Anonymous_Trace' in row:
        total += 1
        answer = interpret_boolean_response(row['Knowledge_Anonymous_Trace'])
        if answer is False:
            score += 1
    
    # Knowledge Check 3: Social media messages (True is correct)
    if 'Knowledge_SocialMedia_Messages' in row:
        total += 1
        answer = interpret_boolean_response(row['Knowledge_SocialMedia_Messages'])
        if answer is True:
            score += 1
    
    return score, total

def prepare_survey_data_for_ml(csv_path='survey_data_backup.csv'):
    """
    Prepare survey data for ML model training
    """
    try:
        df = load_primary_survey_dataframe(csv_path=csv_path)
        print(f"[INFO] Loaded {len(df)} survey responses")
        
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
        
        print("[INFO] Prepared data with knowledge scores")
        print(f"   Average knowledge score: {np.mean(knowledge_scores):.1f}%")
        
        return df
        
    except FileNotFoundError:
        print(f"[ERROR] Survey data file not found: {csv_path}")
        print("   Please ensure the file exists or update the path")
        return None
    except Exception as e:
        print(f"[ERROR] Error preparing data: {e}")
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
        print("\n[WARN] Using sample data instead")
        df = None
    
    # Initialize and train model
    ml = DigitalAwarenessML()
    
    if df is not None:
        # Use survey data
        X, y = ml.preprocess_data(df)
        print(f"\n[INFO] Training with {len(X)} real survey responses")
    else:
        # Use sample data
        df = ml.load_survey_data()
        X, y = ml.preprocess_data(df)
        print("\n[INFO] Training with sample data")
    
    # Train model
    ml.train_model(X, y)
    
    # Save model
    ml.save_model('ml_model.pkl')
    
    print("\n[INFO] Model training complete!")
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

