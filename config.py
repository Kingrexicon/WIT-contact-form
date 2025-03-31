from dotenv import load_dotenv
import csv
import os

load_dotenv()

# Flask config
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")

# Email config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("MAIL_SENDER")
SENDER_PASSWORD = os.getenv("MAIL_PASSWORD")

# CSV config
CSV_FILE = "submissions.csv"
CSV_FIELDS = [
    "first_name", "middle_name", "last_name", "email", "phone_number", "state", 
    "birth_place", "home_address", "campus_address", "gender", "marital", 
    "faculty", "department", "year_level", "study_duration", "grad_year", 
    "rcf_year", "admission_mode", "talents", "personal_challenge", 
    "challenge_details", "home_church", "worker_home", "home_dept", 
    "academic_challenge", "academic_challenge_details", "extra_activities", 
    "cgpa", "bornAgain", "bornAgain_details", "water_baptism", "holyGhost", 
    "baptism_evidence", "passport_photo", "guardian_name", "guardian_relationship", 
    "guardian_number", "guardian_address", "guardian_awareness"
]

# Faculty and departments
FACULTY_DEPARTMENTS = {
    "Administration": ["Accounting", "Business Administration", "Public Administration", "Local Government Studies", "International Relations"],
    "Agriculture": ["Agricultural Economics", "Animal Science", "Crop Production", "Soil Science"],
    "Arts": ["English", "History", "Philosophy", "Music", "Linguistics"],
    "Basic Medical Sciences": ["Anatomy", "Medical Biochemistry", "Medical Rehabilitation", "Physiology"],
    "Clinical Sciences": ["Medicine and Surgery", "Nursing"],
    "Dentistry": ["Dentistry"],
    "Education": ["Educational Management", "Physical & Health Education", "Educational Foundations", "Guidance & Counselling"],
    "Environmental Design and Management": ["Architecture", "Building", "Estate Management", "Fine and Applied Arts", "Quantity Surveying", "Survey and Geoinformatics", "Urban & Regional Planning"],
    "Law": ["Law"],
    "Pharmacy": ["Pharmacy"],
    "Science": ["Biochemistry", "Botany", "Chemistry", "Computer Science", "Mathematics", "Microbiology", "Physics", "Zoology"],
    "Social Sciences": ["Economics", "Geography", "Political Science", "Psychology", "Sociology"],
    "Technology": ["Agricultural Engineering", "Chemical Engineering", "Civil Engineering", "Computer Engineering", "Electrical & Electronics Engineering", "Mechanical Engineering", "Materials Science & Engineering", "Food Science & Technology"]
}

# Ensure CSV exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(CSV_FIELDS)