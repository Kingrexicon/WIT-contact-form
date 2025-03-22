from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from email.mime.text import MIMEText
from dotenv import load_dotenv
import csv
import os
import re
import smtplib

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("APP_SECRET_KEY")

# Faculty and Department Mapping
faculty_departments = {
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

# Ensure CSV file exists with headers
csv_file = "submissions.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "first_name", "middle_name", "last_name", "email", "phone_number", "state", 
            "birth_place", "home_address", "campus_address", "gender", "marital",  # Added index.html fields
            "faculty", "department", "year_level", "study_duration", "grad_year", 
            "rcf_year", "admission_mode", "talents", "personal_challenge", 
            "challenge_details", "home_church", "worker_home", "home_dept", 
            "academic_challenge", "academic_challenge_details", "extra_activities", 
            "cgpa", "bornAgain", "bornAgain_details", "water_baptism", "holyGhost", 
            "baptism_evidence", "passport_photo", "guardian_name", "guardian_relationship", 
            "guardian_number", "guardian_address", "guardian_awareness"
        ])

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.getenv("MAIL_SENDER")
SENDER_PASSWORD = os.getenv("MAIL_PASSWORD")

# Function to send email
def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# ✅ Email validation function
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# ✅ Phone number validation function
def is_valid_phone_number(phone):
    pattern = r"^\+234\d{10}$"  # Starts with +234, followed by exactly 10 digits
    return re.match(pattern, phone) is not None

@app.route("/")
def form():
    return render_template("index.html")

@app.route("/get_departments")
def get_departments():
    faculty = request.args.get("faculty")
    departments = faculty_departments.get(faculty, [])
    return jsonify({"departments": departments})

@app.route("/page2", methods=["GET", "POST"])
def page2():
    if request.method == "POST":
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")

        if not email:
            flash("Email field is required.")
            return redirect(url_for("form"))
        if not is_valid_email(email):
            flash("Invalid email address. Please enter a valid email.")
            return redirect(url_for("form"))
        if not phone_number:
            flash("Phone number is required.")
            return redirect(url_for("form"))
        if not is_valid_phone_number(phone_number):
            flash("Invalid phone number. Please enter a valid Nigerian number (e.g., +2348023456789).")
            return redirect(url_for("form"))

        session["user_data"] = request.form.to_dict()
        return render_template("page2.html")
    return render_template("page2.html")

@app.route("/page3", methods=["GET", "POST"])
def page3():
    if request.method == "POST":
        user_data = session.get("user_data", {})
        user_data.update(request.form.to_dict())
        session["user_data"] = user_data
        return render_template("page3.html")
    # For GET requests, just render page3 if there's data, otherwise redirect to start
    if "user_data" in session:
        return render_template("page3.html")
    return redirect(url_for("form"))

@app.route("/submit_final", methods=["POST"])
def submit_final():
    if request.method == "POST":
        # Get all data from session and update with page3 data
        user_data = session.get("user_data", {})
        user_data.update(request.form.to_dict())

        # Ensure upload directory exists
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        # Handle file upload
        passport_photo = request.files.get("passport_photo")
        if passport_photo and user_data.get("first_name") and user_data.get("last_name") and user_data.get("middle_name"):
            first_name = user_data["first_name"].strip().lower()
            last_name = user_data["last_name"].strip().lower()
            middle_name = user_data["middle_name"].strip().lower()

            # Get file extension
            file_extension = os.path.splitext(passport_photo.filename)[1]

            # Construct new filename
            new_filename = f"{first_name}{last_name}{middle_name}{file_extension}"
            photo_path = os.path.join(upload_folder, new_filename)

            # Save file
            passport_photo.save(photo_path)
            user_data["passport_photo"] = photo_path  # Store path in CSV

        # Save to CSV
        with open(csv_file, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "first_name", "middle_name", "last_name", "email", "phone_number", "state",
                "birth_place", "home_address", "campus_address", "gender", "marital",
                "faculty", "department", "year_level", "study_duration", "grad_year",
                "rcf_year", "admission_mode", "talents", "personal_challenge",
                "challenge_details", "home_church", "worker_home", "home_dept",
                "academic_challenge", "academic_challenge_details", "extra_activities",
                "cgpa", "bornAgain", "bornAgain_details", "water_baptism", "holyGhost",
                "baptism_evidence", "passport_photo", "guardian_name", "guardian_relationship",
                "guardian_number", "guardian_address", "guardian_awareness"
            ])
            writer.writerow(user_data)

        # Send email to the user
        user_email = user_data.get("email")
        recipient_name = user_data.get("first_name", "Participant")  # Default to 'Participant' if no name is provided
        registrar_link = os.getenv("WHATSAPP_LINK")

        email_subject = "Welcome to the Workers In Training Group – Rain Semester 2025"
        email_body = f"""Dear {recipient_name},

        Congratulations! 🎉 We are delighted to officially welcome you to the Workers In Training (WIT) Group for the Rain Semester 2025.

        We are truly blessed to have you join us. Prayers have been made, words have gone ahead, and we believe great things are in store for you.

        ✨ You are in the right place! ✨

        For the next steps, please access the Registrar for further instructions by clicking the link below:

        🔗 [Access the Registrar Here]({registrar_link})

        Once again, welcome! We look forward to seeing you soon.

        Best regards,  
        WIT Registrar & WIT Coordinator
        """

        send_email(user_email, email_subject, email_body)

        # Clear session after saving
        session.pop("user_data", None)

        return redirect(url_for("thank_you"))

@app.route("/thankyou")
def thank_you():
    return render_template("thankyou.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html"), 404

if __name__ == "__main__":
    app.run(debug=True)