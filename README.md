# Digital Awareness Platform

A comprehensive web application for digital privacy awareness, data security education, and AI ethics assessment. This platform allows users to learn about digital data usage, take quizzes to test their knowledge, and track their performance over time.

## Features

### User Features
- **User Registration & Login**: Secure authentication system
- **Dashboard**: Overview of quiz attempts, scores, and recent activities
- **Interactive Quiz System**: Test knowledge on digital privacy, data security, and AI ethics
- **Learning Resources**: Access to educational content and recommendations
- **Profile Management**: View performance history and personal statistics
- **Personalized Suggestions**: ML-based recommendations based on quiz performance

### Admin Features
- **Admin Dashboard**: Comprehensive analytics and user activity monitoring
- **User Statistics**: View all users' quiz performance and activity
- **Analytics**: Visual charts and graphs for platform usage
- **Activity Tracking**: Monitor all user activities in real-time

## Installation

1. **Clone or download the project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Initialize the database**:
The database will be automatically created when you run the application for the first time.

4. **Run the application**:
```bash
python app.py
```

5. **Access the application**:
- Open your browser and go to `http://localhost:5000`
- Default admin credentials:
  - Username: `admin`
  - Password: `admin123`

## Project Structure

```
.
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── quiz.html
│   ├── profile.html
│   ├── learn.html
│   └── admin_dashboard.html
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── Analysis.ipynb        # Survey data analysis notebook
└── README.md
```

## Database Models

- **User**: User accounts with profile information
- **QuizQuestion**: Quiz questions with multiple choice options
- **QuizAttempt**: Records of user quiz attempts and scores
- **UserActivity**: Logs of user activities
- **LearningResource**: Educational resources and links

## Google Sheets Integration

The application is designed to integrate with Google Sheets for survey data analysis. To set up:

1. Create a Google Cloud project and enable Google Sheets API
2. Create service account credentials
3. Share your Google Sheet with the service account email
4. Update the `SHEET_URL` in `app.py` with your sheet URL

## ML Model Integration

The platform is designed to support ML models for:
- Predicting user knowledge levels
- Personalized learning recommendations
- Performance analytics

## Usage

1. **Register a new account** or login with existing credentials
2. **Complete your profile** with demographic information
3. **Take quizzes** to test your knowledge
4. **View learning resources** to improve your understanding
5. **Track your progress** on the dashboard and profile pages

## Admin Access

Admins can:
- View all user statistics
- Monitor platform activity
- Access analytics and reports
- Manage learning resources

## Future Enhancements

- ML model for personalized recommendations
- Google Sheets API integration for survey data
- Advanced analytics and reporting
- Email notifications
- Social features and leaderboards

## License

This project is part of a Final Year Project for educational purposes.

## Contact

For questions or support, please contact the project team.

