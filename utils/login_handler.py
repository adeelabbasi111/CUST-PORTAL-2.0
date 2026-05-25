from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from models.config import PORTAL_URL
import time

class LoginHandler:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 300)

    def perform_login(self):
        try:
            print(f"🌐 Navigating to {PORTAL_URL}...")
            self.driver.get(PORTAL_URL)

            # Store main tab
            main_tab = self.driver.current_window_handle

            # 1. Click Microsoft Login
            print("⏳ Clicking 'Login With Microsoft'...")

            ms_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div/div/div[1]/div[3]/form/div[3]/a")
                )
            )

            ms_btn.click()

            # 2. Wait for Microsoft login page
            self.wait.until(
                lambda d: "login.microsoft" in d.current_url
                or "login.live" in d.current_url
            )

            print("✅ Microsoft login page opened.")

            # 3. Open NEW TAB properly
            print("📂 Opening warning tab...")

            self.driver.switch_to.new_window('tab')

            # Store warning tab handle
            warning_tab = self.driver.current_window_handle

            self.driver.get("http://127.0.0.1:5000/warning")

            # 4. Wait until user clicks OK
            print("⏳ Waiting for OK button...")

            self.wait.until(
                lambda d: "/continue" in d.current_url
            )

            print("✅ OK clicked.")

            # 5. Close warning tab
            self.driver.close()

            # 6. Switch back to main Microsoft login tab
            self.driver.switch_to.window(main_tab)

            print("🔍 Waiting for dashboard...")

            # Wait for successful login
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "user_heading_dash")
                )
            )

            print("🎉 Login Successful!")
            return True

        except Exception as e:
            print(f"❌ Login failed: {e}")

            import traceback
            traceback.print_exc()

            return False