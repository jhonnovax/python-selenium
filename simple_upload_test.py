import os
import time
import dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_file_upload():
    """Simple test for file upload functionality on the media manager page."""
    # Load environment variables from .env file
    dotenv.load_dotenv()
    
    # Get credentials from environment variables
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    
    if not username or not password:
        raise Exception("Login credentials not found in .env file")
    
    # URL to test (login page)
    login_url = "https://wccorionqa.on24.com/webcast/login"
    target_url = "https://wccorionqa.on24.com/webcast/mediamanager"
    
    # Set up Chrome options
    options = Options()
    options.add_argument("--window-size=1920,1080")
    
    # Initialize Chrome WebDriver using Selenium's built-in driver manager
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    
    try:
        # Get the absolute path to the image file
        image_path = os.path.abspath("sample_image.jpeg")
        print(f"Using image file: {image_path}")
        
        # Check if the image file exists
        if not os.path.exists(image_path):
            raise Exception(f"Image file not found: {image_path}")
        
        # Step 1: Navigate to the login page
        print(f"Navigating to login page: {login_url}")
        driver.get(login_url)
        
        # Step 2: Enter login credentials
        print("Entering login credentials...")
        
        # Find username field and enter username
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        # Find password field and enter password
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)
        
        # Click login button
        login_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        print("Login credentials submitted")
        
        # Wait for login to complete and redirect
        time.sleep(3)
        
        # Step 3: Navigate to the media manager page
        print(f"Navigating to target page: {target_url}")
        driver.get(target_url)

        # Wait for target page to load
        time.sleep(3)

        # Step 4: Click the button with class btn-add-content
        print("Looking for 'Add Content' button...")
        add_content_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-add-content"))
        )
        add_content_button.click()
        print("Clicked the 'Add Content' button")
        
        # Step 5: Wait for dropdown to appear
        print("Waiting for dropdown menu...")
        dropdown = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".add-content-options"))
        )
        print("Dropdown menu appeared")
        
        # Step 6: Click the option 'Upload Files' in the unordered list
        print("Looking for option in dropdown...")
        option = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-content-options li"))
        )
        # disable the click event on an `<input>` file
        driver.execute_script(
            "HTMLInputElement.prototype.click = function() {                   " +
            "  if(this.type !== 'file') HTMLElement.prototype.click.call(this);" +
            "};                                                                " 
        );
        option.click()
        print("Clicked the 'Upload Files' button")
        
        # Step 7: Wait for the input file element to be created
        print("Waiting for file input element...")
        time.sleep(1)  # Small delay to ensure the input element is created
        
        # Access the file input from DOM
        print("Accessing file input from DOM...")
        input_file = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']#input-upload-files-media-manager"))
        )
        
        # Upload the image file
        print(f"Attaching file to input element: {image_path}")
        # Send the file path to the input element
        input_file.send_keys(image_path)

        
        # Wait for a moment to observe the file upload process
        print("Waiting for uploading process...")
        time.sleep(1)
        
        # Wait for the upload details modal to appear
        print("Waiting for 'Upload Details' modal...")
        upload_modal = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "on24-modal"))
        )
        
        # Verify the modal title is 'Upload Details'
        modal_title = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "on24-modal header span.title"))
        )
        
        if modal_title.text == 'Upload Details':
            print("'Upload Details' modal appeared successfully")
        else:
            raise Exception(f"Expected modal title 'Upload Details', but got '{modal_title.text}'")
            
        print("Test completed successfully")
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        
    finally:
        # Clean up
        print("Closing browser...")
        driver.quit()


if __name__ == "__main__":
    test_file_upload() 