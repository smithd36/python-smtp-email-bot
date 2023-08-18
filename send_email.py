import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
from datetime import date, timedelta
from datetime import datetime

PORT = 587
SMTP_SERVER = "smtp-mail.outlook.com"

# Load environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("EMAIL")
password_email = os.getenv("PASSWORD")
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")


def get_expirationDate():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the columns and their corresponding names
    columns = [
        ("dotExp", "DOT License"),
        ("palsExp", "PALS License"),
        ("aclsExp", "ACLS License"),
        ("emsExp", "EMS License"),
        ("driversExp", "Drivers License"),
        ("blsExp", "BLS License"),
        ("mvrExp", "MVR License")
    ]

    # Get the current date
    current_date = date.today()

    # Initialize the variables
    expiration_date = None
    column_name = None

    # Iterate over the columns
    for column in columns:
        column_name = column[1]
        query = "SELECT {} FROM employees WHERE {} IS NOT NULL".format(column[0], column[0])
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            expiration_date = row[0]
            difference = expiration_date - current_date

            # Check if the difference is 60, 30, 15, or 1 day
            if difference in [timedelta(days=90), timedelta(days=60), timedelta(days=45), timedelta(days=30), timedelta(days=15), timedelta(days=7), timedelta(days=1)]:
                # Calculate the number of days before expiration
                days_before_expiration = (expiration_date - current_date).days

                # Get the associated person's email
                query = "SELECT EMAIL, NAME FROM employees WHERE {} = %s".format(column[0])
                cursor.execute(query, (expiration_date,))
                result = cursor.fetchone()

                if result:
                    email = result[0]
                    name = result[1]

                    # Send email
                    # Modify the send_email function call in get_expirationDate function
                    send_email(
                        "NOTICE: Upcoming Expiration",
                        ["Dreysmith101@gmail.com, piglife60@gmail.com"],  # Add the additional email addresses here
                        name,
                        str(expiration_date),
                        column_name,
                        days_before_expiration
                    )                   


    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Return the expiration date and column name
    return expiration_date, column_name

def send_email(subject, receiver_email, name, expirationDate, columnName, days_before_expiration):
    # Create basis message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("ResQCert Email Bot", sender_email))
    msg["To"] = ", ".join(receiver_email)  # Join the emails

    # Create message body
    msg.set_content(f"Hello,\n\n{name}'s {columnName} is expiring on {expirationDate}. Only {days_before_expiration} day(s) left.\n\nBest regards,\nYour Email Agent")

    # Add HTML version
    msg.add_alternative(f"""\
    <!DOCTYPE html>
    <html>
        <body>
            <p>Hello,</p>
            <p>{name}'s {columnName} is expiring on {expirationDate}. Only {days_before_expiration} day(s) left.</p>
            <p>Best regards,</p>
            <p>ResQCert Email Bot</p>
        </body>
    </html>
    """, subtype="html")

    # Send email
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.send_message(msg)

if __name__ == "__main__":
    expiration_date, column_name = get_expirationDate()