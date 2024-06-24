from flask import Flask, render_template, request, redirect, url_for
import vonage
import mysql.connector
from datetime import datetime, timedelta
import time

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': '#PY05J8228',
    'host': 'localhost',
    'database': 'simpleturf'
}

# Vonage configuration
vonage_client = vonage.Client(key='ecf52b8b', secret='ypOZpaedsGJRv6Cr')
sms_client = vonage.Sms(vonage_client)

# Helper function to send SMS using Vonage
def send_sms(phone_number, message_body):
    responseData = sms_client.send_message({
        'from': 'Vonage APIs',
        'to': phone_number,
        'text': message_body
    })
    return responseData

# Fetch time slots and booking slots from the database
def fetch_time_slots(city, turf):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT details, slot, bookings FROM turfdatas WHERE city = %s AND turf = %s", (city, turf))
    result = cursor.fetchone()
    conn.close()
    if result:
        details, slot, bookings = result
        turf_details, owner_phone_number = parse_turf_details(details)
        return turf_details, slot.split(','), bookings.split(',') if bookings else [], owner_phone_number
    else:
        return [], [], [], None

# Function to parse turf details and extract the owner's phone number
def parse_turf_details(details):
    turf_details = []
    owner_phone_number = None
    details_list = details.split(', ')
    for detail in details_list:
        if ':' in detail:
            try:
                key, value = detail.split(': ', 1)
                if key.strip().lower() == 'phone no':
                    owner_phone_number = value.strip()
                turf_details.append((key.strip(), value.strip()))
            except ValueError:
                pass  # Ignore improperly formatted details
    return turf_details, owner_phone_number

# Function to update booking slots in the database
def update_booking_slots(city, turf, new_bookings):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE turfdatas SET bookings = %s WHERE city = %s AND turf = %s", (','.join(new_bookings), city, turf))
    conn.commit()
    conn.close()

# Function to reset booking slots at midnight
def reset_booking_slots():
    while True:
        now = datetime.now()
        midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_time = (midnight - now).total_seconds()
        time.sleep(sleep_time)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE turfdatas SET bookings = ''")
        conn.commit()
        conn.close()

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city']
        return redirect(url_for('turfs', city=city_name))
    else:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT city FROM turfdatas")
        cities = [row[0] for row in cursor.fetchall()]
        conn.close()
        return render_template('index.html', cities=cities)

# Route for showing turfs of the selected city
@app.route('/turfs/<city>')
def turfs(city):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT turf FROM turfdatas WHERE city = %s", (city,))
    turfs_data = cursor.fetchall()  # Fetch all turfs
    conn.close()
    turfs = [turf[0] for turf in turfs_data]
    return render_template('turfs.html', city=city, turfs=turfs)

# Route for showing details and booking form
@app.route('/details/<city>/<turf>', methods=['GET', 'POST'])
def details(city, turf):
    details, slots, booking_slots, owner_phone_number = fetch_time_slots(city, turf)

    if request.method == 'POST':
        phone_number = request.form['phone_number']
        time_slot = request.form['time_slot']

        # Check if the time slot is already booked
        if time_slot in booking_slots:
            return render_template('error.html', message="This time slot is already booked.")

        # Update booking slots
        booking_slots.append(time_slot)
        update_booking_slots(city, turf, booking_slots)

        # Send SMS to the user
        user_message = f"Congratulations! You have successfully booked {turf}. Your time slot is {time_slot}."
        user_response = send_sms(phone_number, user_message)

        # Send SMS to the owner
        owner_message = f"Your {turf} has been booked by {phone_number}. The time slot is {time_slot}."
        owner_response = send_sms(owner_phone_number, owner_message)

        if user_response["messages"][0]["status"] == "0" and owner_response["messages"][0]["status"] == "0":
            return render_template('success.html', turf=turf, time_slot=time_slot, phone_number=phone_number)
        else:
            return render_template('error.html', message="Booking failed. Please try again.")

    return render_template('details.html', city=city, turf=turf, details=details, slots=slots, booking_slots=booking_slots)

# Route to display the form to add new turfs
@app.route('/add_turf', methods=['GET'])
def add_turf():
    return render_template('add_turf.html')

# Route to handle the form submission and add the new turf to the database
@app.route('/add_turf', methods=['POST'])
def add_turf_post():
    city = request.form['city']
    turf = request.form['turf']
    details = request.form['details']
    slot = request.form['slot']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO turfdatas (city, turf, details, slot) VALUES (%s, %s, %s, %s)", (city, turf, details, slot))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
