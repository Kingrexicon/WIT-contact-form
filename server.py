from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import csv
import os
import re

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session handling


# Faculty and Department Mapping
faculty_departments = {
    "Administration": ["Accounting", "Business Administration", "Public Administration", "Local Government Studies"],
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
            "email", "phone_number", "faculty", "department", "year_level",
            "study_duration", "grad_year", "rcf_year", "admission_mode", "talents",
            "personal_challenge", "challenge_details", "home_church", "worker_home",
            "home_dept", "academic_challenge", "academic_challenge_details",
            "extra_activities", "cgpa", "bornAgain", "bornAgain_details",
            "water", "holyGhost", "baptism_evidence", "guardian_name",
            "guardian_relationship", "guardian_number", "guardian_address",
            "guardian_knows"
        ])

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
    departments = faculty_departments.get(faculty, [])  # Get departments for selected faculty
    return jsonify({"departments": departments})  # Return as JSON

@app.route("/page2", methods=["POST"])
def page2():
    email = request.form.get("email")  
    phone_number = request.form.get("phone_number")  

    print(f"DEBUG - Phone Number Received: {phone_number}")  # ✅ Debugging Line

    if not is_valid_email(email):  
        flash("Invalid email address. Please enter a valid email.")
        return redirect(url_for("form"))  

    if not is_valid_phone_number(phone_number):  
        flash("Invalid phone number. Please enter a valid Nigerian number (e.g., +2348023456789).")
        return redirect(url_for("form"))  

    session["user_data"] = request.form.to_dict()  
    return render_template("page2.html")


@app.route("/page3", methods=["GET", "POST"])
def page3():
    if request.method == "POST":
        user_data = session.get("user_data", {})
        user_data.update(request.form.to_dict())

        # ✅ Save to CSV
        with open(csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(user_data.values())

        session.pop("user_data", None)  # ✅ Clear session after saving
        return redirect(url_for("thank_you"))

    return render_template("page3.html")

@app.route("/thankyou")
def thank_you():
    return render_template("thankyou.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
