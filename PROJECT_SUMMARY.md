# Digital Awareness Platform - Project Summary

## Overview

This is a comprehensive web application designed to educate users about digital privacy, data security, and AI ethics. The platform is built based on survey analysis from Google Sheets and includes ML-powered personalized recommendations.

## Key Features Implemented

### 1. User Management
- ✅ User registration with profile information (age, gender, academic stream, year of study)
- ✅ Secure login/logout functionality
- ✅ User profile management
- ✅ Admin user support

### 2. Quiz System
- ✅ Interactive quiz with multiple-choice questions
- ✅ Questions based on digital privacy, data security, and AI ethics topics
- ✅ Real-time scoring and feedback
- ✅ Explanation for each question after submission
- ✅ Performance tracking and history

### 3. Learning Resources
- ✅ Digital data usage information pages
- ✅ Educational content about privacy and security
- ✅ Learning resource library
- ✅ ML-powered personalized recommendations

### 4. Dashboard & Analytics
- ✅ User dashboard with statistics (total quizzes, average score)
- ✅ Recent quiz attempts display
- ✅ Activity log tracking
- ✅ Performance visualization

### 5. Admin Panel
- ✅ Admin dashboard with platform-wide statistics
- ✅ User activity monitoring
- ✅ Analytics and reporting
- ✅ User performance overview

### 6. ML Integration
- ✅ Machine learning model for knowledge level prediction
- ✅ Personalized recommendations based on user profile and performance
- ✅ Random Forest classifier for predictions
- ✅ Support for training on survey data

### 7. Google Sheets Integration
- ✅ Connection to Google Sheets for survey data
- ✅ Data refresh functionality
- ✅ Support for service account authentication

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **ML**: scikit-learn (Random Forest)
- **Data Analysis**: pandas, numpy
- **Authentication**: Flask-Login

## Project Structure

```
.
├── app.py                          # Main Flask application
├── ml_model.py                     # ML model implementation
├── google_sheets_integration.py    # Google Sheets API integration
├── setup.py                        # Database and model initialization
├── requirements.txt                # Python dependencies
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
├── PROJECT_SUMMARY.md              # This file
├── templates/                      # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── quiz.html
│   ├── profile.html
│   ├── learn.html
│   └── admin_dashboard.html
└── static/                         # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Database Schema

### User
- id, username, email, password_hash
- is_admin, created_at
- age_range, gender, academic_stream, year_of_study

### QuizQuestion
- id, question_text
- option_a, option_b, option_c, option_d
- correct_answer, category, explanation, difficulty

### QuizAttempt
- id, user_id, score, total_questions, percentage
- completed_at, answers (JSON)

### UserActivity
- id, user_id, activity_type, description, created_at

### LearningResource
- id, title, description, url, category, resource_type

## ML Model Details

- **Algorithm**: Random Forest Classifier
- **Purpose**: Predict user knowledge level (Low/Medium/High)
- **Features**: Age, Gender, Academic Stream, Year of Study, Privacy behaviors
- **Output**: Knowledge level prediction and personalized recommendations

## Survey Data Integration

The platform is designed to work with survey data from Google Sheets:
- Privacy policy reading habits
- App permission review frequency
- Password security practices
- AI trust levels
- Knowledge check questions

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run setup: `python setup.py`
3. Start application: `python app.py`
4. Access at: `http://localhost:5000`

Default admin: username `admin`, password `admin123`

## Future Enhancements

- [ ] Enhanced ML model with more features
- [ ] Real-time Google Sheets sync
- [ ] Email notifications
- [ ] Social features and leaderboards
- [ ] Mobile app version
- [ ] Advanced analytics dashboard
- [ ] Certificate generation for quiz completion
- [ ] Multi-language support

## Notes

- The ML model will automatically train on available survey data
- If survey data is not available, the model uses sample data
- Google Sheets integration requires service account setup
- All user data is stored locally in SQLite database
- Admin panel provides comprehensive analytics

## Contact

For questions or support regarding this project, please refer to the main README.md file.

