import os , sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Portal Configuration
PORTAL_URL = "https://tasjeel.cust.edu.pk/"

GRADE_POINTS = {
    "A": 4.00, "A-": 3.67, "B+": 3.33, "B": 3.00, "B-": 2.67,
    "C+": 2.33, "C": 2.00, "C-": 1.67, "D+": 1.33, "D": 1.00, "F": 0.00
}
DATA_FOLDER = "StudentData"

# Paths
USERNAME = os.getlogin()
EDGE_DRIVER_PATH = get_resource_path(os.path.join( "drivers","msedgedriver.exe"))


# Browser Profiles
BROWSER_PROFILES = {
    'chrome': rf"C:\Users\{USERNAME}\AppData\Local\Google\Chrome\User Data",
    'edge': rf"C:\Users\{USERNAME}\AppData\Local\Microsoft\Edge\User Data"
}

# Selectors (Login Flow)
LOGIN_SELECTORS = {
    'ms_button_xpath': "/html/body/div/div/div[1]/div[3]/form/div[3]/a",
    'account_tile_xpath': "//div[@role='button'][contains(@class, 'table')]"
}

# Selectors (Dashboard Scraping)
DASHBOARD_SELECTORS = {
    'name_xpath': "/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div/div[2]/h2/span[1]",
    'reg_no_xpath': "/html/body/div[1]/div[2]/div/div/div[1]/div[2]/div/div[2]/h2/span[2]",
    'cgpa_xpath': "/html/body/div[1]/div[2]/div/div/div[1]/div[3]/div/span",
    'course_card_xpath': "//a[contains(@href, '/student/course/info/')]/div[contains(@class, 'card')]",
    'user_heading_wait': "user_heading_dash"
}