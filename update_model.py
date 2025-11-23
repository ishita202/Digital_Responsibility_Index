"""
Quick script to update ML model with latest survey data
Run this whenever you have new survey responses
"""

from enhance_model import train_enhanced_model
from import_survey_data import import_survey_data_from_csv
from app import app

def update_all():
    """Update both database and ML model"""
    print("🔄 Updating system with latest survey data...\n")
    
    with app.app_context():
        # Step 1: Import survey data to database
        print("Step 1: Importing survey data...")
        import_survey_data_from_csv()
        
        # Step 2: Retrain ML model
        print("\nStep 2: Retraining ML model...")
        train_enhanced_model()
        
        print("\n✅ Update complete!")
        print("   - Survey data imported to database")
        print("   - ML model retrained with latest data")
        print("   - Application ready to use enhanced model")

if __name__ == '__main__':
    update_all()

