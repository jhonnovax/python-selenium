import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIG ===
LOGIN_URL = "https://ais.usvisa-info.com/en-ca/niv/users/sign_in"
EMAIL_USER = "kpmv.ca@gmail.com"         # Your login email for visa site
EMAIL_PASS = "Karen123*"                   # Your password for visa site
CHECK_INTERVAL = 10 * 60                        # Minutes in seconds

# Email notification setup (Gmail example)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "jhonnovax@gmail.com"           # Gmail to send from
SENDER_PASS = "tjql iizd dugq whwd"        # Gmail app password (see note below)
RECEIVER_EMAIL = "jhonnovax@gmail.com" # Where to receive alerts

# === FUNCTIONS ===

def fill_submit_login_info(driver):
	# Fill login info
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_email"))).send_keys(EMAIL_USER)
	driver.find_element(By.ID, "user_password").send_keys(EMAIL_PASS)
	driver.find_element(By.CLASS_NAME, "icheckbox").click()

	# Click sign in button
	driver.find_element(By.NAME, "commit").click()

def login(driver):	
	# Open login page
	driver.get(LOGIN_URL)

	# Fill and submit login info
	fill_submit_login_info(driver)
	
	 # Wait until URL changes after login (max 2 minutes)
	WebDriverWait(driver, 120).until(lambda d: d.current_url != LOGIN_URL)

def send_email(subject, body):
	msg = MIMEText(body)
	msg["Subject"] = subject
	msg["From"] = SENDER_EMAIL
	msg["To"] = RECEIVER_EMAIL

	with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
		server.starttls()
		server.login(SENDER_EMAIL, SENDER_PASS)
		server.send_message(msg)

def check_appointments(driver):
	try:
		# Go to appointment page
		driver.get("https://ais.usvisa-info.com/en-ca/niv/schedule/61655878/appointment")
		
		# Open the calendar
		# Wait for the element to be clickable and then click it
		appointment_date_element = WebDriverWait(driver, 5).until(
			EC.element_to_be_clickable((By.ID, "appointments_consulate_appointment_date"))
		)
		appointment_date_element.click()
		time.sleep(3)
		
		# Wait for calendar to load
		WebDriverWait(driver, 5).until(
			EC.presence_of_element_located((By.CLASS_NAME, "ui-datepicker-calendar"))
		)

		# Check if June is available - example: check calendar header
		# Calendar header has class 'ui-datepicker-title', example text: "June 2025"
		month_header = driver.find_element(By.CLASS_NAME, "ui-datepicker-title").text.lower()
		
		if "june" in month_header or "july" in month_header:
			# Extract available clickable days (dates that can be clicked)
			available_days = driver.find_elements(By.CSS_SELECTOR, "td[data-handler='selectDay']")
			
			if available_days:
				return True, len(available_days)
			
		return False, 0
	
	except Exception as e:
		print(f"System busy...")
		return False, 0

def main():		
	# Loop every 15 minutes to check appointments
	while True:
		try:
			# Start browser
			driver = webdriver.Chrome()

			print("Logging in...")
			login(driver)

			print("Checking for appointments...")
			found, count = check_appointments(driver)
			if found:
				subject = "Visa ✅ Dates available!"
				body = f"There are {count} available appointment dates 😃."
				print(subject)
				send_email(subject, body)
			else:
				print("Visa ❌ No dates available!")

		except Exception as e:
			print(f"Error: {e}")

		finally:
			driver.quit()
			print(f"Waiting {CHECK_INTERVAL//60} minutes before next check...")
			time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
	main()
