import os
import subprocess
import sys
from selenium import webdriver
from models.config import BROWSER_PROFILES

class BrowserManager:
    def __init__(self, browser_name: str):
        self.browser_name = browser_name.lower()
        self.driver = None

    def find_user_data_dir(self) -> str:
        path = BROWSER_PROFILES.get(self.browser_name)
        if path and os.path.exists(path):
            print(f"✅ Found {self.browser_name.capitalize()} User Data at: {path}")
            return path
        print(f"❌ Could not find {self.browser_name.capitalize()} User Data.")
        sys.exit("Exiting because User Data directory was not found.")

    def kill_processes(self):
        process_name = "msedge.exe" if self.browser_name == 'edge' else "chrome.exe"
        print(f"🧹 Killing existing {process_name} processes...")
        try:
            subprocess.run(["taskkill", "/f", "/im", process_name],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ Background processes cleared.")
        except Exception as e:
            print(f"⚠️ Could not kill processes: {e}")

    def setup_driver(self):
        user_data_dir = self.find_user_data_dir()
        profile_dir = "Default"

        print(f"🚀 Launching {self.browser_name.capitalize()} using MAIN profile: '{profile_dir}'")
        print("⚠️ IMPORTANT: Ensure your main browser is CLOSED before proceeding.")

        if self.browser_name == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("--remote-debugging-port=9222")
        elif self.browser_name == 'edge':
            options = webdriver.EdgeOptions()
            options.add_argument("--remote-debugging-port=9223")
        else:
            raise ValueError("Invalid browser choice.")

        # Common Anti-Detection & Profile Settings
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--profile-directory={profile_dir}")
        options.add_argument("--start-maximized")

        # User Agent
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        if self.browser_name == 'edge':
            ua += " Edg/122.0.0.0"
        options.add_argument(f"user-agent={ua}")

        # ✅ Selenium Manager automatically downloads & caches the correct driver
        if self.browser_name == 'chrome':
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Edge(options=options)

        # Inject Stealth Script
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })

        return self.driver