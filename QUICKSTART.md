# Quick Start Guide

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database and Train ML Model

```bash
python setup.py
```

This will:
- Create the database
- Create default admin user (username: `admin`, password: `admin123`)
- Train the ML model (if survey data is available)

### 3. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## First Time Setup

### Default Admin Account
- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change the admin password after first login!

### Creating Your First User Account

1. Go to the registration page
2. Fill in your details:
   - Username
   - Email
   - Password
   - Age Range
   - Gender
   - Academic Stream
   - Year of Study
3. Click Register
4. Login with your new account

## Using the Platform

### For Regular Users

1. **Dashboard**: View your quiz attempts, scores, and recent activities
2. **Learn**: Access learning resources and personalized recommendations
3. **Quiz**: Take quizzes to test your knowledge
4. **Profile**: View your performance history

### For Admins

1. **Admin Dashboard**: View all user statistics and platform analytics
2. **User Management**: Monitor user activities and performance
3. **Analytics**: View charts and graphs of platform usage

## Google Sheets Integration (Optional)

To connect to your Google Sheets survey data:

1. **Set up Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Sheets API and Google Drive API

2. **Create Service Account**:
   - Go to IAM & Admin > Service Accounts
   - Create a new service account
   - Download the credentials JSON file

3. **Share Your Sheet**:
   - Open your Google Sheet
   - Click Share
   - Add the service account email (from the JSON file)
   - Give it "Viewer" access

4. **Update Configuration**:
   - Place the credentials JSON file in the project root
   - Update `google_sheets_integration.py` with the file path
   - Update `SHEET_URL` in `app.py` with your sheet URL

5. **Refresh Data**:
   ```python
   from google_sheets_integration import GoogleSheetsIntegration
   gs = GoogleSheetsIntegration(credentials_path='credentials.json')
   gs.refresh_data()
   ```

## ML Model Training

The ML model is automatically trained when you run `setup.py`. If you want to retrain it:

```python
from ml_model import train_and_save_model
ml = train_and_save_model()
```

The model will:
- Load survey data from `survey_data_backup.csv` (if available)
- Preprocess the data
- Train a Random Forest classifier
- Save the model to `ml_model.pkl`

## Troubleshooting

### Database Issues
- Delete `digital_awareness.db` and run `setup.py` again
- Make sure you have write permissions in the project directory

### ML Model Issues
- If the model fails to load, it will train a new one automatically
- Check that `survey_data_backup.csv` exists if you want to use real data
- The model will work with sample data if survey data is not available

### Google Sheets Issues
- Make sure the service account email has access to the sheet
- Check that the credentials JSON file is valid
- Verify the sheet URL is correct

## Next Steps

1. **Customize Quiz Questions**: Add more questions in the database
2. **Add Learning Resources**: Add more resources through the admin panel
3. **Configure Analytics**: Customize the analytics dashboard
4. **Deploy**: Deploy to a production server (Heroku, AWS, etc.)

## Support

For issues or questions, check the main README.md file or contact the development team.

