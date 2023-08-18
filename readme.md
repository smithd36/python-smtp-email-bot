# Expiration Date Notifier Bot

This is a Python script that connects to a MySQL database and checks for upcoming expiration dates for various licenses. It sends email notifications to the concerned individuals when an expiration date is approaching. The script utilizes the smtplib library to send emails via an Outlook SMTP server.

# Features
Connects to a MySQL database to retrieve expiration dates for various licenses.
Sends email notifications using an Outlook SMTP server.
Supports multiple licenses and configurable notification intervals.

# Prerequisites
Before running the script, ensure that you have the following:

Python 3.x installed on your system.
Required Python packages: smtplib, email, pathlib, mysql.connector, dotenv.
An Outlook email account for sending notifications.
Access to a MySQL database with the required credentials.

# Setup
To set up and configure the script, follow these steps:

1. Clone the repository or download the script to your local machine.
2. Install the required Python packages by running the following command:
- pip install smtplib email pathlib mysql-connector-python python-dotenv
3. Set up the environment variables by creating a .env file in the same directory as the script. Add the following variables and provide the corresponding values:
image.png
4. Update the PORT and SMTP_SERVER variables in the script if you are using an SMTP server other than Outlook.

# Usage
To run the script, execute the following command:
- python send_email.py
The script will connect to the MySQL database using the provided credentials. It will check for upcoming expiration dates for various licenses and send email notifications to the concerned individuals.

# Customization
The script can be customized according to your specific requirements:

Modify the database schema and table structure to match your database setup.
Add or remove license columns and update the columns list accordingly.
Adjust the notification intervals by modifying the difference in [...] section.
Customize the email subject and message content in the send_email function.

# Script Overview
1. Loads the required Python modules and libraries: os, smtplib, email, pathlib, mysql.connector, dotenv, date, timedelta, datetime.
2. Reads the environment variables from the .env file.
3. Defines the SMTP server details and the port number.
4. Defines a function get_expirationDate to connect to the MySQL database and retrieve expiration dates for different licenses.
5. Defines a function send_email to send email notifications using the provided SMTP server details.
6. Executes the get_expirationDate function and retrieves the expiration date and column name.
7. Sends email notifications for approaching expiration dates.

# Conclusion
The Expiration Date Notifier script provides a simple and automated way to track and notify individuals about upcoming expiration dates for licenses stored in a MySQL database. By utilizing email notifications, it ensures that concerned individuals are promptly informed, allowing them to take necessary actions. Feel free to modify and customize the script to meet your specific needs and integrate it seamlessly into your workflow."# python-smtp-email-bot" 
"# python-smtp-email-bot" 
