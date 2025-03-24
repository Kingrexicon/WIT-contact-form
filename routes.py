from flask import render_template, request, redirect, session, url_for, flash, jsonify
from email_utils import send_email
from form_utils import is_valid_email, is_valid_phone_number, save_to_csv, handle_file_upload
from config import FACULTY_DEPARTMENTS


def register_routes(app):
    @app.route("/")
    def form():
        return render_template("index.html")

    @app.route("/get_departments")
    def get_departments():
        faculty = request.args.get("faculty")
        departments = FACULTY_DEPARTMENTS.get(faculty, [])
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
        if "user_data" in session:
            return render_template("page3.html")
        return redirect(url_for("form"))

    @app.route("/submit_final", methods=["POST"])
    def submit_final():
        if request.method == "POST":
            user_data = session.get("user_data", {})
            user_data.update(request.form.to_dict())

            passport_photo = request.files.get("passport_photo")
            if passport_photo:
                photo_path = handle_file_upload(passport_photo, user_data)
                if photo_path:
                    user_data["passport_photo"] = photo_path

            save_to_csv(user_data)

            user_email = user_data.get("email")
            recipient_name = user_data.get("first_name", "Participant")
            email_subject = "Welcome to the Workers In Training Group – Rain Semester 2025"

            default_email_body = f"""Dear {recipient_name},

Congratulations! 🎉 We are delighted to officially welcome you to the Workers In Training (WIT) Group for the Rain Semester 2025.

We are truly blessed to have you join us. Prayers have been made, words have gone ahead, and we believe great things are in store for you.

✨ You are in the right place! ✨ We will get back to you in real time.

Once again, welcome! We look forward to seeing you soon.

Best regards,
WIT Registrar & WIT Coordinator"""

            try:
                with open("email_template.txt", "r", encoding="utf-8") as template_file:  # Use UTF-8
                    lines = [line for line in template_file.readlines() if not line.strip().startswith('#')]
                    email_template = ''.join(lines)
                email_body = email_template.format(recipient_name=recipient_name)
            except (FileNotFoundError, KeyError):
                email_body = default_email_body

            send_email(user_email, email_subject, email_body)

            session.pop("user_data", None)
            return redirect(url_for("thank_you"))

    # ... (other routes unchanged)

    @app.route("/thankyou")
    def thank_you():
        return render_template("thankyou.html")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("notfound.html"), 404