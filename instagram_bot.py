"""
Instagram Signup Bot - EDUCATIONAL PURPOSES ONLY
WARNING: Automating Instagram account creation violates Instagram's Terms of Service.
This code is for learning web automation concepts only.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchWindowException
import time
import random
import datetime
import os
import json
import re
import pathlib


class InstagramSignupBot:
    def __init__(self):
        """Initialize the bot with Chrome options"""
        self.chrome_options = Options()
        # Uncomment the line below to run in headless mode (no browser window)
        # self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = None
    
    def start_driver(self):
        """Start the Chrome driver"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.maximize_window()
            print("✓ Chrome driver started successfully")
        except Exception as e:
            print(f"✗ Error starting Chrome driver: {e}")
            print("Make sure you have Chrome and ChromeDriver installed")
            raise
    
    def open_instagram_signup(self):
        """Navigate to Instagram signup page"""
        try:
            self.driver.get("https://www.instagram.com/accounts/emailsignup/")
            print("✓ Navigated to Instagram signup page")
            time.sleep(3)  # Wait for page to load
        except Exception as e:
            print(f"✗ Error opening Instagram: {e}")
            raise
    
    def fill_signup_form(self, email, full_name, username, password):
        """
        Fill in the signup form with provided information
        
        Args:
            email (str): Email address
            full_name (str): Full name
            username (str): Desired username
            password (str): Password (min 6 characters)
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Wait for and fill email field
            print("Filling email field...")
            email_field = wait.until(
                EC.presence_of_element_located((By.NAME, "emailOrPhone"))
            )
            email_field.clear()
            email_field.send_keys(email)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Fill full name field
            print("Filling full name field...")
            fullname_field = self.driver.find_element(By.NAME, "fullName")
            fullname_field.clear()
            fullname_field.send_keys(full_name)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Fill username field
            print("Filling username field...")
            username_field = self.driver.find_element(By.NAME, "username")
            username_field.clear()
            username_field.send_keys(username)
            time.sleep(random.uniform(0.5, 1.5))
            
            # Fill password field
            print("Filling password field...")
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            time.sleep(random.uniform(0.5, 1.5))
            
            print("✓ All fields filled successfully")
            
        except Exception as e:
            print(f"✗ Error filling form: {e}")
            raise
    
    def click_signup_button(self):
        """Click the signup button"""
        try:
            wait = WebDriverWait(self.driver, 12)

            # Helper: wait for potential overlays to disappear
            overlay_selectors = [
                (By.XPATH, "//div[contains(@class,'xdj266r') and contains(@class,'x1ga7v0g') and contains(@class,'x1c1uobl')]")
                ,(By.CSS_SELECTOR, "div[role='presentation'] div[style*='--x-width']")
            ]

            def wait_overlays():
                for how, value in overlay_selectors:
                    try:
                        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((how, value)))
                    except Exception:
                        pass

            # Try multiple strategies to find the Sign Up button
            button_candidates = [
                (By.XPATH, "//button[contains(text(), 'Sign up') or contains(text(), 'Sign Up')]") ,
                (By.XPATH, "//button[contains(@class, '_aswp') or contains(@class, '_acan') or contains(@class, '_acap')][@type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]

            signup_button = None
            for how, selector in button_candidates:
                try:
                    signup_button = wait.until(EC.element_to_be_clickable((how, selector)))
                    break
                except Exception:
                    continue

            if not signup_button:
                raise Exception("Sign Up button not found")

            # Scroll into view and click with JS fallback to avoid interception
            wait_overlays()
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", signup_button)
            time.sleep(0.6)

            # Wait until the button is enabled (not disabled)
            wait.until(lambda d: signup_button.is_enabled() and signup_button.get_attribute("disabled") is None)
            time.sleep(0.3)

            try:
                signup_button.click()
            except Exception:
                # Fallback to JS click if intercepted
                self.driver.execute_script("arguments[0].click();", signup_button)

            time.sleep(3)
            print("✓ Sign up button clicked")

        except Exception as e:
            print(f"✗ Error clicking signup button: {e}")
            # Take a screenshot for debugging
            try:
                self.driver.save_screenshot("signup_error.png")
                print("Screenshot saved as signup_error.png")
            except:
                pass
            raise
    
    def handle_birthday_selection(self, birth_date: datetime.date):
        """Fill birthday dialog if it appears, then click Next."""
        try:
            wait = WebDriverWait(self.driver, 12)

            # Wait for dropdowns
            month_el = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[aria-label='Month'], select[title*='Month']"))
            )
            day_el = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[aria-label='Day'], select[title*='Day']"))
            )
            year_el = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[aria-label='Year'], select[title*='Year']"))
            )

            Select(month_el).select_by_visible_text(birth_date.strftime("%B"))
            Select(day_el).select_by_visible_text(str(birth_date.day))
            Select(year_el).select_by_visible_text(str(birth_date.year))

            # Click Next button in DOB modal
            next_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))
            )
            next_btn.click()
            print("✓ Birthday information filled and Next clicked")

        except Exception as e:
            print(f"Note: Birthday selection not required or error: {e}")
    
    def close(self):
        """Close the browser"""
        if self.driver:
            print("Closing browser...")
            time.sleep(5)  # Wait a bit before closing
            self.driver.quit()
            print("✓ Browser closed")


def load_config(path: str = "config.json") -> dict:
    """Load Gmail credentials from config.json"""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing {path}. Create it from config.example.json with your Gmail and app password."
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_accounts(path: str = "accounts.txt") -> list[dict]:
    """Load accounts from accounts.txt (email,password,full_name,username). Lines starting with # are ignored."""
    accounts = []
    if not os.path.exists(path):
        return accounts
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 4:
                continue
            accounts.append({
                "email": parts[0],
                "password": parts[1],
                "full_name": parts[2],
                "username": parts[3]
            })
    return accounts


def fetch_latest_code_via_gmail_tab(driver, gmail_user: str, gmail_password: str, timeout_sec: int = 180) -> str:
    """Login to Gmail in a new tab (basic HTML view), open the latest Instagram email, and return a 6-digit code."""
    code_regex = re.compile(r"\b(\d{6})\b")
    parent = driver.current_window_handle
    wait = WebDriverWait(driver, 20)

    def switch_to_new_tab(url: str):
        driver.execute_script("window.open('about:blank','_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)

    def maybe_login_gmail():
        try:
            email_input = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
            email_input.clear()
            email_input.send_keys(gmail_user)
            driver.find_element(By.ID, "identifierNext").click()
            pw_input = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            pw_input.clear()
            pw_input.send_keys(gmail_password)
            driver.find_element(By.ID, "passwordNext").click()
            time.sleep(5)
            print("✓ Logged into Gmail")
        except Exception as e:
            # Already logged in or different flow
            print(f"Login flow skipped or already logged in: {e}")
            pass

    def find_code_on_message_page() -> str:
        body_text = driver.find_element(By.TAG_NAME, "body").text
        m = code_regex.search(body_text)
        return m.group(1) if m else None

    search_url = "https://mail.google.com/mail/u/0/h/?v=lvr&search=search&qs=true&q=from%3Ano-reply@mail.instagram.com"
    login_url = "https://accounts.google.com/ServiceLogin?service=mail&continue=https://mail.google.com/mail/u/0/h/"

    switch_to_new_tab(login_url)
    try:
        maybe_login_gmail()
        
        # Force navigate to Gmail inbox (bypasses workspace landing page)
        print("Navigating to Gmail inbox...")
        
        # Use direct Gmail URL that doesn't redirect to workspace
        gmail_inbox_url = f"https://mail.google.com/mail/u/0/"
        driver.get(gmail_inbox_url)
        time.sleep(5)

        # Dismiss Chrome profile modal if present
        try:
            modal_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Use Chrome without an account')]/ancestor::button | //span[contains(text(),'Continue as')]/ancestor::button"))
            )
            modal_btn.click()
            time.sleep(1)
        except Exception:
            try:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            except Exception:
                pass
        
        # Check if still on workspace page, then force navigate
        if "workspace.google.com" in driver.current_url:
            print("Detected workspace redirect, forcing Gmail access...")
            # Try alternate Gmail URLs
            alternate_urls = [
                "https://mail.google.com/mail/",
                "https://mail.google.com/",
                f"https://accounts.google.com/AccountChooser?continue=https://mail.google.com/mail/"
            ]
            for url in alternate_urls:
                driver.get(url)
                time.sleep(3)
                if "mail.google.com" in driver.current_url and "workspace" not in driver.current_url:
                    print(f"Successfully accessed Gmail via {url}")
                    break

        # If we're on accounts.google.com sign-in, run login again then go to inbox
        if "accounts.google.com" in driver.current_url:
            print("Detected Google sign-in page, retrying login...")
            maybe_login_gmail()
            driver.get(gmail_inbox_url)
            time.sleep(5)
        
        print(f"Current URL: {driver.current_url}")
        
        end_time = time.time() + timeout_sec
        code = None
        attempt = 0
        while time.time() < end_time and not code:
            attempt += 1
            print(f"Attempt {attempt}: Searching for Instagram code...")

            try:
                # Navigate directly to Gmail search results for reliability
                search_url_direct = "https://mail.google.com/mail/u/0/#search/is+your+Instagram+code"
                driver.get(search_url_direct)
                # Wait for result rows
                rows = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.zA"))
                )
                found = False
                for row in rows[:12]:
                    try:
                        row_text = row.get_attribute("innerText") or row.text
                        match = code_regex.search(row_text)
                        if match:
                            code = match.group(1)
                            print(f"Extracted code from search row: {code}")
                            found = True
                            break
                        # Open the row and parse email body
                        row.click()
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.a3s"))
                        )
                        body_text = driver.find_element(By.CSS_SELECTOR, "div.a3s").text
                        match_body = code_regex.search(body_text)
                        if match_body:
                            code = match_body.group(1)
                            print(f"Extracted code from email body: {code}")
                            found = True
                            break
                    except StaleElementReferenceException:
                        # Re-fetch rows and continue
                        rows = driver.find_elements(By.CSS_SELECTOR, "tr.zA")
                        continue
                    finally:
                        # Go back to search results if opened
                        try:
                            driver.get(search_url_direct)
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.zA"))
                            )
                        except Exception:
                            pass
                if found and code:
                    break
                print("No Instagram code found yet, retrying in 5 seconds...")
                time.sleep(5)
            except (StaleElementReferenceException, NoSuchWindowException) as e:
                print(f"Window or element stale, re-opening Gmail tab: {e}")
                # Reopen Gmail tab and continue
                try:
                    driver.switch_to.window(parent)
                except Exception:
                    pass
                switch_to_new_tab(login_url)
                maybe_login_gmail()
                driver.get(gmail_inbox_url)
                time.sleep(3)
                continue
            except Exception as e:
                print(f"Error searching for code: {e}")
                time.sleep(5)
                continue

        if not code:
            raise TimeoutError("Timed out waiting for Gmail code via browser.")
        return code
    finally:
        # Close tab and return
        try:
            driver.close()
            driver.switch_to.window(parent)
        except Exception:
            pass


def submit_email_code(driver, code: str):
    """Enter the email verification code and submit."""
    wait = WebDriverWait(driver, 20)
    # Locate code field
    code_input = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//input[@name='email_confirmation_code' or @name='confirmationCode' or contains(@placeholder,'code') or contains(@aria-label,'code') or contains(@name,'code')]"
        ))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", code_input)
    time.sleep(0.3)
    code_input.clear()
    code_input.send_keys(code)

    # Click the confirmation/next button with fallbacks
    button_candidates = [
        "//button[contains(., 'Next') or contains(., 'Submit') or contains(., 'Confirm')]",
        "//div[@role='button' and (contains(., 'Next') or contains(., 'Confirm'))]"
    ]
    confirm_btn = None
    for xpath in button_candidates:
        try:
            confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            break
        except Exception:
            continue

    if not confirm_btn:
        raise Exception("Confirmation button not found")

    try:
        confirm_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", confirm_btn)

    print("✓ Verification code submitted")


def signup_one_account(user_data: dict, gmail_user: str, gmail_password: str) -> bool:
    """Signup a single Instagram account with provided user_data.
    Returns True on success, False otherwise."""
    bot = InstagramSignupBot()
    try:
        bot.start_driver()
        bot.open_instagram_signup()
        bot.fill_signup_form(
            email=user_data['email'],
            full_name=user_data['full_name'],
            username=user_data['username'],
            password=user_data['password']
        )
        bot.click_signup_button()

        # Optional DOB step
        try:
            today = datetime.date.today()
            max_age, min_age = 35, 19
            latest = today.replace(year=today.year - min_age)
            earliest = today.replace(year=today.year - max_age)
            delta_days = (latest - earliest).days
            random_days = random.randint(0, delta_days)
            birth_date = earliest + datetime.timedelta(days=random_days)
            bot.handle_birthday_selection(birth_date)
        except Exception:
            pass

        # Fetch and submit code
        print("Waiting for email verification code via Gmail tab...")
        code = fetch_latest_code_via_gmail_tab(bot.driver, gmail_user, gmail_password)
        print(f"✓ Code received: {code}")
        submit_email_code(bot.driver, code)
        return True
    except Exception as e:
        print(f"Signup failed for {user_data.get('email')}: {e}")
        return False
    finally:
        bot.close()


def append_account_result(path: str, user_data: dict, status: str):
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(f"{user_data['email']},{user_data['username']},{status}\n")
    except Exception as e:
        print(f"Could not write result to {path}: {e}")


def main():
    """Main function to run the bot"""
    print("\n" + "="*60)
    print("Instagram Signup Bot - EDUCATIONAL PURPOSES ONLY")
    print("WARNING: This violates Instagram's Terms of Service")
    print("="*60 + "\n")

    # Load config
    try:
        config = load_config()
        gmail_user = config.get("gmail_user")
        gmail_password = config.get("gmail_password") or config.get("gmail_app_password")
        if not gmail_user or not gmail_password:
            print("✗ Missing gmail_user or gmail_password in config.json")
            return
    except Exception as e:
        print(f"✗ Config error: {e}")
        return

    def get_or_prompt(key: str, prompt_text: str):
        val = config.get(key)
        if val:
            return val
        return input(prompt_text).strip()

    # Prefer accounts.txt if present
    accounts = load_accounts()
    if accounts:
        acct = accounts[0]
        email_addr = acct["email"]
        full_name = acct["full_name"]
        username = acct["username"]
        password = acct["password"]
        print(f"Using account from accounts.txt: {email_addr} / {username}")
    else:
        email_addr = get_or_prompt("signup_email", "Enter your email (Gmail recommended): ")
        full_name = get_or_prompt("signup_full_name", "Enter your full name: ")
        username = get_or_prompt("signup_username", "Enter desired username: ")
        password = get_or_prompt("signup_password", "Enter password (min 6 characters): ")

    # Validate inputs
    if not all([email_addr, full_name, username, password]):
        print("\n✗ Error: All fields are required!")
        return

    if len(password) < 6:
        print("\n✗ Error: Password must be at least 6 characters!")
        return

    user_data = {
        'email': email_addr,
        'full_name': full_name,
        'username': username,
        'password': password
    }

    print(f"\nAccount details:")
    print(f"Email: {user_data['email']}")
    print(f"Full Name: {user_data['full_name']}")
    print(f"Username: {user_data['username']}")
    print(f"Password: {'*' * len(user_data['password'])}\n")
    
    if not config.get("auto_confirm", False):
        confirm = input("Continue with account creation? (yes/no): ").strip().lower()
        if confirm not in ['yes', 'y']:
            print("Account creation cancelled.")
            return
    
    # Bulk-create mode: iterate accounts.txt if bulk_create=true
    if config.get("bulk_create", False):
        results_path = "accounts_created.txt"
        accounts = load_accounts()
        if not accounts:
            print("No accounts found in accounts.txt for bulk create.")
            return
        print(f"Bulk creating {len(accounts)} accounts...")
        for i, acct in enumerate(accounts, start=1):
            print("\n" + "-"*60)
            print(f"[{i}/{len(accounts)}] Creating: {acct['email']} / {acct['username']}")
            success = signup_one_account(acct, gmail_user, gmail_password)
            append_account_result(results_path, acct, "success" if success else "failed")
            # Small delay to avoid rate limits
            time.sleep(5)
        print("Bulk create finished. See accounts_created.txt for results.")
        return

    # Single account flow
    success = signup_one_account(user_data, gmail_user, gmail_password)
    append_account_result("accounts_created.txt", user_data, "success" if success else "failed")
    print("\n" + "="*60)
    print("Bot execution completed!")
    print("Note: Instagram may require additional verification")
    print("(email confirmation, phone number, CAPTCHA, etc.)")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
