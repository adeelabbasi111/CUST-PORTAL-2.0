import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.student_data import StudentData, PersonalInfo, Course, Summary
from models.config import DASHBOARD_SELECTORS

class DashboardScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def scrape(self) -> StudentData:
        print("⏳ Waiting for dashboard to load...")
        time.sleep(2)  # Buffer for dynamic content

        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, DASHBOARD_SELECTORS['user_heading_wait'])))

            # Scrape Personal Info
            name = self.driver.find_element(By.XPATH, DASHBOARD_SELECTORS['name_xpath']).text
            reg_no = self.driver.find_element(By.XPATH, DASHBOARD_SELECTORS['reg_no_xpath']).text
            cgpa = self.driver.find_element(By.XPATH, DASHBOARD_SELECTORS['cgpa_xpath']).text

            p_info = PersonalInfo(name=name, reg_no=reg_no, cgpa=cgpa)

            # Scrape Courses
            courses_list = []
            course_cards = self.driver.find_elements(By.XPATH, DASHBOARD_SELECTORS['course_card_xpath'])

            for card in course_cards:
                # 🚨 CHECK FOR WITHDRAWN COURSES FIRST
                header_el = card.find_element(By.CSS_SELECTOR, ".card-header")
                header_text = header_el.text.strip()

                # Agar (Withdraw) ya (Withdrawn) mila to skip kar do
                if "(Withdraw)" in header_text or "(Withdrawn)" in header_text:
                    course_name_preview = header_text.split("(Withdraw")[0].strip()
                    print(f"⏭️ Skipping withdrawn course: {course_name_preview}")
                    continue

                parent_link = card.find_element(By.XPATH, "..")
                href = parent_link.get_attribute("href")
                course_id = href.split("/")[-1] if href else "N/A"

                c_name = card.find_element(By.CSS_SELECTOR, ".card-header span").text.strip()
                teacher = card.find_element(By.CSS_SELECTOR, ".card-title").text.strip()

                # Code
                try:
                    code_el = card.find_element(By.CSS_SELECTOR, ".sub-heading.md-color-blue-grey-600")
                    c_code = code_el.text.strip()
                except:
                    c_code = "N/A"

                # Credits
                card_text = card.find_element(By.CSS_SELECTOR, ".card-text").text
                c_credits = "N/A"
                if "Credits :" in card_text:
                    c_credits = card_text.split("Credits : ")[1].split()[0].strip()

                # Attendance
                att_el = card.find_element(By.XPATH, "div[2]/div[2]/span[1]")
                attendance = att_el.text

                courses_list.append(Course(
                    course_identifier=course_id,
                    course_name=c_name,
                    teacher=teacher,
                    course_code=c_code,
                    credit_hours=c_credits,
                    attendance=attendance
                ))

            # Scrape Summary
            summary = Summary()
            credit_divs = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'user_heading_content')]/div")
            for div in credit_divs:
                text = div.text
                if "Earned Cr " in text:
                    summary.earned_credits = text.split(": ")[-1].strip()
                elif "Total Cr " in text:
                    summary.total_credits = text.split(": ")[-1].strip()
                elif "Inprogress Cr " in text:
                    summary.inprogress_credits = text.split(": ")[-1].strip()

            # 💡 SMART FIX: Recalculate Total Credits from ONLY valid courses
            # (Portal sometimes includes withdrawn courses in Total Cr, ye usko fix karega)
            try:
                valid_credits = sum(
                    float(c.credit_hours) for c in courses_list
                    if c.credit_hours not in ["N/A", "", "0.0"]
                )
                summary.total_credits = str(round(valid_credits, 1))
                print(f"📊 Recalculated Total Credits (excl. withdrawn): {summary.total_credits}")
            except Exception as e:
                print(f"⚠️ Could not auto-calculate credits: {e}")

            return StudentData(personal_info=p_info, courses=courses_list, summary=summary)

        except Exception as e:
            print(f"❌ Error scraping dashboard: {str(e)}")
            raise e