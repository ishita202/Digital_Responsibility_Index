# Member 2: System Architect - Quick Reference

## 🎯 Role Overview
**Responsibility**: Server, Database, and Security  
**Focus**: The "How" and the "Backbone" (Flask + Database)

---

## 📐 1. Architecture: MVC Pattern

### MVC Components

| Component | Location | Responsibility |
|-----------|----------|---------------|
| **Model** | `app.py` (Lines 271-343) | Database models (User, QuizAttempt, etc.) |
| **View** | `templates/` | HTML templates (dashboard.html, quiz.html) |
| **Controller** | `app.py` (Routes) | Route handlers process requests |

### Flask App Structure
```python
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digital_awareness.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
```

---

## 🗄️ 2. Database: SQLite + SQLAlchemy ORM

### Database File
- **Location**: `instance/digital_awareness.db`
- **Type**: SQLite (file-based, zero-config)

### Key Tables

#### User Table
```python
class User(db.Model):
    id, username, email, password_hash
    is_admin, created_at
    age_range, gender, academic_stream, year_of_study
    # Relationships
    quiz_attempts → QuizAttempt
    activities → UserActivity
```

#### QuizAttempt Table
```python
class QuizAttempt(db.Model):
    id, user_id (FK), quiz_type
    score, total_questions, percentage
    time_taken, time_limit
    answers (JSON), completed_at
```

#### LearningResource Table
```python
class LearningResource(db.Model):
    id, title, description, url
    category, resource_type, created_at
```

### Relationships
```
User (1) ──────< (Many) QuizAttempt
User (1) ──────< (Many) UserActivity
```

### SQLAlchemy Benefits
- ✅ Python objects instead of SQL
- ✅ Type safety
- ✅ Database-agnostic
- ✅ Automatic relationships

---

## 🔒 3. Security Implementation

### 3.1 Password Hashing (Werkzeug)

**Registration:**
```python
password_hash=generate_password_hash(password)
```

**Login:**
```python
check_password_hash(user.password_hash, password)
```

**Algorithm**: PBKDF2 with salt  
**Security**: Industry-standard, prevents rainbow table attacks

### 3.2 Session Management (Flask-Login)

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/dashboard')
@login_required  # Protects route
def dashboard():
    return render_template('dashboard.html')
```

### 3.3 Role-Based Access Control

**Admin Check:**
```python
if not current_user.is_admin:
    flash('Access denied')
    return redirect(url_for('dashboard'))
```

**Access Levels:**
- **Public**: `/`, `/register`, `/login`
- **User**: `/dashboard`, `/quiz`, `/learn`
- **Admin**: `/admin`, `/admin/manage/*`, `/visualizations`

### 3.4 Security Features
- ✅ Password hashing (PBKDF2)
- ✅ Session management (Flask-Login)
- ✅ Role-based access (Admin/User)
- ✅ Input validation
- ✅ SQL injection prevention (ORM)
- ✅ XSS prevention (Jinja2 auto-escape)

---

## 📁 4. Key Files

### `app.py` (1,837 lines)
**Sections:**
1. Imports & Configuration (Lines 1-34)
2. Helper Functions (Lines 89-269)
3. Database Models (Lines 271-343)
4. Database Initialization (Lines 349-800)
5. Routes (Lines 802-1834)

**Key Features:**
- 30+ routes
- 6 database models
- 15+ helper functions
- ML integration
- Analytics engine

### `instance/digital_awareness.db`
- SQLite database file
- 6 tables: user, quiz_question, quiz_attempt, user_activity, learning_resource, quiz_type
- Auto-created on first run

### `requirements.txt`
**Core:**
- Flask>=3.0.0
- Flask-SQLAlchemy>=3.1.1
- Flask-Login>=0.6.3
- Werkzeug>=3.0.1

**Data & ML:**
- pandas>=2.2.0
- numpy>=2.0.0
- scikit-learn>=1.5.0

---

## 💡 Key Talking Points

### Architecture
- "We use Flask's MVC pattern to separate concerns"
- "Models handle data, Views render UI, Controllers process requests"
- "Modular design for maintainability"

### Database
- "SQLite for simplicity and zero-configuration"
- "SQLAlchemy ORM for Python-based database operations"
- "6 tables with proper relationships and foreign keys"

### Security
- "Werkzeug PBKDF2 hashing - passwords never stored in plain text"
- "Flask-Login for secure session management"
- "Role-based access control for admin and user separation"
- "Input validation prevents SQL injection and XSS"

---

## 🎤 Presentation Flow

1. **Introduction** (30 sec)
   - "I'm the System Architect, responsible for backend and security"

2. **Architecture** (2 min)
   - Explain MVC pattern
   - Show Flask app structure
   - Demonstrate route handling

3. **Database** (2 min)
   - SQLite choice rationale
   - Show database models
   - Explain relationships
   - SQLAlchemy ORM benefits

4. **Security** (2 min)
   - Password hashing demonstration
   - Session management
   - Role-based access
   - Security best practices

5. **Code Walkthrough** (1 min)
   - Show key files
   - Highlight important sections
   - Explain file structure

6. **Q&A Preparation** (1 min)
   - Common questions ready
   - Technical depth available

---

## 🔍 Code Examples for Demo

### Show Password Hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

hash = generate_password_hash("password123")
print(hash)  # Shows hashed password
check_password_hash(hash, "password123")  # True
```

### Show Database Query
```python
from app import app, db, User, QuizAttempt

with app.app_context():
    user = User.query.filter_by(username='admin').first()
    attempts = QuizAttempt.query.filter_by(user_id=user.id).all()
    print(f"User has {len(attempts)} quiz attempts")
```

### Show Protected Route
```python
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('dashboard'))
    return render_template('admin_dashboard.html')
```

---

## ✅ Checklist Before Presentation

- [ ] Review `app.py` structure
- [ ] Understand database schema
- [ ] Know security implementations
- [ ] Prepare code examples
- [ ] Review MVC pattern explanation
- [ ] Practice database query demos
- [ ] Prepare answers for common questions

---

## 📊 Statistics to Mention

- **Total Routes**: 30+
- **Database Models**: 6
- **Lines of Code**: ~1,837 in app.py
- **Security Layers**: 4+ (hashing, sessions, roles, validation)
- **Database Tables**: 6
- **Dependencies**: 15+ packages

---

**Quick Reference End**

