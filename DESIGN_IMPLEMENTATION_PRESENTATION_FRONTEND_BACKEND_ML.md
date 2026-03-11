## Design & Implementation – Presentation (Frontend / Backend / ML Split)

This file is structured as **PowerPoint slides**.  
Each slide has:
- **Slide Title**
- **Bullet points** (for the slide)
- **Speaker Notes** (what the presenter can say)

You can copy each slide section into PowerPoint as one slide.

---

## Person 1 – Frontend & UI (Presentation Layer)

### Slide 1 – Frontend Role & Overview

- **Title:** Frontend Design & User Experience
- **Content (bullets):**
  - Responsible for **all user-facing pages** and overall user experience of the Digital Awareness Platform.
  - Built using **HTML5, CSS3, JavaScript, Jinja2 templates, and Bootstrap 5** for responsive design.
  - Focus on making complex topics like **digital privacy, data security, and AI ethics** easy to understand.
  - Ensures that the visual design matches the educational goals of the platform.

**Speaker Notes:**  
“This section explains how the **frontend** of the Digital Awareness Platform is designed and implemented. The frontend team is responsible for the entire **user-facing layer** – all the pages that students, professionals, and administrators interact with. Standard web technologies such as HTML, CSS, JavaScript, and Bootstrap 5 are combined with Flask’s Jinja2 templates to create a modern, responsive interface. The main objective is not only to make the website visually appealing, but also to present topics such as digital privacy, security, and AI ethics in a way that is **clear, engaging, and easy to navigate** for all users.”

---

### Slide 2 – Frontend Architecture & Template Structure

- **Title:** Templates and Layout Structure
- **Content (bullets):**
  - The frontend follows a **template inheritance** pattern using `base.html` as the main layout.
  - **`base.html`** defines the common structure: navigation bar, header, footer, and message area.
  - Public-facing pages:
    - `index.html` – landing page with project overview and call-to-action.
    - `learn_public.html` and `quiz_public.html` – preview of resources and quizzes without login.
  - Authenticated user pages:
    - `dashboard.html`, `quiz.html`, `quiz_select.html`, `learn.html`, `profile.html`, `visualizations.html`.
  - Admin pages:
    - `admin_dashboard.html`, `admin_manage_questions.html`, `admin_manage_resources.html`, `admin_home.html`, `admin_settings.html`.
  - All pages **extend** `base.html`, which guarantees a **consistent header, footer, and styling**.

**Speaker Notes:**  
“On the frontend, a clean template structure is used to keep the code organized. The core idea is a single **base template** called `base.html`. This file defines the common components such as the navigation bar, footer, and the general page layout. All other pages, such as `index.html`, `dashboard.html`, `quiz.html`, and the admin pages, simply **extend** this base template. Any change to navigation or branding in the base template is automatically reflected across the platform. Pages for public users, authenticated users, and administrators are logically separated, but visually they appear as parts of one consistent system.”

---

### Slide 3 – Key User Flows from the Frontend Perspective

- **Title:** User Flows and Navigation Design
- **Content (bullets):**
  - **Public user flow:**
    - Visits landing page → explores **public learn** and **public quiz** previews → registers or logs in.
  - **Authenticated user flow:**
    - Logs in → lands on **dashboard** with statistics and shortcuts → **takes quizzes**, views **detailed results** and **explanations** → receives **ML-based recommendations** → explores **learning resources** → monitors progress via **charts and activity history**.
  - **Admin flow:**
    - Logs in as admin → accesses **admin dashboard** → manages **quiz questions** and **learning resources** → views **platform-wide analytics and visualizations**.
  - Navigation is designed to be **intuitive**, with clear call-to-action buttons and a consistent menu.

**Speaker Notes:**  
“From the frontend perspective, the **user journeys** are carefully designed. A new visitor first lands on the home page and can see public previews of quizzes and learning resources, which helps build interest and encourages registration. After logging in, a user is presented with a personalized **dashboard** displaying attempts, scores, and quick links to quizzes and resources. Following each quiz, the interface shows detailed explanations and personalized recommendations. For administrators, a dedicated set of pages provides tools to manage questions, resources, and view overall statistics. All of these elements are connected through a clear navigation bar and prominent call-to-action buttons so that users can move through the platform without confusion.”

---

### Slide 4 – Visual Design, Styling, and Interactivity

- **Title:** UI Components & Visual Experience
- **Content (bullets):**
  - Styling is handled by **Bootstrap 5** plus a custom stylesheet `static/css/style.css`.
  - Uses a **modern, warm color palette** (e.g., blue and green tones) to create a professional yet friendly look.
  - Core UI components:
    - **Cards** for quizzes and resources.
    - **Alerts** and badges for feedback and status messages.
    - **Responsive grid layouts** for desktop, tablet, and mobile screens.
  - Interactivity via `static/js/main.js` and inline scripts:
    - Quiz **countdown timer** and time limit handling.
    - Basic client-side validation and dynamic content updates.
    - Preparation of data for **charts and visualizations**.
  - Emphasis on **readability**, **spacing**, and **accessibility-friendly layouts**.

**Speaker Notes:**  
“For the visual design, **Bootstrap 5** is combined with custom CSS in `style.css` to achieve a clean and modern interface while still supporting project-specific branding. Card components are used to present quizzes and resources in a structured way, and alert components display success and error messages. Because the platform may be used on phones, tablets, and laptops, a **mobile-first, responsive design** approach is adopted. Interactivity is handled through JavaScript in `main.js`, for example, for the quiz timer and dynamic updates on the quiz page. Overall, the interface is intended to remain visually appealing while staying **simple, readable, and accessible**.”

---

### Slide 5 – Frontend Challenges and Future Enhancements

- **Title:** Frontend Challenges & Improvements
- **Content (bullets):**
  - **Challenge 1:** Presenting **46+ quiz questions** and **49+ learning resources** without overwhelming users.
    - Solution: use categorized views, concise cards, and pagination/sections.
  - **Challenge 2:** Displaying **ML-based recommendations** in a way that is easy to understand.
    - Solution: show the knowledge level (Low/Medium/High) with short, actionable tips and direct links to resources.
  - **Challenge 3:** Maintaining **consistency** across public, user, and admin interfaces.
    - Solution: enforce a shared layout via `base.html` and shared CSS components.
  - **Planned future improvements:**
    - Dark mode and improved accessibility (e.g., ARIA attributes, keyboard navigation).
    - More advanced chart visualizations and interactive dashboards.
    - Progressive Web App features for better mobile experience.

**Speaker Notes:**  
“On the frontend side, several challenges were encountered. The first challenge was the amount of content: more than 46 questions and 49 resources. To avoid overwhelming users, content is organized by categories and presented using clean card layouts instead of large blocks of text. A second challenge was explaining the **ML recommendations** clearly; this is addressed by presenting a simple knowledge level label and pairing it with direct suggestions and links. Another challenge was ensuring that the admin, user, and public interfaces remain consistent, which is achieved through the shared layout and CSS. Planned improvements include dark mode, stronger accessibility support, and more interactive charts to enhance the user experience.”

---

## Person 2 – Backend & Database (Flask + SQLite)

### Slide 6 – Backend Role & Overview

- **Title:** Backend Architecture & Responsibilities
- **Content (bullets):**
  - Backend implemented using **Flask** as the web framework.
  - Follows an **MVC-style structure**: models, views (templates), controllers (routes).
  - Responsible for **business logic**, **security**, and **data management**.
  - Key files:
    - `app.py` – main application file (~1,800+ lines of code).
    - `setup.py` – database initialization and setup.
    - `instance/digital_awareness.db` – SQLite database.
  - Integrates with the **ML model** and exposes APIs for analytics and recommendations.

**Speaker Notes:**  
“The **backend** of the Digital Awareness Platform is implemented using Flask to handle all server-side logic. Although Flask is a lightweight framework, an **MVC-style approach** is followed, where models are represented by database classes, views are the templates, and controllers are the route functions in `app.py`. The backend is responsible for handling authentication, quiz logic, analytics, administrative functions, and communication with both the database and the machine learning model. The core of the backend resides in `app.py`, which contains the models, helper functions, and more than thirty different routes.”

---

### Slide 7 – Project Structure and Core Modules

- **Title:** Backend Project Structure
- **Content (bullets):**
  - Overall project layout (from the report):
    - `app.py` – main Flask app (routes, models, helpers, ML integration).
    - `ml_model.py` – training and prediction functions for Random Forest.
    - `google_sheets_integration.py` – imports survey data from Google Sheets.
    - `requirements.txt` – Python dependencies.
    - `templates/` – 17+ HTML templates.
    - `static/` – CSS and JavaScript assets.
    - `instance/digital_awareness.db` – SQLite database file.
  - **Core backend responsibilities:**
    - User authentication and authorization.
    - Quiz management and scoring.
    - Admin panel operations.
    - Analytics and API endpoints.

**Speaker Notes:**  
“The backend is organized around `app.py`, which serves as the main entry point. It defines the Flask application, configures the database, and registers all route handlers. The `ml_model.py` file focuses on machine learning logic, while `google_sheets_integration.py` is used to pull survey data from Google Sheets for training. There are also dedicated directories for templates and static assets. Within the backend, the main responsibilities include handling user logins and logouts, managing quizzes, providing dashboards and analytics, and offering tools for administrators to manage questions and resources. All of these components work together to support the educational goals of the platform.”

---

### Slide 8 – Database Design and SQLAlchemy Models

- **Title:** Database Schema & ORM Design
- **Content (bullets):**
  - Database used: **SQLite** file `digital_awareness.db` located in `instance/`.
  - ORM: **SQLAlchemy** for defining models and performing queries.
  - Main models (tables):
    - `User` – stores user accounts, profile, and admin flag.
    - `QuizQuestion` – stores quiz questions, options, correct answers, category, and quiz type.
    - `QuizType` – defines quiz configurations (name, description, time limit, question count, difficulty).
    - `QuizAttempt` – stores results of each quiz attempt (score, percentage, time, answers JSON).
    - `UserActivity` – logs activities such as login, logout, quiz_completed, resource_viewed.
    - `LearningResource` – stores title, URL, category, and type of each resource.
  - Relationships:
    - One `User` → many `QuizAttempt` and `UserActivity` records.
    - One `QuizType` → many related questions and attempts.
  - Benefits of ORM:
    - No raw SQL needed, easier migrations, and safer queries.

**Speaker Notes:**  
“For data storage, **SQLite** is used as a lightweight, file-based database. Interaction with the database is handled through **SQLAlchemy**, which allows tables to be defined as Python classes. The key models are `User`, `QuizQuestion`, `QuizType`, `QuizAttempt`, `UserActivity`, and `LearningResource`, each corresponding to a table in the `digital_awareness.db` file. For example, the `User` model holds login credentials and profile information, while `QuizAttempt` records each quiz taken by a user. There are clear relationships, such as one user having many attempts and activities. Using an ORM provides several advantages: manual SQL is avoided, errors are reduced, and the schema can be modified more easily when new features are added.”

---

### Slide 9 – Security, Sessions, and Access Control

- **Title:** Security & Session Management
- **Content (bullets):**
  - **Authentication:** implemented using **Flask-Login**.
    - `login_user()`, `logout_user()`, `current_user`, and `@login_required` decorator.
  - **Password security:** handled by **Werkzeug**.
    - `generate_password_hash()` for hashing.
    - `check_password_hash()` for verification.
    - Uses **PBKDF2** with salt and multiple iterations.
  - **Role-based access:**
    - `is_admin` boolean field in `User` model.
    - Admin-only routes such as `/admin`, `/admin/manage/questions`, `/admin/manage/resources` are protected with checks.
  - Additional security practices:
    - Secret key for signing sessions.
    - HTTPOnly and SameSite cookie settings (especially in production).
    - Validation of user input and use of SQLAlchemy ORM to prevent injection.
    - Jinja2 auto-escaping to reduce XSS risks.

**Speaker Notes:**  
“Security is a core part of the backend. For authentication and sessions, **Flask-Login** is used to simplify login handling and session management. Passwords are never stored in plain text; instead, Werkzeug’s `generate_password_hash` is used during registration and `check_password_hash` during login. This approach relies on PBKDF2 with a salt and many iterations, which is a widely accepted standard. **Role-based access control** is implemented through the `is_admin` flag in the `User` table, restricting certain routes, such as the admin dashboard, to administrative users only. In addition, secure session cookies are configured, and ORM features together with template auto-escaping help protect against SQL injection and cross-site scripting.”

---

### Slide 10 – Backend Logic Flows and Challenges

- **Title:** Backend Workflows & Limitations
- **Content (bullets):**
  - Example **quiz workflow**:
    - User selects quiz type → route loads configuration from `QuizType`.
    - Fetch questions from `QuizQuestion` → randomize order.
    - Render `quiz.html` with timer and questions.
    - On submit: backend loads correct answers, computes score and percentage.
    - Saves `QuizAttempt` and logs `UserActivity`.
    - Triggers ML module for knowledge level prediction and recommendations.
  - **Challenges:**
    - Managing a large single-file application (`app.py`) while keeping routes and logic readable.
    - Handling database schema changes safely (ALTER TABLE logic for new columns).
  - **Planned backend improvements:**
    - Split `app.py` into multiple **blueprints/modules**.
    - Migrate from SQLite to **PostgreSQL/MySQL** for higher scalability.
    - Introduce caching and background jobs for heavy analytics or ML tasks.

**Speaker Notes:**  
“To illustrate how the backend operates, consider the quiz workflow. When a user chooses a quiz type, the backend loads the configuration from the `QuizType` table and fetches appropriate questions from `QuizQuestion`, then renders the quiz page. After submission, the backend compares answers, calculates the score, saves a new `QuizAttempt` record, and logs the action in `UserActivity`. Finally, the machine learning module is called to generate personalized recommendations. One major challenge is the size of `app.py`, which contains many routes and functions; future work involves splitting it into smaller modules using Flask blueprints and potentially upgrading from SQLite to a more scalable database as usage grows.”

---

## Person 3 – Machine Learning Specialist & Data Integration

### Slide 11 – ML Role & High-Level Overview

- **Title:** Machine Learning & Personalization Engine
- **Content (bullets):**
  - Implements the **Random Forest–based model** for predicting user knowledge level.
  - Integrates survey data and quiz performance into a unified **feature set**.
  - Generates **personalized learning recommendations** for each user.
  - Main files and tools:
    - `ml_model.py` – ML pipeline (training, evaluation, saving model).
    - `Analysis.ipynb` – exploratory data analysis and experiments.
    - `google_sheets_integration.py` – data import from Google Sheets.
    - `ml_model.pkl` – serialized trained Random Forest model.

**Speaker Notes:**  
“The machine learning specialist is responsible for building and integrating the **personalization engine** of the platform. A **Random Forest Classifier** is used to predict the user’s digital awareness level and then map that prediction to specific learning recommendations. Work is carried out mainly with Python data science libraries and files such as `ml_model.py` and `Analysis.ipynb`. The model is trained using real survey data imported from Google Sheets and is saved as `ml_model.pkl` so that the Flask application can load it quickly in production.”

---

### Slide 12 – Data Sources and Preprocessing

- **Title:** Data Collection & Preprocessing
- **Content (bullets):**
  - Primary data source: **survey responses** collected via Google Forms/Sheets.
    - Stored temporarily in Excel (`Project Survey (Responses).xlsx`) or CSV (`survey_data_backup.csv`).
    - Imported using `google_sheets_integration.py` and processed with **pandas**.
  - Additional data: platform-generated data (user demographics, quiz attempts) from `digital_awareness.db`.
  - Preprocessing pipeline:
    - Load raw data into pandas DataFrames.
    - Handle missing values and inconsistent entries.
    - Encode categorical variables (age range, gender, academic stream, year of study, behaviour questions).
    - Split into **train and test sets** (e.g., 80% training, 20% testing).
  - Ensures the model receives **clean, consistent, and meaningful features**.

**Speaker Notes:**  
“The primary dataset originates from a survey conducted using Google Forms. The responses are stored in Google Sheets and also exported to Excel and CSV formats. The script `google_sheets_integration.py` together with libraries such as `pandas` is used to import and clean this data. Preprocessing is critical: missing values are handled, categories are unified, and text fields like age range or academic stream are encoded into numeric codes that the model can understand. A train–test split is then performed to evaluate performance reliably. In addition to survey data, the platform’s own database can later be used to enrich the feature set with real user behavior.”

---

### Slide 13 – Random Forest Model Design and Features

- **Title:** Model Architecture & Feature Engineering
- **Content (bullets):**
  - Algorithm chosen: **Random Forest Classifier** – robust and interpretable for classification tasks.
  - Target variable: **knowledge level** with categories like **Low**, **Medium**, and **High**.
  - Feature groups:
    - **Demographic features:**
      - Age range, gender, academic stream, year of study.
    - **Behavioural features:**
      - Frequency of reading privacy policies.
      - Checking app permissions.
      - Using different passwords for different accounts.
    - **Performance features (planned/extended):**
      - Average quiz score and history-based indicators.
  - Training parameters (from report):
    - Number of trees, maximum depth, and other hyperparameters chosen for balanced performance.
  - Model is trained, evaluated, and finally stored as `ml_model.pkl` for deployment.

**Speaker Notes:**  
“The **Random Forest Classifier** is selected as the main algorithm because it handles categorical data well and is robust for classification tasks. The objective is to classify users into knowledge levels: Low, Medium, or High awareness. To achieve this, features are engineered from three areas: demographics, digital behaviour, and quiz performance. Demographic features include age range and academic background, while behavioural features capture habits such as reading privacy policies or checking app permissions. In extended versions of the model, actual quiz scores are also considered. After tuning parameters like the number of trees and maximum depth, the model is trained and evaluated, and once the performance is satisfactory it is serialized as `ml_model.pkl` so the Flask application can load it without retraining each time.”

---

### Slide 14 – Integration with the Flask Application

- **Title:** ML Integration & Recommendation Flow
- **Content (bullets):**
  - The ML model is **loaded into memory** by the Flask app from `ml_model.pkl`.
  - Whenever a user completes a quiz:
    - Backend gathers user profile data and relevant quiz performance metrics.
    - Constructs a **feature vector** in the same format used during training.
    - Calls the Random Forest model to predict the knowledge level.
  - The predicted knowledge level is mapped to **human-readable recommendations**:
    - Low → focus on foundational topics and basic resources.
    - Medium → intermediate security practices and habit-building content.
    - High → advanced resources, research papers, and deeper AI ethics topics.
  - Recommendations are displayed on:
    - The **quiz result page** (immediately after a quiz).
    - The **dashboard/learning resources** section (ongoing guidance).

**Speaker Notes:**  
“A key aspect is how the machine learning model is integrated into the live system. The Flask application loads the trained model from `ml_model.pkl` at startup. After the user completes a quiz, the backend collects the necessary information about the user—such as demographic profile and quiz performance—and builds a feature vector that matches the one used during training. This vector is passed to the Random Forest model, which returns a predicted knowledge level. This label is then translated into concrete recommendations: for a low level, introductory materials are suggested; for medium, more practical security steps are recommended; and for high, advanced resources are provided. These recommendations are shown directly with the results and also influence what the user sees on the dashboard.”

---

### Slide 15 – ML Challenges, Evaluation, and Future Enhancements

- **Title:** ML Challenges, Results & Roadmap
- **Content (bullets):**
  - **Challenges faced:**
    - Cleaning and encoding real survey data with varied responses.
    - Avoiding overfitting while using a relatively small academic dataset.
    - Ensuring fast prediction so quiz submission is not delayed.
  - **Model evaluation:**
    - Used metrics like **accuracy, precision, and recall** (as discussed in analysis notebook).
    - Verified that predictions were **reasonable and consistent** across demographic groups.
  - **Planned improvements:**
    - Continuously **retrain the model** with new platform data (quiz attempts and activity logs).
    - Experiment with **other algorithms** or ensembles and compare performance.
    - Add **explainability tools** (e.g., feature importance) to help users understand why a recommendation was made.
    - Use more behavioural signals such as time spent on resources or repeated quiz attempts.

**Speaker Notes:**  
“Working with real survey data always introduces challenges. The responses must be carefully cleaned and converted into a format that machine learning models can understand. Because the dataset is from an academic context, attention must be paid to the risk of overfitting. The model is evaluated using metrics such as accuracy and precision, and predictions are checked to ensure that they make sense across different user groups. Looking ahead, the ML component of the platform has significant room for growth: the model can be retrained periodically on fresh platform data, newer algorithms can be explored, and explainability techniques can be integrated to show users which factors influence their predicted knowledge level. Additional behavioural data, such as how often users revisit resources or retake quizzes, can also be incorporated to make recommendations even more accurate.”

---

## End of Presentation File

This markdown file is designed to be **directly convertible into PowerPoint slides** by copying each “Slide” section into one PPT slide and using the **Speaker Notes** as presenter script.


