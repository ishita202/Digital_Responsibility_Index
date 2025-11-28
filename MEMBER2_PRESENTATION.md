# Member 2: System Architect (Backend & Security) - Presentation Guide

## Overview
As the System Architect, I am responsible for the server infrastructure, database design, and security implementation of the Digital Responsibility Index platform. This document outlines the technical architecture and implementation details.

---

## 1. Architecture: MVC Pattern with Flask

### 1.1 What is MVC Pattern?

**MVC (Model-View-Controller)** is a software architectural pattern that separates an application into three interconnected components:

- **Model**: Represents the data and business logic
- **View**: Handles the presentation layer (user interface)
- **Controller**: Manages user input and coordinates between Model and View

### 1.2 MVC Implementation in Our Flask Application

#### **Model Layer** (`app.py` - Lines 271-343)
The Model layer consists of SQLAlchemy database models that represent our data structure:

```python
# Example: User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Relationships
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True)
```

**Key Models:**
- `User`: User accounts and authentication
- `QuizQuestion`: Quiz questions and answers
- `QuizAttempt`: User quiz attempts and scores
- `LearningResource`: Educational content
- `UserActivity`: Activity logging
- `QuizType`: Quiz categories

#### **View Layer** (`templates/` directory)
The View layer consists of HTML templates that render the user interface:

- `base.html`: Base template with navigation
- `index.html`: Landing page
- `login.html`, `register.html`: Authentication pages
- `dashboard.html`: User dashboard
- `quiz.html`: Quiz interface
- `admin_dashboard.html`: Admin panel

**Template Rendering Example:**
```python
@app.route('/dashboard')
@login_required
def dashboard():
    attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', attempts=attempts)
```

#### **Controller Layer** (`app.py` - Routes)
The Controller layer consists of Flask route handlers that process requests:

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')
```

**Controller Responsibilities:**
- Handle HTTP requests (GET, POST)
- Validate user input
- Interact with Models (database queries)
- Render Views (templates)
- Manage business logic

### 1.3 Flask Application Structure

```python
# Flask App Initialization (app.py - Lines 30-34)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_awareness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database and Login Manager Setup (Lines 84-87)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
```

**Key Components:**
- **Flask App**: Main application instance
- **SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **Werkzeug**: Security utilities (password hashing)

---

## 2. Database: SQLite Schema & SQLAlchemy ORM

### 2.1 Database Choice: SQLite

**Why SQLite?**
- Lightweight and file-based (no separate server needed)
- Perfect for small to medium applications
- Zero configuration
- ACID compliant
- Suitable for development and deployment

**Database Location:**
- File: `instance/digital_awareness.db`
- Created automatically on first run

### 2.2 SQLAlchemy ORM (Object-Relational Mapping)

**What is ORM?**
ORM allows us to interact with the database using Python objects instead of writing raw SQL queries.

**Benefits:**
- Type safety
- Code reusability
- Database-agnostic (can switch from SQLite to PostgreSQL easily)
- Automatic relationship management

### 2.3 Database Schema

#### **2.3.1 User Table**

```python
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
```

**Table Structure:**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key (auto-increment) |
| username | String(80) | Unique username |
| email | String(120) | Unique email address |
| password_hash | String(255) | Hashed password (Werkzeug) |
| is_admin | Boolean | Admin role flag |
| created_at | DateTime | Registration timestamp |
| age_range | String(50) | User age range |
| gender | String(50) | User gender |
| academic_stream | String(200) | Academic field |
| year_of_study | String(50) | Current year |

**Relationships:**
- One User → Many QuizAttempts
- One User → Many UserActivities

#### **2.3.2 QuizAttempt Table**

```python
class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_type = db.Column(db.String(100))
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    time_taken = db.Column(db.Integer)  # Time in seconds
    time_limit = db.Column(db.Integer)  # Time limit in seconds
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.Column(db.Text)  # JSON string of answers
```

**Table Structure:**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| quiz_type | String(100) | Type of quiz taken |
| score | Integer | Correct answers count |
| total_questions | Integer | Total questions |
| percentage | Float | Score percentage |
| time_taken | Integer | Time taken (seconds) |
| time_limit | Integer | Time limit (seconds) |
| completed_at | DateTime | Completion timestamp |
| answers | Text (JSON) | User's answers (JSON format) |

#### **2.3.3 LearningResource Table**

```python
class LearningResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    resource_type = db.Column(db.String(50))  # article, video, course
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Table Structure:**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| title | String(200) | Resource title |
| description | Text | Resource description |
| url | String(500) | Resource URL |
| category | String(100) | Resource category |
| resource_type | String(50) | Type (article/video/course) |
| created_at | DateTime | Creation timestamp |

### 2.4 Database Relationships (Entity Relationship Model)

```
User (1) ──────< (Many) QuizAttempt
User (1) ──────< (Many) UserActivity
QuizQuestion (Many) ────< (Many) QuizAttempt (via JSON answers)
```

**Relationship Types:**
- **One-to-Many**: One user can have many quiz attempts
- **One-to-Many**: One user can have many activities
- **Many-to-Many**: Questions linked to attempts via JSON

### 2.5 Database Initialization

```python
# Database creation (app.py - Lines 349-350)
with app.app_context():
    db.create_all()  # Creates all tables if they don't exist
```

**Automatic Features:**
- Tables created on first run
- Default admin user created
- Sample quiz questions added
- Quiz types initialized

### 2.6 SQLAlchemy Query Examples

**Querying Users:**
```python
# Get all users
users = User.query.all()

# Get user by username
user = User.query.filter_by(username='john').first()

# Get user with admin privileges
admins = User.query.filter_by(is_admin=True).all()
```

**Querying Quiz Attempts:**
```python
# Get all attempts for a user
attempts = QuizAttempt.query.filter_by(user_id=current_user.id).all()

# Get average score
avg_score = db.session.query(db.func.avg(QuizAttempt.percentage)).filter_by(user_id=current_user.id).scalar()
```

**Creating Records:**
```python
# Create new user
user = User(
    username='john',
    email='john@example.com',
    password_hash=generate_password_hash('password123')
)
db.session.add(user)
db.session.commit()
```

---

## 3. Security Implementation

### 3.1 Password Hashing with Werkzeug

**Why Hash Passwords?**
- Never store plain text passwords
- Protect against database breaches
- Industry standard security practice

**Implementation:**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# During Registration (app.py - Line 828)
user = User(
    username=username,
    email=email,
    password_hash=generate_password_hash(password)  # Hash the password
)
db.session.add(user)
db.session.commit()

# During Login (app.py - Line 859)
user = User.query.filter_by(username=username).first()
if user and check_password_hash(user.password_hash, password):  # Verify hash
    login_user(user)
```

**How It Works:**
1. `generate_password_hash()`: Creates a secure hash using PBKDF2 algorithm
2. `check_password_hash()`: Verifies password against stored hash
3. Uses salt (random data) to prevent rainbow table attacks
4. Multiple iterations for security

**Security Features:**
- **PBKDF2 Algorithm**: Industry-standard key derivation function
- **Salt**: Random data added to prevent pre-computed attacks
- **Iterations**: Multiple hashing rounds (default: 260,000+)

### 3.2 Session Management with Flask-Login

**Flask-Login Setup:**
```python
from flask_login import LoginManager, login_user, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

**Key Features:**
- **Session-based authentication**: Secure session cookies
- **User loader**: Retrieves user from database
- **Login required decorator**: Protects routes
- **Current user**: Access logged-in user anywhere

**Protected Routes:**
```python
@app.route('/dashboard')
@login_required  # Requires authentication
def dashboard():
    # Only accessible to logged-in users
    return render_template('dashboard.html')
```

### 3.3 Role-Based Access Control (Admin vs User)

**User Model:**
```python
class User(UserMixin, db.Model):
    is_admin = db.Column(db.Boolean, default=False)  # Admin flag
```

**Admin Protection:**
```python
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:  # Check admin status
        flash('Access denied')
        return redirect(url_for('dashboard'))
    # Admin-only content
    return render_template('admin_dashboard.html')
```

**Admin Decorator (Alternative Approach):**
```python
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/manage/questions')
@admin_required
def manage_questions():
    # Admin-only route
    pass
```

**Access Control Examples:**
- **Public Routes**: `/`, `/register`, `/login`, `/quiz/public`, `/learn/public`
- **User Routes**: `/dashboard`, `/quiz`, `/learn`, `/profile`
- **Admin Routes**: `/admin`, `/admin/manage/questions`, `/admin/manage/resources`, `/visualizations`

### 3.4 CSRF Protection

**Flask-WTF CSRF (Implicit):**
- Flask forms can use CSRF tokens
- Session-based protection
- Prevents cross-site request forgery

**Best Practices Implemented:**
- Secret key for session signing
- HTTPS in production (recommended)
- Secure cookie flags
- Input validation

### 3.5 Input Validation & Sanitization

**Form Validation:**
```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check for existing user
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
```

**SQL Injection Prevention:**
- SQLAlchemy ORM automatically escapes queries
- Parameterized queries prevent injection
- No raw SQL strings with user input

**XSS Prevention:**
- Jinja2 templates auto-escape HTML
- User input sanitized before display
- JSON encoding for data storage

### 3.6 Security Configuration

```python
# app.py - Security Settings
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'  # Change in production!
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only (production)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
```

---

## 4. Key Files & Responsibilities

### 4.1 `app.py` - Main Application File

**Purpose:** Core Flask application with all routes, models, and business logic

**Key Sections:**
1. **Imports & Configuration** (Lines 1-34)
   - Flask, SQLAlchemy, Flask-Login imports
   - App configuration
   - Database URI setup

2. **Database Models** (Lines 271-343)
   - User, QuizQuestion, QuizAttempt, etc.
   - Relationships and constraints

3. **Database Initialization** (Lines 349-800)
   - Table creation
   - Default data seeding
   - Migration handling

4. **Routes** (Lines 802-1834)
   - Public routes (index, register, login)
   - User routes (dashboard, quiz, learn)
   - Admin routes (admin dashboard, management)
   - API endpoints

5. **Helper Functions** (Lines 89-269)
   - Data loading
   - ML model integration
   - Analytics building

**File Statistics:**
- **Total Lines**: ~1,837
- **Routes**: 30+ endpoints
- **Models**: 6 database models
- **Functions**: 15+ helper functions

### 4.2 `instance/digital_awareness.db` - Database File

**Structure:**
- SQLite database file
- Created automatically
- Contains all application data

**Tables:**
1. `user` - User accounts
2. `quiz_question` - Quiz questions
3. `quiz_attempt` - Quiz attempts
4. `user_activity` - Activity logs
5. `learning_resource` - Learning resources
6. `quiz_type` - Quiz categories

**Database Operations:**
- Read: Query user data, quiz attempts
- Write: Create users, save quiz results
- Update: Modify user profiles, update resources
- Delete: Remove questions, resources (admin)

### 4.3 `requirements.txt` - Dependencies

**Core Dependencies:**

```
Flask>=3.0.0                    # Web framework
Flask-SQLAlchemy>=3.1.1         # ORM for database
Flask-Login>=0.6.3              # User session management
Werkzeug>=3.0.1                 # Security utilities (password hashing)
```

**Data & ML Dependencies:**
```
pandas>=2.2.0                   # Data manipulation
numpy>=2.0.0                    # Numerical computing
scikit-learn>=1.5.0              # Machine learning
```

**Additional Dependencies:**
```
gspread>=5.12.0                 # Google Sheets integration
google-auth>=2.23.4             # Google API authentication
pytz>=2024.1                    # Timezone handling
openpyxl>=3.1.2                 # Excel file support
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 5. Technical Highlights & Best Practices

### 5.1 Code Organization

**Separation of Concerns:**
- Models in database classes
- Views in templates
- Controllers in route handlers
- Business logic in helper functions

**Modularity:**
- ML model in separate file (`ml_model.py`)
- Static files organized (`static/css/`, `static/js/`)
- Templates organized (`templates/`)

### 5.2 Error Handling

```python
try:
    # Database operations
    db.session.commit()
except Exception as e:
    db.session.rollback()
    flash('An error occurred')
    return redirect(url_for('home'))
```

### 5.3 Database Migrations

**Automatic Schema Updates:**
```python
# Check and add missing columns (app.py - Lines 352-393)
inspector = inspect(db.engine)
if 'quiz_type' not in quiz_question_columns:
    db.session.execute(text('ALTER TABLE quiz_question ADD COLUMN quiz_type VARCHAR(100)'))
    db.session.commit()
```

### 5.4 Activity Logging

**User Activity Tracking:**
```python
activity = UserActivity(
    user_id=current_user.id,
    activity_type='quiz_completed',
    description=f'Completed {quiz_type} quiz with {score}/{total}'
)
db.session.add(activity)
db.session.commit()
```

**Activity Types:**
- `login`, `logout`, `registration`
- `quiz_completed`, `resource_viewed`
- Admin actions

### 5.5 Timezone Handling

```python
# Timezone conversion (app.py - Lines 49-82)
DEFAULT_TIMEZONE = 'Asia/Kolkata'

def utc_to_local(utc_dt):
    local_tz = get_local_timezone()
    return utc_dt.astimezone(local_tz)

@app.template_filter('localtime')
def localtime_filter(dt):
    return utc_to_local(dt).strftime('%Y-%m-%d %H:%M')
```

---

## 6. Presentation Talking Points

### Opening Statement
"As the System Architect, I'm responsible for building the robust backend infrastructure that powers our Digital Responsibility Index platform. I've implemented a secure, scalable architecture using Flask's MVC pattern, SQLAlchemy ORM, and industry-standard security practices."

### Architecture Discussion
1. **MVC Pattern**: "We use Flask's MVC architecture to separate concerns - Models handle data, Views render templates, and Controllers process requests."
2. **Flask Framework**: "Flask provides a lightweight, flexible framework perfect for our educational platform."
3. **Modular Design**: "Our code is organized into logical modules for maintainability."

### Database Discussion
1. **SQLite Choice**: "We chose SQLite for its simplicity and zero-configuration setup."
2. **SQLAlchemy ORM**: "SQLAlchemy allows us to work with Python objects instead of raw SQL, making our code more maintainable."
3. **Schema Design**: "Our database has 6 main tables with proper relationships and foreign keys."
4. **Data Integrity**: "We use constraints like unique usernames and foreign keys to maintain data integrity."

### Security Discussion
1. **Password Security**: "We use Werkzeug's PBKDF2 hashing with salt - passwords are never stored in plain text."
2. **Session Management**: "Flask-Login handles secure session management with encrypted cookies."
3. **Role-Based Access**: "Admin and user roles are enforced at the route level."
4. **Input Validation**: "All user input is validated and sanitized to prevent SQL injection and XSS attacks."

### Technical Achievements
1. **Scalable Architecture**: "The MVC pattern allows easy addition of new features."
2. **Security First**: "Security is built into every layer - authentication, authorization, and data protection."
3. **Database Efficiency**: "ORM relationships enable efficient queries without manual joins."
4. **Activity Tracking**: "Comprehensive logging for analytics and security auditing."

---

## 7. Demo Points

### Show Database Structure
```python
# In Python shell or during presentation
from app import app, db, User, QuizAttempt
with app.app_context():
    users = User.query.all()
    print(f"Total users: {len(users)}")
    attempts = QuizAttempt.query.count()
    print(f"Total quiz attempts: {attempts}")
```

### Show Security Implementation
```python
# Demonstrate password hashing
from werkzeug.security import generate_password_hash, check_password_hash

password = "mypassword123"
hash = generate_password_hash(password)
print(f"Hash: {hash}")
print(f"Verification: {check_password_hash(hash, password)}")  # True
print(f"Wrong password: {check_password_hash(hash, 'wrong')}")  # False
```

### Show Database Queries
```python
# Show ORM queries
user = User.query.filter_by(username='admin').first()
attempts = QuizAttempt.query.filter_by(user_id=user.id).all()
avg_score = sum(a.percentage for a in attempts) / len(attempts) if attempts else 0
```

---

## 8. Questions & Answers Preparation

**Q: Why did you choose SQLite over PostgreSQL or MySQL?**
A: "SQLite is perfect for our use case - it's file-based, requires no server setup, and handles our expected user load efficiently. We can easily migrate to PostgreSQL if needed since we use SQLAlchemy ORM."

**Q: How do you handle database migrations?**
A: "We use automatic schema detection and ALTER TABLE statements for simple migrations. For production, we'd use Flask-Migrate for version-controlled migrations."

**Q: What security measures are in place?**
A: "We implement multiple layers: password hashing with PBKDF2, session management with Flask-Login, role-based access control, input validation, and SQL injection prevention through ORM."

**Q: How scalable is this architecture?**
A: "The MVC pattern and ORM make it easy to scale. We can add caching, move to PostgreSQL, implement load balancing, and add microservices as needed."

**Q: How do you ensure data integrity?**
A: "We use database constraints (unique, foreign keys, not null), ORM validations, and transaction management with rollback on errors."

---

## 9. Summary

### Key Responsibilities
✅ **Architecture**: MVC pattern implementation with Flask  
✅ **Database**: SQLite schema design with SQLAlchemy ORM  
✅ **Security**: Password hashing, session management, role-based access  
✅ **Code Quality**: Modular, maintainable, well-documented code  

### Technical Stack
- **Backend**: Flask 3.0+
- **Database**: SQLite with SQLAlchemy ORM
- **Security**: Werkzeug, Flask-Login
- **Architecture**: MVC Pattern

### Files Owned
- `app.py` - Main application (1,837 lines)
- `instance/digital_awareness.db` - Database file
- `requirements.txt` - Dependencies

---

**End of Presentation Guide**

