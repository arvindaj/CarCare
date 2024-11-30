from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB Configuration
CLIENT_NAME = "mongodb://localhost:27017/"
client = MongoClient(CLIENT_NAME)
DB_EMPLOYEE = "TASK"
db = client[DB_EMPLOYEE]

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
jwt = JWTManager(app)

# Collections
newput_collection = db["newput"]
counters_collection = db["counters"]

# Auto-increment helper for `id`
def get_next_id():
    counter = counters_collection.find_one_and_update(
        {"_id": "newput_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return counter["seq"]

# Function to send email
def send_email(to_email, subject, body, attachment=None):
    from_email = 'your_email@gmail.com'
    password = 'your_app_password'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment:
        part = MIMEApplication(attachment, Name="newput_data.pdf")
        part['Content-Disposition'] = 'attachment; filename="newput_data.pdf"'
        msg.attach(part)

    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Function to generate PDF
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="NewPut Data", ln=True, align="C")
    pdf.ln(10)

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.output("/tmp/newput_data.pdf")
    with open("/tmp/newput_data.pdf", "rb") as file:
        return file.read()

# API to add new item
@app.route("/newput", methods=["POST"])
def add_item():
    try:
        data = request.json
        name = data.get("name")
        place = data.get("place")
        date = data.get("date")
        partlist = data.get("partlist")
        email = data.get("email")

        # Validation
        if not all([name, place, date, partlist, email]):
            return jsonify({"error": "All fields are required"}), 400

        # Get the next ID for this entry
        id = get_next_id()

        # Insert into MongoDB
        item = {
            "id": id,
            "name": name,
            "place": place,
            "date": datetime.strptime(date, "%Y-%m-%d"),
            "partlist": partlist,
            "email": email,
        }
        newput_collection.insert_one(item)

        # Generate PDF and send email
        pdf_data = generate_pdf(item)
        subject = "Your NewPut Entry"
        body = f"Hello {name},\n\nYour entry has been recorded successfully. Please find the details attached as a PDF."
        send_email(email, subject, body, pdf_data)

        return jsonify({"message": "Item added successfully and email sent", "id": id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
