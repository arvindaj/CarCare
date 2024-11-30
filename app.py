from flask_pymongo import PyMongo
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from bson import ObjectId
from datetime import datetime
from bson.json_util import dumps  # Import this helper from bson








app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)


CLIENT_NAME ="mongodb://localhost:27017/"
client = MongoClient(CLIENT_NAME)
DB_EMPLOYEE ="TASK"
db = client[DB_EMPLOYEE]
users_collection= db["login"]
appointment_collection = db["APPOINTMENTS_COLLECTION"]
Employees_Collection = db["EMPLOYEE_COLLECTION"]
job_card_collection = db["JOB_CARD_COLLECTION"]
parts_collection = db["Parts_Collection"]
estimations = db["ESTIMATION_COLLECTION"]
car_collection = db["CAR_COLLECTION"]
job_card_collection = db["JOB_CARD_COLLECTION"]
counter_collection = db["ESTIMATION_PDF"]
counters_collection = db["COUNTER_COLLECTION"] 
order_parts_collection = db["Order_Parts_Collection"]
parts_collection = db["Parts_Collection"]
vendors_collection = db["Vendors_Collection"]


app.secret_key = 'secret key'
app.config['JWT_SECRET_KEY'] = 'this-is-secret-key'

@app.route("/")
def hello():
    return "hello 1111"

# Helper function to hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# Helper function to verify password
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = hash_password(password)
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully"}), 201

### Login Endpoint ###
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = users_collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        access_token = create_access_token(identity=str(user["_id"]))
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid username or password"}), 401


# Function to generate auto-incrementing employee ID
def generate_employee_id():
    """Generates an auto-incrementing 6-digit employee ID."""
    last_employee = Employees_Collection.find_one(sort=[("employee_id", -1)])
    return last_employee["employee_id"] + 1 if last_employee else 100001

# Create Employee
@app.route('/employee', methods=['POST'])
def create_employee():
    data = request.json
    employee_id = generate_employee_id()

    # Validate required fields
    required_fields = ['name', 'mobile_number', 'aadhar_number', 'ifsc_code', 'pan_number', 'bank_account_number', 'address']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required."}), 400

    # Create employee data
    input_data = {
        "employee_id": employee_id,
        "name": data['name'],
        "mobile_number": data['mobile_number'],
        "alternate_number": data.get('alternate_number'),  # Optional
        "aadhar_number": data['aadhar_number'],
        "ifsc_code": data['ifsc_code'],
        "pan_number": data['pan_number'],
        "bank_account_number": data['bank_account_number'],
        "address": data['address']
    }

    result = Employees_Collection.insert_one(input_data)
    return jsonify({"employee_id": employee_id}), 201  # Return employee_id


##stock
db.vendors.find()
def convert_objectid_to_str(doc):
    """Convert all ObjectId fields in the document to strings."""
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

@app.route('/add-part', methods=['POST'])
def add_part():
    data = request.json

    # Ensure part_id is a three-digit number (e.g., 001, 002, ...)
    part_id = data.get('part_id')
    
    if not part_id:
        # If part_id is not provided, generate the next part_id as a three-digit integer
        last_part = parts_collection.find_one(sort=[("_id", -1)])  # Find the last inserted part
        last_part_id = int(last_part['_id']) if last_part else 0  # If no part exists, start from 0
        part_id = f"{last_part_id + 1:03d}"  # Format as three digits (e.g., '001')

    # Ensure part_id is a valid string (not None or other invalid types)
    if not isinstance(part_id, str) or len(part_id) != 3:
        return jsonify({"error": "Invalid part_id format. It should be a three-digit string."}), 400

    # Check if the part already exists
    existing_part = parts_collection.find_one({"_id": part_id})
    if existing_part:
        return jsonify({"error": "Part with the same ID already exists"}), 400
    
    # Validate unit_price
    try:
        unit_price = float(data.get('unit_price'))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid 'unit_price'. It must be a numeric value."}), 400

    # Insert the part data
    part_data = {
        "_id": part_id,
        "name": data.get('name'),
        "unit_price": unit_price,
        "discount": data.get('discount', 0)
    }

    # Ensure all required fields are present
    if not part_data.get("name") or not part_data.get("unit_price"):
        return jsonify({"error": "Missing required fields: 'name' or 'unit_price'."}), 400

    try:
        parts_collection.insert_one(part_data)
    except Exception as e:
        return jsonify({"error": f"Failed to insert part: {str(e)}"}), 500

    return jsonify({"message": "Part added successfully", "part_id": part_id}), 201


# Function to generate auto-incrementing customer ID
def generate_customer_id():
    """Generates an auto-incrementing customer ID."""
    last_appointment = appointment_collection.find_one(sort=[("customer_id", -1)])
    return last_appointment["customer_id"] + 1 if last_appointment else 1001

import datetime
# Create Appointment
@app.route("/appointment", methods=["POST"])
def create_appointment():
    data = request.json

 # Validate required fields
    required_fields = ['name', 'mobile_number', 'address', 'car_number', 'email']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400


    customer_id = generate_customer_id()
    appointment = {
        "customer_id": customer_id,
        'name': data['name'],
        'mobile_number': data['mobile_number'],
        'alternative_number': data.get('alternative_number'),
        'address': data['address'],
        'car_number': data['car_number'],
        'email': data['email'],
        'created_at': datetime.datetime.now()
    }
    try:
        appointment_collection.insert_one(appointment)
    except Exception as e:
        return jsonify({'error': f'Error creating appointment: {str(e)}'}), 500

    return jsonify({'message': 'Appointment created successfully', 'appointment_id': customer_id}), 201

# Initialize the job card counter in MongoDB if it does not exist
def initialize_job_card_counter():
    if counters_collection.find_one({"_id": "job_card_id"}) is None:
        counters_collection.insert_one({"_id": "job_card_id", "sequence_value": 0})

initialize_job_card_counter()

# Generate a new job card ID by incrementing the counter
def get_next_job_card_id():
    result = counters_collection.find_one_and_update(
        {"_id": "job_card_id"},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    return result["sequence_value"]

# Helper function to validate employee and customer existence
def is_valid_employee(employee_id):
    """Check if employee exists."""
    return Employees_Collection.find_one({"employee_id": int(employee_id)}) is not None

def is_valid_customer(customer_id):
    """Check if customer exists."""
    return appointment_collection.find_one({"customer_id": int(customer_id)}) is not None

def get_employee_details(employee_id):
    """Fetch employee details by ID."""
    return Employees_Collection.find_one({"employee_id": int(employee_id)})

def get_customer_details(customer_id):
    """Fetch customer details by customer ID."""
    return appointment_collection.find_one({"customer_id": int(customer_id)})

# Create Job Card
@app.route("/api/job_card", methods=["POST"])
def create_job_card():
    data = request.json
    employee_id = data.get("employee_id")
    customer_id = data.get("customer_id")
    
    # Fetch employee and customer details
    employee = get_employee_details(employee_id)
    customer = get_customer_details(customer_id)
    
    # Validate that both employee and customer exist
    if not employee:
        return jsonify({"error": "Invalid employee ID"}), 404
    if not customer:
        return jsonify({"error": "Invalid customer ID"}), 404
    
    # Create a new car entry in the car collection
    car_data = {
        "car_model": data.get('car_model'),
        "car_make": data.get('car_make'),
        "year": data.get('year'),
    }
    car = car_collection.insert_one(car_data)
    car_id = str(car.inserted_id)  # Store car's ObjectId

    # Generate a unique job card ID as an integer
    job_card_id = get_next_job_card_id()
    
    # Prepare job card data, including the car ID
    job_card = {
        "job_card_id": job_card_id,  # Use integer job card ID
        "employee_id": employee_id,
        "customer_id": customer_id,
        "employee_name": employee.get("name"),
        "customer_name": customer.get("name"),
        "service_type": data.get("service_type"),
        "labour_cost": data.get("labour_cost"),
        "car_image": data.get("car_image"),
        "car_id": car_id,  # Add car ID reference here
        "fuel_type": data.get('fuel_type'),
        "vehicle_colour": data.get('vehicle_colour'),
        "chasse_number": data.get('chasse_number'),
        "estimation_delivery_date": data.get('estimation_delivery_date'),
        "insurance_company": data.get('insurance_company'),
        "advance_payment": data.get('advance_payment'),
        "customer_details": {
            "customer_id": customer.get("customer_id"),
            "name": customer.get("name"),
            "address": customer.get("address"),
            "car_number": customer.get("car_number"),
            "email": customer.get("email"),
            "mobile_number": customer.get("mobile_number"),
            "alternative_number": customer.get("alternative_number"),
        }
    }
    
    # Insert job card into the collection and get the inserted ID
    inserted_id = job_card_collection.insert_one(job_card).inserted_id
    job_card["_id"] = str(inserted_id)  # Convert ObjectId to string for JSON serialization

    return jsonify({"message": f"Job card successfully created with ID {job_card_id}", "job_card": job_card}), 201


# Function to send email
def send_email(to_email, subject, body, attachment=None):
    from_email = ''
    password = ''
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment:
        part = MIMEApplication(attachment, Name="estimation.pdf")
        part['Content-Disposition'] = 'attachment; filename="estimation.pdf"'
        msg.attach(part)

    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# PDF generation function
def generate_pdf(estimation_details):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 40, "Estimation Details")

    y_position = height - 80
    c.setFont("Helvetica", 12)
    c.drawString(100, y_position, f"Estimation ID: {estimation_details['estimation_id']}")
    y_position -= 20
    c.drawString(100, y_position, f"Job Card ID: {estimation_details['jobcard_id']}")
    y_position -= 20
    c.drawString(100, y_position, f"Total Price: {estimation_details['total_price']}")
    y_position -= 20
    c.drawString(100, y_position, f"Total Part Price: {estimation_details['part_value']}")
    y_position -= 20
    c.drawString(100, y_position, f"Discount: {estimation_details['discount']}")
    y_position -= 20
    c.drawString(100, y_position, f"Tax: {estimation_details['tax']}")

    # Part details
    y_position -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y_position, "Parts:")
    y_position -= 20
    c.setFont("Helvetica", 10)

    for part in estimation_details['parts']:
        c.drawString(100, y_position, f"Part: {part['name']} | Quantity: {part['quantity']} | Price: {part['unit_price']} | Total: {part['total_price']}")
        y_position -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

# Create estimation API
# Function to generate the next estimation_id (4-digit integer)
def generate_estimation_id():
    counter = counter_collection.find_one_and_update(
        {"_id": "estimation_id_counter"},
        {"$inc": {"counter": 1}},
        upsert=True,
        return_document=True
    )
    estimation_id = counter["counter"]
    if estimation_id > 9999:
        estimation_id = 1000
        counter_collection.update_one({"_id": "estimation_id_counter"}, {"$set": {"counter": estimation_id}})
    return estimation_id

@app.route('/estimation', methods=['POST'])
def create_estimation():
    data = request.json
    required_fields = ['customer_id', 'jobcard_id', 'estimation_parts']

    # Check for required fields
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Log the received data for debugging
    print(f"Received data: {data}")

    # Generate estimation ID
    estimation_id = generate_estimation_id()

    # Check if job card exists
    job_card_id = data.get('jobcard_id')
    job_card = job_card_collection.find_one({'job_card_id': int(job_card_id)}) 

    
    # Debug: Log job card lookup
    print(f"Looking for job card with ID {job_card_id}: {job_card}")
    
    if not job_card:
        return jsonify({"error": "Job card not found"}), 404

    # Check if the customer_id matches the one from the job card
    customer_id = data.get('customer_id')
    if job_card['customer_id'] != customer_id:
        return jsonify({"error": "Customer ID does not match job card"}), 400

    # Process parts for the estimation
    inward_parts = data.get('estimation_parts')
    fetched_parts = []
    total_part_price = 0
    
    for part in inward_parts:
        part_id = part.get('part_id')
        quantity = part.get('quantity')

        try:
            # Convert quantity to integer
            quantity = int(quantity)
        except ValueError:
            return jsonify({"error": f"Invalid quantity for part ID {part_id}"}), 400

        # Fetch part data from the database
        part_data = parts_collection.find_one({"_id": str(part_id)})
        if not part_data:
            return jsonify({"error": f"Part with ID {part_id} not found"}), 404

        try:
            # Convert unit_price to float
            unit_price = float(part_data['unit_price'])
        except ValueError:
            return jsonify({"error": f"Invalid unit price for part ID {part_id}"}), 500

        # Calculate part cost
        part_cost = unit_price * quantity
        total_part_price += part_cost

        fetched_parts.append({
            "part_id": part_id,
            "name": part_data['name'],
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": part_cost
        })

    # Calculate total price with service cost, discount, and tax
    service_cost = data.get("service_cost", 0)
    discount = data.get("discount", 0)
    tax = data.get("tax", 0)
    total_price = (service_cost + total_part_price) - discount + tax

    # Create new estimation object
    new_estimation = {
        "estimation_id": estimation_id,
        "jobcard_id": job_card_id,
        "part_value": total_part_price,
        "parts": fetched_parts,
        "service_cost": service_cost,
        "discount": discount,
        "tax": tax,
        "total_price": total_price,
        "is_accepted": None,  # Field to track acceptance status
        "decision_timestamp": None  # Field to track when the decision was made
    }
    estimations.insert_one(new_estimation)

    return jsonify({
        "message": "Estimation created successfully!",
        "estimation_id": estimation_id,
        "total_price": total_price,
        "total_part_price": total_part_price,
        "tax": tax
    }), 201


# Retrieve a single estimation by estimation_id
@app.route('/estimation/<int:estimation_id>', methods=['GET'])
def get_estimation_by_id(estimation_id):
    estimation = estimations.find_one({"estimation_id": estimation_id})
    if estimation:
        estimation_json = dumps(estimation)
        return jsonify({"estimation": estimation_json}), 200
    return jsonify({"error": "Estimation not found!"}), 404

# API to send estimation PDF
@app.route('/send_estimation_pdf/<int:estimation_id>', methods=['POST'])
def send_estimation_pdf(estimation_id):
    estimation = estimations.find_one({"estimation_id": estimation_id})
    
    if not estimation:
        return jsonify({"error": f"Estimation with ID {estimation_id} not found!"}), 404
    
    job_card = job_card_collection.find_one({"job_card_id": estimation['jobcard_id']})
    if not job_card:
        return jsonify({"error": "Job card not found!"}), 404

    customer_email = job_card.get("customer_details", {}).get("email")
    if not customer_email:
        return jsonify({"error": "Customer email not found!"}), 404

    subject = "Estimation for your vehicle repair"

    # Link to the double-check confirmation page
    double_check_url = f"http://localhost:5000/estimation/{estimation_id}/double_check"

    body = f"""\
Dear {job_card['customer_name']},

Please find attached the estimation details for your vehicle repair.

To proceed, please confirm your decision by visiting the following link:
- [Confirm Decision]({double_check_url})

Best regards,
Your Service Team
"""

    pdf_attachment = generate_pdf(estimation)
    send_email(customer_email, subject, body, pdf_attachment)

    # Update estimation status to indicate the PDF is sent and awaiting a decision
    estimations.update_one(
        {"estimation_id": estimation_id},
        {"$set": {"status": "pending_decision"}}
    )

    return jsonify({"message": "Estimation PDF sent successfully!"}), 200

# Endpoint for double-check confirmation page
@app.route('/estimation/<int:estimation_id>/double_check', methods=['GET'])
def double_check_estimation(estimation_id):
    estimation = estimations.find_one({"estimation_id": estimation_id})
    
    if not estimation:
        return "<h3>Estimation not found!</h3>", 404

    # Render HTML with Accept and Reject buttons
    return f"""
        <html>
        <head><title>Confirm Your Decision</title></head>
        <body>
            <h2>Estimation ID: {estimation_id}</h2>
            <p>Please confirm your choice for this estimation:</p>
            <form action="/estimation/{estimation_id}/confirm_accept" method="POST">
                <button type="submit" style="padding:10px; color:white; background-color:green;">Accept</button>
            </form>
            <br>
            <form action="/estimation/{estimation_id}/confirm_reject" method="POST">
                <button type="submit" style="padding:10px; color:white; background-color:red;">Reject</button>
            </form>
        </body>
        </html>
    """


# Endpoint to accept the estimation via email link
# Endpoint to confirm acceptance from the double-check page
@app.route('/estimation/<int:estimation_id>/confirm_accept', methods=['POST'])
def confirm_accept_estimation(estimation_id):
    result = estimations.update_one(
        {"estimation_id": estimation_id},
        {"$set": {"is_accepted": True, "decision_timestamp": datetime.now()}}
    )
    if result.matched_count:
        return "<h3>Thank you! You have confirmed acceptance of the estimation.</h3>", 200
    return "<h3>Estimation not found!</h3>", 404

# Endpoint to confirm rejection from the double-check page
@app.route('/estimation/<int:estimation_id>/confirm_reject', methods=['POST'])
def confirm_reject_estimation(estimation_id):
    result = estimations.update_one(
        {"estimation_id": estimation_id},
        {"$set": {"is_accepted": False, "decision_timestamp": datetime.now()}}
    )
    if result.matched_count:
        return "<h3>Thank you! You have confirmed rejection of the estimation.</h3>", 200
    return "<h3>Estimation not found!</h3>", 404



if __name__ == '__main__':
    app.run(debug=True)
