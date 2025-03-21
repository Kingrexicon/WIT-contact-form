from flask import Flask, render_template, request, redirect, session, url_for, flash
import csv
import os
import re

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Required for session handling

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

@app.route("/page2", methods=["POST"])
def page2():
    email = request.form.get("email")  # Get email from form data
    phone_number = request.form.get("phone_number")  # Get phone number

    if not is_valid_email(email):  
        flash("Invalid email address. Please enter a valid email.")
        return redirect(url_for("form"))  # Stay on index.html

    if not is_valid_phone_number(phone_number):  
        flash("Invalid phone number. Please enter a valid Nigerian number (e.g., +2348023456789).")
        return redirect(url_for("form"))  # Stay on index.html

    session["user_data"] = request.form.to_dict()  # Store user data
    return render_template("page2.html")  # Move to page2.html

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
