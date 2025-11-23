"""
Setup script for Digital Awareness Platform
Run this script to initialize the database and train the ML model
"""

import os
import sys

def setup_database():
    """Initialize the database"""
    print("Setting up database...")
    from app import app, db
    with app.app_context():
        db.create_all()
        print("✓ Database initialized")
        
        # Create default admin if not exists
        from app import User
        from werkzeug.security import generate_password_hash
        
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin user created (username: admin, password: admin123)")

def train_ml_model():
    """Train the ML model"""
    print("\nTraining ML model...")
    try:
        from ml_model import train_and_save_model
        ml = train_and_save_model()
        print("✓ ML model trained and saved")
        return True
    except Exception as e:
        print(f"⚠ Warning: Could not train ML model: {e}")
        print("The application will still work, but ML features may not be available.")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Digital Awareness Platform - Setup")
    print("=" * 60)
    
    # Setup database
    setup_database()
    
    # Train ML model
    train_ml_model()
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nTo run the application:")
    print("  python app.py")
    print("\nDefault admin credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()

