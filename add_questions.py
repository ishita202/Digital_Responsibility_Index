"""
Script to add more quiz questions to the database
Run this to populate all quiz types with questions
"""

from app import app, db, QuizQuestion, QuizType

def add_all_questions():
    """Add questions for all quiz types"""
    with app.app_context():
        # Get all quiz types
        quiz_types = QuizType.query.all()
        print(f"Found {len(quiz_types)} quiz types")
        
        # Questions to add
        all_questions = [
            # Privacy Basics - Additional questions
            QuizQuestion(
                question_text="What is a VPN and what does it do?",
                option_a="A virtual private network that encrypts your internet connection",
                option_b="A type of browser",
                option_c="A social media platform",
                option_d="An email service",
                correct_answer="A",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="VPN encrypts your connection and hides your IP address, providing privacy online.",
                difficulty="Medium",
                time_limit=50
            ),
            QuizQuestion(
                question_text="What information can websites track about you?",
                option_a="Only your name",
                option_b="IP address, browsing history, location, device info",
                option_c="Nothing",
                option_d="Only your email",
                correct_answer="B",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="Websites can track IP address, browsing patterns, location, device information, and more.",
                difficulty="Easy",
                time_limit=45
            ),
            QuizQuestion(
                question_text="What is browser fingerprinting?",
                option_a="A security feature",
                option_b="A way to identify users based on browser characteristics",
                option_c="A type of cookie",
                option_d="A password manager",
                correct_answer="B",
                category="Privacy",
                quiz_type="Privacy Basics",
                explanation="Browser fingerprinting identifies users by unique browser and device characteristics.",
                difficulty="Hard",
                time_limit=55
            ),
            
            # Data Security - Additional questions
            QuizQuestion(
                question_text="What is a password manager?",
                option_a="A tool to store and manage passwords securely",
                option_b="A type of antivirus",
                option_c="A browser extension",
                option_d="A social media app",
                correct_answer="A",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Password managers securely store and generate strong passwords for your accounts.",
                difficulty="Easy",
                time_limit=35
            ),
            QuizQuestion(
                question_text="What is phishing?",
                option_a="A type of fishing",
                option_b="A fraudulent attempt to obtain sensitive information",
                option_c="A security software",
                option_d="A data backup method",
                correct_answer="B",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Phishing is when attackers trick you into revealing passwords or personal information.",
                difficulty="Medium",
                time_limit=40
            ),
            QuizQuestion(
                question_text="What should you do if you receive a suspicious email?",
                option_a="Click all links to verify",
                option_b="Delete it and report as spam",
                option_c="Forward it to friends",
                option_d="Reply immediately",
                correct_answer="B",
                category="Data Security",
                quiz_type="Data Security",
                explanation="Never click links in suspicious emails. Delete and report them as spam.",
                difficulty="Easy",
                time_limit=30
            ),
            
            # AI Ethics - Additional questions
            QuizQuestion(
                question_text="What is machine learning bias?",
                option_a="AI always makes mistakes",
                option_b="AI systems that reflect unfair prejudices from training data",
                option_c="AI being too slow",
                option_d="AI not working at all",
                correct_answer="B",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="ML bias occurs when AI systems perpetuate unfair treatment based on biased training data.",
                difficulty="Hard",
                time_limit=60
            ),
            QuizQuestion(
                question_text="What is informed consent in AI?",
                option_a="Agreeing without understanding",
                option_b="Understanding and agreeing to how your data is used",
                option_c="Forcing users to agree",
                option_d="Not telling users anything",
                correct_answer="B",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="Informed consent means users understand how their data will be used before agreeing.",
                difficulty="Medium",
                time_limit=50
            ),
            QuizQuestion(
                question_text="Should AI decisions be explainable?",
                option_a="No, AI should be a black box",
                option_b="Yes, especially for important decisions",
                option_c="Only sometimes",
                option_d="It doesn't matter",
                correct_answer="B",
                category="AI Ethics",
                quiz_type="AI Ethics",
                explanation="AI decisions affecting people should be explainable, especially for fairness and accountability.",
                difficulty="Medium",
                time_limit=50
            ),
            
            # Social Media Privacy - Additional questions
            QuizQuestion(
                question_text="What is geotagging?",
                option_a="Adding location information to posts",
                option_b="A type of hashtag",
                option_c="A privacy setting",
                option_d="A social media feature",
                correct_answer="A",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="Geotagging adds location data to your posts, which can reveal where you are.",
                difficulty="Easy",
                time_limit=35
            ),
            QuizQuestion(
                question_text="Can social media companies sell your data?",
                option_a="No, never",
                option_b="Yes, often to advertisers and third parties",
                option_c="Only with permission",
                option_d="Only in certain countries",
                correct_answer="B",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="Many platforms share or sell user data to advertisers and partners as part of their business model.",
                difficulty="Medium",
                time_limit=45
            ),
            QuizQuestion(
                question_text="What does 'friends of friends' privacy setting mean?",
                option_a="Only your friends can see",
                option_b="Your friends and their friends can see",
                option_c="Everyone can see",
                option_d="Only you can see",
                correct_answer="B",
                category="Privacy",
                quiz_type="Social Media Privacy",
                explanation="Friends of friends means your content is visible to your friends and their friends too.",
                difficulty="Easy",
                time_limit=30
            ),
            
            # Quick Challenge questions (fast-paced, medium difficulty)
            QuizQuestion(
                question_text="What is the minimum recommended password length?",
                option_a="4 characters",
                option_b="8 characters",
                option_c="12 characters",
                option_d="16 characters",
                correct_answer="C",
                category="Data Security",
                quiz_type="Quick Challenge",
                explanation="12+ characters is recommended for strong passwords.",
                difficulty="Medium",
                time_limit=20
            ),
            QuizQuestion(
                question_text="True or False: Public Wi-Fi is always safe to use.",
                option_a="True",
                option_b="False",
                option_c="Sometimes",
                option_d="Depends on the network",
                correct_answer="B",
                category="Data Security",
                quiz_type="Quick Challenge",
                explanation="Public Wi-Fi can be insecure. Use VPN or avoid sensitive activities.",
                difficulty="Easy",
                time_limit=15
            ),
            QuizQuestion(
                question_text="What is two-factor authentication?",
                option_a="Two passwords",
                option_b="Password plus another verification method",
                option_c="Two email accounts",
                option_d="Two usernames",
                correct_answer="B",
                category="Data Security",
                quiz_type="Quick Challenge",
                explanation="2FA uses password plus SMS, app, or biometric verification.",
                difficulty="Easy",
                time_limit=20
            ),
            QuizQuestion(
                question_text="How often should you update your apps?",
                option_a="Never",
                option_b="When you remember",
                option_c="Regularly, as updates include security patches",
                option_d="Once a year",
                correct_answer="C",
                category="Data Security",
                quiz_type="Quick Challenge",
                explanation="Regular updates include security patches that protect against vulnerabilities.",
                difficulty="Easy",
                time_limit=20
            ),
            QuizQuestion(
                question_text="What is a data breach?",
                option_a="A type of password",
                option_b="Unauthorized access to personal data",
                option_c="A security feature",
                option_d="A backup method",
                correct_answer="B",
                category="Data Security",
                quiz_type="Quick Challenge",
                explanation="A data breach is when unauthorized parties access personal information.",
                difficulty="Easy",
                time_limit=20
            ),
        ]
        
        # Check which questions already exist
        existing_questions = QuizQuestion.query.all()
        existing_texts = {q.question_text for q in existing_questions}
        
        # Add only new questions
        new_questions = [q for q in all_questions if q.question_text not in existing_texts]
        
        if new_questions:
            for q in new_questions:
                db.session.add(q)
            db.session.commit()
            print(f"✅ Added {len(new_questions)} new questions")
        else:
            print("ℹ️  All questions already exist")
        
        # Print summary
        print("\n📊 Question Summary:")
        for qt in quiz_types:
            count = QuizQuestion.query.filter_by(quiz_type=qt.name).count()
            print(f"   {qt.name}: {count} questions")

if __name__ == '__main__':
    print("=" * 70)
    print("ADDING QUIZ QUESTIONS TO DATABASE")
    print("=" * 70)
    add_all_questions()
    print("\n✅ Complete!")


