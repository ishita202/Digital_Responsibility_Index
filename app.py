from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import gspread
from google.oauth2.service_account import Credentials
import os
import json
import pickle
import pytz
from functools import wraps

# Import ML model
try:
    from ml_model import DigitalAwarenessML
    ml_model_available = True
except ImportError:
    ml_model_available = False
    print("Warning: ML model module not available")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_awareness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Timezone configuration - Change this to your country's timezone
# Common timezones: 'Asia/Kolkata' (India), 'America/New_York' (US Eastern), 
# 'Europe/London' (UK), 'Asia/Dubai' (UAE), etc.
# List of all timezones: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
DEFAULT_TIMEZONE = 'Asia/Kolkata'  # Change this to your timezone

def get_local_timezone():
    """Get the local timezone, defaulting to configured timezone"""
    try:
        return pytz.timezone(DEFAULT_TIMEZONE)
    except:
        # Fallback to UTC if timezone is invalid
        return pytz.UTC

def utc_to_local(utc_dt):
    """Convert UTC datetime to local timezone"""
    if utc_dt is None:
        return None
    if utc_dt.tzinfo is None:
        # Assume it's UTC if no timezone info
        utc_dt = pytz.UTC.localize(utc_dt)
    local_tz = get_local_timezone()
    return utc_dt.astimezone(local_tz)

# Jinja2 filter for timezone conversion
@app.template_filter('localtime')
def localtime_filter(dt):
    """Jinja2 filter to convert UTC to local time"""
    if dt is None:
        return None
    local_dt = utc_to_local(dt)
    return local_dt.strftime('%Y-%m-%d %H:%M')

@app.template_filter('localtime_date')
def localtime_date_filter(dt):
    """Jinja2 filter to convert UTC to local time (date only)"""
    if dt is None:
        return None
    local_dt = utc_to_local(dt)
    return local_dt.strftime('%Y-%m-%d')

@app.template_filter('localtime_time')
def localtime_time_filter(dt):
    """Jinja2 filter to convert UTC to local time (time only)"""
    if dt is None:
        return None
    local_dt = utc_to_local(dt)
    return local_dt.strftime('%H:%M')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Google Sheets Configuration
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1ZoZ7ZQXVLnk5JokphSQK0tqIT9IshB2NCg9_UCiAw6s/edit?gid=1620608954#gid=1620608954'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Initialize ML Model (will be loaded when needed)
ml_model = None

def get_ml_model():
    """Get or initialize ML model"""
    global ml_model
    if ml_model is not None:
        return ml_model
    
    if not ml_model_available:
        return None
    
    try:
        ml_model = DigitalAwarenessML()
        if os.path.exists('ml_model.pkl'):
            if ml_model.load_model('ml_model.pkl'):
                return ml_model
        # If model doesn't exist, try to train it
        print("ML model not found. Training new model...")
        df = ml_model.load_survey_data()
        if df is not None and len(df) > 0:
            X, y = ml_model.preprocess_data(df)
            ml_model.train_model(X, y)
            ml_model.save_model()
            return ml_model
    except Exception as e:
        print(f"Error initializing ML model: {e}")
        ml_model = None
    
    return None

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile information
    age_range = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    academic_stream = db.Column(db.String(200))
    year_of_study = db.Column(db.String(50))
    
    # Relationships
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True)
    activities = db.relationship('UserActivity', backref='user', lazy=True)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    category = db.Column(db.String(100))  # Privacy, AI Ethics, Data Security, etc.
    quiz_type = db.Column(db.String(100), default='General')  # Privacy Basics, Security Fundamentals, AI Ethics, etc.
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='Medium')  # Easy, Medium, Hard
    time_limit = db.Column(db.Integer, default=60)  # Time limit in seconds per question
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QuizType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Font Awesome icon class
    color = db.Column(db.String(20))  # Bootstrap color class
    time_limit = db.Column(db.Integer, default=300)  # Total time limit in seconds
    question_count = db.Column(db.Integer, default=5)  # Number of questions
    difficulty = db.Column(db.String(20), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_type = db.Column(db.String(100))  # Type of quiz taken
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    time_taken = db.Column(db.Integer)  # Time taken in seconds
    time_limit = db.Column(db.Integer)  # Time limit in seconds
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.Column(db.Text)  # JSON string of answers

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # login, quiz_completed, resource_viewed, etc.
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LearningResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    resource_type = db.Column(db.String(50))  # article, video, course, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database
with app.app_context():
    db.create_all()
    
    # Migrate existing database - add new columns if they don't exist
    try:
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        
        # Check if tables exist
        tables = inspector.get_table_names()
        
        if 'quiz_question' in tables:
            quiz_question_columns = [col['name'] for col in inspector.get_columns('quiz_question')]
            
            # Add quiz_type and time_limit to QuizQuestion if missing
            if 'quiz_type' not in quiz_question_columns:
                db.session.execute(text('ALTER TABLE quiz_question ADD COLUMN quiz_type VARCHAR(100) DEFAULT "General"'))
                db.session.commit()
                print("Added quiz_type column to quiz_question")
            
            if 'time_limit' not in quiz_question_columns:
                db.session.execute(text('ALTER TABLE quiz_question ADD COLUMN time_limit INTEGER DEFAULT 60'))
                db.session.commit()
                print("Added time_limit column to quiz_question")
        
        if 'quiz_attempt' in tables:
            quiz_attempt_columns = [col['name'] for col in inspector.get_columns('quiz_attempt')]
            
            # Add quiz_type, time_taken, time_limit to QuizAttempt if missing
            if 'quiz_type' not in quiz_attempt_columns:
                db.session.execute(text('ALTER TABLE quiz_attempt ADD COLUMN quiz_type VARCHAR(100)'))
                db.session.commit()
                print("Added quiz_type column to quiz_attempt")
            
            if 'time_taken' not in quiz_attempt_columns:
                db.session.execute(text('ALTER TABLE quiz_attempt ADD COLUMN time_taken INTEGER'))
                db.session.commit()
                print("Added time_taken column to quiz_attempt")
            
            if 'time_limit' not in quiz_attempt_columns:
                db.session.execute(text('ALTER TABLE quiz_attempt ADD COLUMN time_limit INTEGER'))
                db.session.commit()
                print("Added time_limit column to quiz_attempt")
    except Exception as e:
        print(f"Migration note: {e}")
        # If migration fails, you may need to delete database and recreate
        print("If errors persist, delete digital_awareness.db and restart the app")
    
    # Create default admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
    
    # Add quiz types if none exist
    if QuizType.query.count() == 0:
        quiz_types = [
            QuizType(
                name="Privacy Basics",
                description="Test your knowledge about digital privacy fundamentals. Learn how to protect your personal information online.",
                icon="fa-shield-alt",
                color="primary",
                time_limit=300,  # 5 minutes
                question_count=5,
                difficulty="Easy"
            ),
            QuizType(
                name="Data Security",
                description="Master password security, encryption, and data protection practices. Essential for keeping your data safe.",
                icon="fa-lock",
                color="success",
                time_limit=360,  # 6 minutes
                question_count=6,
                difficulty="Medium"
            ),
            QuizType(
                name="AI Ethics",
                description="Understand ethical considerations in artificial intelligence, data collection, and algorithmic decision-making.",
                icon="fa-robot",
                color="info",
                time_limit=420,  # 7 minutes
                question_count=7,
                difficulty="Hard"
            ),
            QuizType(
                name="Social Media Privacy",
                description="Learn about privacy settings, data sharing, and how social media platforms use your information.",
                icon="fa-share-alt",
                color="warning",
                time_limit=300,  # 5 minutes
                question_count=5,
                difficulty="Medium"
            ),
            QuizType(
                name="Quick Challenge",
                description="Fast-paced quiz with time pressure. Test your knowledge under time constraints!",
                icon="fa-bolt",
                color="danger",
                time_limit=180,  # 3 minutes
                question_count=5,
                difficulty="Medium"
            ),
        ]
        for qt in quiz_types:
            db.session.add(qt)
        db.session.commit()
    
    # Add sample quiz questions if none exist
    if QuizQuestion.query.count() == 0:
        sample_questions = [
            # Privacy Basics Questions
            QuizQuestion(
                question_text="Incognito mode hides your browsing history from your Internet Service Provider (ISP).",
                option_a="True",
                option_b="False",
                option_c="Partially True",
                option_d="Depends on the browser",
                correct_answer="B",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="Incognito mode only prevents your browser from storing history locally. Your ISP can still see your browsing activity.",
                difficulty="Easy",
                time_limit=45
            ),
            QuizQuestion(
                question_text="What is the primary purpose of a privacy policy?",
                option_a="To protect user data",
                option_b="To inform users how their data is collected and used",
                option_c="To prevent data breaches",
                option_d="To comply with advertising requirements",
                correct_answer="B",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="Privacy policies are meant to inform users about data collection and usage practices.",
                difficulty="Easy",
                time_limit=40
            ),
            QuizQuestion(
                question_text="Which of the following is NOT a privacy best practice?",
                option_a="Reading privacy policies before signing up",
                option_b="Sharing passwords with trusted friends",
                option_c="Reviewing app permissions regularly",
                option_d="Using two-factor authentication",
                correct_answer="B",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="Never share passwords, even with trusted friends. This is a security risk.",
                difficulty="Easy",
                time_limit=35
            ),
            QuizQuestion(
                question_text="What does 'cookies' refer to in web browsing?",
                option_a="Small text files stored on your device",
                option_b="Security certificates",
                option_c="Browser extensions",
                option_d="Encrypted passwords",
                correct_answer="A",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="Cookies are small text files that websites store on your device to remember information.",
                difficulty="Easy",
                time_limit=40
            ),
            QuizQuestion(
                question_text="Should you accept all cookies when visiting a website?",
                option_a="Yes, always",
                option_b="No, only accept necessary cookies",
                option_c="It doesn't matter",
                option_d="Only on trusted sites",
                correct_answer="B",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="Only accept necessary cookies. Optional cookies are often used for tracking and advertising.",
                difficulty="Medium",
                time_limit=45
            ),
            # Data Security Questions
            QuizQuestion(
                question_text="What is the best practice for password security?",
                option_a="Use the same password everywhere",
                option_b="Use different passwords for different accounts",
                option_c="Write passwords in a notebook",
                option_d="Share passwords with friends",
                correct_answer="B",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Using unique passwords for each account prevents a single breach from compromising all your accounts.",
                difficulty="Easy",
                time_limit=30
            ),
            QuizQuestion(
                question_text="How often should you review app permissions on your phone?",
                option_a="Never",
                option_b="Once a year",
                option_c="Every few months",
                option_d="When installing new apps",
                correct_answer="C",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Regularly reviewing app permissions helps ensure apps only have access to data they need.",
                difficulty="Easy",
                time_limit=35
            ),
            QuizQuestion(
                question_text="What is two-factor authentication (2FA)?",
                option_a="Using two different passwords",
                option_b="Verifying identity using two different methods",
                option_c="Having two email accounts",
                option_d="Using two different browsers",
                correct_answer="B",
                category="Data Security",
                quiz_type="Data Security",
                explanation="2FA requires two different authentication methods, like password + SMS code or biometric.",
                difficulty="Medium",
                time_limit=40
            ),
            QuizQuestion(
                question_text="What makes a strong password?",
                option_a="Using your name and birthdate",
                option_b="A mix of uppercase, lowercase, numbers, and symbols",
                option_c="A common word with numbers",
                option_d="Your pet's name",
                correct_answer="B",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Strong passwords use a mix of character types and are not easily guessable.",
                difficulty="Easy",
                time_limit=35
            ),
            QuizQuestion(
                question_text="What should you do if you suspect a data breach?",
                option_a="Ignore it",
                option_b="Change passwords immediately and monitor accounts",
                option_c="Share it on social media",
                option_d="Wait and see",
                correct_answer="B",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Immediately change passwords and monitor your accounts for suspicious activity.",
                difficulty="Medium",
                time_limit=40
            ),
            QuizQuestion(
                question_text="What is encryption?",
                option_a="Hiding files on your computer",
                option_b="Converting data into a code to prevent unauthorized access",
                option_c="Deleting old files",
                option_d="Backing up data",
                correct_answer="B",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Encryption converts readable data into coded format that can only be read with a key.",
                difficulty="Medium",
                time_limit=45
            ),
            # AI Ethics Questions
            QuizQuestion(
                question_text="Data described as 'anonymous' in privacy policies is impossible to trace back to you.",
                option_a="True",
                option_b="False",
                option_c="Sometimes True",
                option_d="Not specified",
                correct_answer="B",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="Anonymous data can often be de-anonymized using various techniques, especially when combined with other data sources.",
                difficulty="Hard",
                time_limit=60
            ),
            QuizQuestion(
                question_text="Should AI tools be allowed to analyze students' social media posts to detect mental health issues?",
                option_a="Yes, always",
                option_b="No, never",
                option_c="Only with explicit consent",
                option_d="Only for research purposes",
                correct_answer="C",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="AI analysis of personal data should require explicit consent and clear purpose.",
                difficulty="Hard",
                time_limit=60
            ),
            QuizQuestion(
                question_text="Who should be held accountable if AI algorithms make incorrect decisions?",
                option_a="Only the AI system",
                option_b="Only the developers",
                option_c="The organization using the AI",
                option_d="Multiple parties including developers and users",
                correct_answer="D",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="Accountability for AI decisions should be shared among developers, organizations, and users.",
                difficulty="Hard",
                time_limit=65
            ),
            QuizQuestion(
                question_text="Can AI algorithms have bias?",
                option_a="No, AI is always objective",
                option_b="Yes, if trained on biased data",
                option_c="Only in certain cases",
                option_d="Bias doesn't matter",
                correct_answer="B",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="AI can inherit bias from training data, making it crucial to use diverse, representative datasets.",
                difficulty="Medium",
                time_limit=50
            ),
            QuizQuestion(
                question_text="What is algorithmic transparency?",
                option_a="Making AI code public",
                option_b="Understanding how AI makes decisions",
                option_c="Using clear variable names",
                option_d="Documenting code",
                correct_answer="B",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="Algorithmic transparency means understanding how AI systems make their decisions.",
                difficulty="Hard",
                time_limit=60
            ),
            QuizQuestion(
                question_text="Should companies use your search history to serve targeted ads?",
                option_a="Yes, always",
                option_b="No, never",
                option_c="Only with consent",
                option_d="It doesn't matter",
                correct_answer="C",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="Using personal data for advertising should require user consent and transparency.",
                difficulty="Medium",
                time_limit=50
            ),
            QuizQuestion(
                question_text="What is the main concern with AI in education?",
                option_a="AI is too expensive",
                option_b="Privacy, bias, and fairness",
                option_c="AI is too slow",
                option_d="AI doesn't work",
                correct_answer="B",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="Main concerns include student privacy, algorithmic bias, and ensuring fair treatment.",
                difficulty="Medium",
                time_limit=50
            ),
            # Social Media Privacy Questions
            QuizQuestion(
                question_text="Social media platforms are allowed to analyze private messages to target ads.",
                option_a="True",
                option_b="False",
                option_c="Only with consent",
                option_d="Only for security",
                correct_answer="A",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="Most social media platforms' terms of service allow them to analyze private messages for ad targeting and other purposes.",
                difficulty="Medium",
                time_limit=45
            ),
            QuizQuestion(
                question_text="How often should you review privacy settings on social media?",
                option_a="Never",
                option_b="Once when you sign up",
                option_c="Regularly, as settings change",
                option_d="Only if there's a problem",
                correct_answer="C",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="Privacy settings change frequently, so regular reviews are important.",
                difficulty="Easy",
                time_limit=35
            ),
            QuizQuestion(
                question_text="What information should you avoid sharing publicly on social media?",
                option_a="Everything",
                option_b="Personal details like address, phone number, birthdate",
                option_c="Only photos",
                option_d="Nothing, it's all safe",
                correct_answer="B",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="Avoid sharing sensitive personal information that could be used for identity theft or stalking.",
                difficulty="Easy",
                time_limit=35
            ),
            QuizQuestion(
                question_text="Can you completely delete your data from social media platforms?",
                option_a="Yes, always",
                option_b="No, some data may be retained",
                option_c="Only if you pay",
                option_d="It depends on the platform",
                correct_answer="B",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="Many platforms retain some data even after account deletion, as stated in their privacy policies.",
                difficulty="Medium",
                time_limit=45
            ),
            QuizQuestion(
                question_text="What does 'public profile' mean on social media?",
                option_a="Anyone can see your posts",
                option_b="Only friends can see",
                option_c="Only you can see",
                option_d="Only verified users",
                correct_answer="A",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="A public profile means anyone on the internet can view your posts and information.",
                difficulty="Easy",
                time_limit=30
            )
        ]
        for q in sample_questions:
            db.session.add(q)
        db.session.commit()
    
    # Add sample learning resources
    if LearningResource.query.count() == 0:
        resources = [
            LearningResource(
                title="Understanding Digital Privacy",
                description="A comprehensive guide to digital privacy and data protection",
                url="https://example.com/privacy-guide",
                category="Privacy",
                resource_type="article"
            ),
            LearningResource(
                title="AI Ethics in Education",
                description="Learn about ethical considerations when using AI in educational settings",
                url="https://example.com/ai-ethics",
                category="AI Ethics",
                resource_type="article"
            ),
            LearningResource(
                title="Data Security Best Practices",
                description="Essential tips for protecting your personal data online",
                url="https://example.com/data-security",
                category="Data Security",
                resource_type="video"
            )
        ]
        for r in resources:
            db.session.add(r)
        db.session.commit()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            age_range=request.form.get('age_range'),
            gender=request.form.get('gender'),
            academic_stream=request.form.get('academic_stream'),
            year_of_study=request.form.get('year_of_study')
        )
        db.session.add(user)
        db.session.commit()
        
        # Log activity
        activity = UserActivity(
            user_id=user.id,
            activity_type='registration',
            description=f'User {username} registered'
        )
        db.session.add(activity)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            
            # Log activity
            activity = UserActivity(
                user_id=user.id,
                activity_type='login',
                description=f'User {username} logged in'
            )
            db.session.add(activity)
            db.session.commit()
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    activity = UserActivity(
        user_id=current_user.id,
        activity_type='logout',
        description=f'User {current_user.username} logged out'
    )
    db.session.add(activity)
    db.session.commit()
    
    logout_user()
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    """User home/explore page with featured content and recommendations"""
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get user statistics
    total_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).count()
    recent_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.completed_at.desc()).limit(5).all()
    
    # Calculate average score
    attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
    avg_score = np.mean([a.percentage for a in attempts]) if attempts else 0
    
    # Get recent activities
    recent_activities = UserActivity.query.filter_by(user_id=current_user.id).order_by(UserActivity.created_at.desc()).limit(5).all()
    
    # Get personalized recommendations
    recommendations = []
    ml = get_ml_model()
    if ml and current_user:
        try:
            user_data = {
                'Age_Range': current_user.age_range or '18-21',
                'Gender': current_user.gender or 'Male',
                'Academic_Stream': current_user.academic_stream or 'B.Tech',
                'Year_of_Study': current_user.year_of_study or '2nd year',
                'Privacy_Policy_Reading': 'Sometimes',
                'App_Permissions_Review': 'Sometimes',
                'Different_Passwords': 'Yes'
            }
            
            if attempts:
                avg_score_val = np.mean([a.percentage for a in attempts])
                if avg_score_val < 40:
                    user_data['Privacy_Policy_Reading'] = 'Never'
                    user_data['App_Permissions_Review'] = 'Never'
                elif avg_score_val >= 70:
                    user_data['Privacy_Policy_Reading'] = 'Often'
                    user_data['App_Permissions_Review'] = 'Often'
            
            knowledge_level, confidence = ml.predict_knowledge_level(user_data)
            recommendations = ml.get_recommendations(knowledge_level)
        except Exception as e:
            print(f"Error getting ML recommendations: {e}")
    
    # Get featured resources
    featured_resources = LearningResource.query.limit(3).all()
    resources_count = LearningResource.query.count()
    
    # Calculate streak (simplified - days with activity)
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    streak = 0
    check_date = today
    # Check up to 30 days back for streak
    for i in range(30):
        day_activities = UserActivity.query.filter(
            UserActivity.user_id == current_user.id,
            db.func.date(UserActivity.created_at) == check_date
        ).first()
        if day_activities:
            streak += 1
            check_date = check_date - timedelta(days=1)
        else:
            break
    
    return render_template('home.html',
                         total_attempts=total_attempts,
                         recent_attempts=recent_attempts,
                         avg_score=avg_score,
                         recent_activities=recent_activities,
                         recommendations=recommendations,
                         featured_resources=featured_resources,
                         resources_count=resources_count,
                         current_streak=streak)

@app.route('/dashboard')
@login_required
def dashboard():
    """Detailed analytics dashboard"""
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get user statistics
    total_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).count()
    recent_attempts = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.completed_at.desc()).limit(5).all()
    
    # Calculate average score
    attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
    avg_score = np.mean([a.percentage for a in attempts]) if attempts else 0
    
    # Get recent activities
    recent_activities = UserActivity.query.filter_by(user_id=current_user.id).order_by(UserActivity.created_at.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                         total_attempts=total_attempts,
                         recent_attempts=recent_attempts,
                         avg_score=avg_score,
                         recent_activities=recent_activities)

@app.route('/profile')
@login_required
def profile():
    attempts = QuizAttempt.query.filter_by(user_id=current_user.id).order_by(QuizAttempt.completed_at.desc()).all()
    return render_template('profile.html', attempts=attempts)

@app.route('/learn')
@login_required
def learn():
    resources = LearningResource.query.all()
    
    # Get personalized recommendations using ML model
    recommendations = []
    ml = get_ml_model()
    if ml and current_user:
        try:
            # Prepare user data for prediction
            user_data = {
                'Age_Range': current_user.age_range or '18-21',
                'Gender': current_user.gender or 'Male',
                'Academic_Stream': current_user.academic_stream or 'B.Tech',
                'Year_of_Study': current_user.year_of_study or '2nd year',
                'Privacy_Policy_Reading': 'Sometimes',  # Default values
                'App_Permissions_Review': 'Sometimes',
                'Different_Passwords': 'Yes'
            }
            
            # Get user's average quiz score
            attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
            if attempts:
                avg_score = np.mean([a.percentage for a in attempts])
                if avg_score < 40:
                    user_data['Privacy_Policy_Reading'] = 'Never'
                    user_data['App_Permissions_Review'] = 'Never'
                elif avg_score < 70:
                    user_data['Privacy_Policy_Reading'] = 'Sometimes'
                    user_data['App_Permissions_Review'] = 'Sometimes'
                else:
                    user_data['Privacy_Policy_Reading'] = 'Often'
                    user_data['App_Permissions_Review'] = 'Often'
            
            knowledge_level, confidence = ml.predict_knowledge_level(user_data)
            recommendations = ml.get_recommendations(knowledge_level)
        except Exception as e:
            print(f"Error getting ML recommendations: {e}")
            recommendations = [
                'Review privacy settings on all your social media accounts',
                'Read privacy policies before installing new apps',
                'Use different passwords for different accounts'
            ]
    
    return render_template('learn.html', resources=resources, recommendations=recommendations)

@app.route('/quiz')
@login_required
def quiz_select():
    """Quiz selection page - choose quiz type"""
    quiz_types = QuizType.query.all()
    return render_template('quiz_select.html', quiz_types=quiz_types)

@app.route('/quiz/<quiz_type_name>')
@login_required
def quiz(quiz_type_name):
    """Take a specific quiz type"""
    quiz_type = QuizType.query.filter_by(name=quiz_type_name).first_or_404()
    questions = QuizQuestion.query.filter_by(quiz_type=quiz_type_name).limit(quiz_type.question_count).all()
    
    if not questions:
        flash('No questions available for this quiz type.')
        return redirect(url_for('quiz_select'))
    
    return render_template('quiz.html', questions=questions, quiz_type=quiz_type)

@app.route('/submit_quiz', methods=['POST'])
@login_required
def submit_quiz():
    data = request.json
    answers = data.get('answers', {})
    quiz_type = data.get('quiz_type', 'General')
    time_taken = data.get('time_taken', 0)
    time_limit = data.get('time_limit', 0)
    
    # Get questions for this quiz type
    question_ids = list(answers.keys())
    questions = QuizQuestion.query.filter(QuizQuestion.id.in_(question_ids)).all()
    
    score = 0
    total = len(questions)
    
    for q in questions:
        user_answer = answers.get(str(q.id))
        if user_answer == q.correct_answer:
            score += 1
    
    percentage = (score / total * 100) if total > 0 else 0
    
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_type=quiz_type,
        score=score,
        total_questions=total,
        percentage=percentage,
        time_taken=time_taken,
        time_limit=time_limit,
        answers=json.dumps(answers)
    )
    db.session.add(attempt)
    
    # Log activity
    activity = UserActivity(
        user_id=current_user.id,
        activity_type='quiz_completed',
        description=f'Completed {quiz_type} quiz with {score}/{total} correct answers ({percentage:.1f}%)'
    )
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({
        'score': score,
        'total': total,
        'percentage': percentage,
        'time_taken': time_taken
    })

@app.route('/admin/update_model', methods=['POST'])
@login_required
def update_model():
    """Admin endpoint to retrain ML model with latest data"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        from enhance_model import train_enhanced_model
        ml = train_enhanced_model()
        return jsonify({'success': True, 'message': 'Model updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('dashboard'))
    
    # Analytics
    total_users = User.query.count()
    total_quizzes = QuizAttempt.query.count()
    total_activities = UserActivity.query.count()
    
    # Recent activities
    recent_activities = UserActivity.query.order_by(UserActivity.created_at.desc()).limit(20).all()
    
    # User statistics
    users = User.query.all()
    user_stats = []
    for user in users:
        attempts = QuizAttempt.query.filter_by(user_id=user.id).all()
        avg_score = np.mean([a.percentage for a in attempts]) if attempts else 0
        user_stats.append({
            'username': user.username,
            'total_attempts': len(attempts),
            'avg_score': avg_score,
            'last_activity': UserActivity.query.filter_by(user_id=user.id).order_by(UserActivity.created_at.desc()).first()
        })
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_quizzes=total_quizzes,
                         total_activities=total_activities,
                         recent_activities=recent_activities,
                         user_stats=user_stats)

@app.route('/api/analytics')
@login_required
def analytics():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    # Daily activity
    activities = UserActivity.query.all()
    daily_activity = {}
    for activity in activities:
        date = activity.created_at.date()
        daily_activity[date] = daily_activity.get(date, 0) + 1
    
        # Quiz performance over time (convert to local timezone)
        attempts = QuizAttempt.query.order_by(QuizAttempt.completed_at).all()
        quiz_performance = {}
        for attempt in attempts:
            local_dt = utc_to_local(attempt.completed_at)
            date = local_dt.date()
            if date not in quiz_performance:
                quiz_performance[date] = []
            quiz_performance[date].append(attempt.percentage)
    
    quiz_avg = {str(k): np.mean(v) for k, v in quiz_performance.items()}
    
    return jsonify({
        'daily_activity': {str(k): v for k, v in daily_activity.items()},
        'quiz_performance': quiz_avg
    })

@app.route('/api/recommendations')
@login_required
def get_recommendations():
    """Get personalized recommendations for the current user"""
    ml = get_ml_model()
    if not ml:
        return jsonify({'error': 'ML model not available'}), 503
    
    try:
        # Prepare user data
        user_data = {
            'Age_Range': current_user.age_range or '18-21',
            'Gender': current_user.gender or 'Male',
            'Academic_Stream': current_user.academic_stream or 'B.Tech',
            'Year_of_Study': current_user.year_of_study or '2nd year',
            'Privacy_Policy_Reading': 'Sometimes',
            'App_Permissions_Review': 'Sometimes',
            'Different_Passwords': 'Yes'
        }
        
        # Adjust based on quiz performance
        attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
        if attempts:
            avg_score = np.mean([a.percentage for a in attempts])
            if avg_score < 40:
                user_data['Privacy_Policy_Reading'] = 'Never'
                user_data['App_Permissions_Review'] = 'Never'
            elif avg_score >= 70:
                user_data['Privacy_Policy_Reading'] = 'Often'
                user_data['App_Permissions_Review'] = 'Often'
        
        knowledge_level, confidence = ml.predict_knowledge_level(user_data)
        recommendations = ml.get_recommendations(knowledge_level)
        
        return jsonify({
            'knowledge_level': knowledge_level,
            'confidence': float(confidence),
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

