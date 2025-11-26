# Database Connection Status

## ✅ Database is Connected!

Your application uses **SQLite** database located at:
- **File**: `digital_awareness.db`
- **Connection**: `sqlite:///digital_awareness.db`

## 📊 Current Database Contents

### Users & Admins
- **Total Users**: Stored in `user` table
- **Admin Users**: Users with `is_admin=True`
- **Default Admin**: 
  - Username: `admin`
  - Password: `admin123`

### Quiz System
- **Quiz Types**: 5 types configured
  - Privacy Basics
  - Data Security
  - AI Ethics
  - Social Media Privacy
  - Quick Challenge

- **Quiz Questions**: Questions distributed across quiz types
- **Quiz Attempts**: Stored when users complete quizzes

### Learning Resources
- **Resources**: Educational content for users
- **Categories**: Privacy, AI Ethics, Data Security

### Activity Tracking
- **User Activities**: Login, logout, quiz completion, etc.
- **Timestamps**: All activities logged with UTC timestamps

## 🔧 How Database Works

1. **Automatic Creation**: Database is created automatically when you first run `app.py`
2. **Tables Created**: All tables are created via `db.create_all()`
3. **Data Persistence**: All data is saved to `digital_awareness.db` file
4. **Migrations**: New columns are added automatically when needed

## ✅ Verification

To verify database connection, run:
```python
python -c "from app import app, db; app.app_context().push(); print('Database connected:', db.engine.url)"
```

## 🔍 Database Location

The database file is in your project root directory:
```
C:\Users\APS IT SOLUTION\Documents\Final Year project\digital_awareness.db
```

## 📝 Admin & User Data

### Admin Data
- Stored in `user` table with `is_admin=True`
- Can access `/admin` dashboard
- Can view all user analytics
- Can retrain ML model

### User Data
- Stored in `user` table with `is_admin=False`
- Profile information (age, gender, academic stream, year)
- Quiz attempts and scores
- Activity history
- Personalized recommendations

## 🚀 All Data is Connected!

- ✅ User registration → Saved to database
- ✅ User login → Activity logged
- ✅ Quiz attempts → Scores saved
- ✅ Admin dashboard → Reads from database
- ✅ User dashboard → Shows user's data
- ✅ Learning resources → Stored in database
- ✅ ML recommendations → Based on user data

Everything is working and connected! 🎉


