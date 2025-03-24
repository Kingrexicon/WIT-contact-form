import re
import os
import csv
from config import CSV_FILE, CSV_FIELDS

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_valid_phone_number(phone):
    pattern = r"^\+234\d{10}$"
    return re.match(pattern, phone) is not None

def save_to_csv(user_data):
    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writerow(user_data)

def handle_file_upload(passport_photo, user_data):
    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)
    
    if passport_photo and user_data.get("first_name") and user_data.get("last_name") and user_data.get("middle_name"):
        first_name = user_data["first_name"].strip().lower()
        last_name = user_data["last_name"].strip().lower()
        middle_name = user_data["middle_name"].strip().lower()
        file_extension = os.path.splitext(passport_photo.filename)[1]
        new_filename = f"{first_name}{last_name}{middle_name}{file_extension}"
        photo_path = os.path.join(upload_folder, new_filename)
        passport_photo.save(photo_path)
        return photo_path
    return None