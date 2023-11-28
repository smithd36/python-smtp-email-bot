import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import sqlite3
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

PORT = 587
SMTP_SERVER = "smtp-mail.outlook.com"
TIME_ZONE = "US/Mountain" # nm time

# Load environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")
db_file = os.getenv("DB_FILE")

def send_email(subject, receiver_emails, name, expirationDate, columnName, days_before_expiration):
    try:
        # Create a time zone object
        time_zone = pytz.timezone(TIME_ZONE)

        # Convert the current date to the specified time zone
        current_date_mst = datetime.now(tz=time_zone)

        # Create basis message
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = formataddr(("ResQCert Email Bot", sender_email))
        msg["To"] = ", ".join(receiver_emails)  # Join the emails

        # Create message body
        body = f"Hello,\n\n{name}'s {columnName} is expiring on {expirationDate}. Only {days_before_expiration} day(s) left.\n\nBest regards,\nYour Email Agent"
        msg.set_content(body)

        # Add HTML version
        html_content = f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <p>Hello,</p>
                <p>{name}'s {columnName} is expiring on {expirationDate}. Only {days_before_expiration} day(s) left.</p>
                <p>Best regards,</p>
                <p>ResQCert Email Bot</p>
            </body>
        </html>
        """
        msg.add_alternative(html_content, subtype="html")

        # Send email
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


def get_expiration_date():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Define the columns and their corresponding names
    columns = [
        ("dotExp", "DOT License"),
        ("emsExp", "EMS License"),
        ("driversExp", "Drivers License"),
        ("blsExp", "BLS License"),
        ("mvrExp", "MVR License")
    ]

    # Get the current date
    current_date = datetime.now()

    # Iterate over the columns
    for column, license_name in columns:
        query = f"SELECT email, name, {column} FROM employees WHERE {column} IS NOT NULL"
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            email, name, expiration_date = row

            # Check if the value is a date
            try:
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d')
            except ValueError:
                # Skip non-date values and print a warning
                print(f"Skipping non-date value: {expiration_date}")
                continue

            days_before_expiration = (expiration_date - current_date).days

            # Check if the difference is 60, 30, 15, or 1 day
            if days_before_expiration in [90, 60, 45, 30, 15, 7, 1]:
                # Send email
                send_email(
                    "NOTICE: Upcoming Expiration",
                    ["Dreysmith101@gmail.com"],
                    name,
                    expiration_date.strftime('%Y-%m-%d'),
                    license_name,
                    days_before_expiration
                )

    # Close the cursor and database connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    get_expiration_date()