from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from typing import List, Optional
import time

# Importing our data classes
from models.student_data import GradeCategory, Assessment


class GradeBookScraper:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # Thora zyada wait time for .exe stability

    def _safe_get_class(self, element) -> List[str]:
        """Helper: Safe class attribute extraction"""
        class_attr = element.get_attribute("class")
        return class_attr.split() if class_attr else []

    def _safe_click(self, element, timeout=10):
        """Helper: Robust click with scroll and retry"""
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                element
            )
            time.sleep(0.3)  # .exe mein thora buffer time
            element.click()
            return True
        except WebDriverException:
            # Fallback: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except:
                return False

    def parse_grade_table(self) -> List[GradeCategory]:
        category_dict = {}
        categories = []
        assessment_name = None
        next_is_percent = False

        try:
            # Wait for table with longer timeout for .exe
            table = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "uk-table"))
            )

            # Thora wait karo taake saare rows load ho jayen
            time.sleep(1)

            rows = self.driver.find_elements(By.TAG_NAME, "tr")
            print(f"🔍 Found {len(rows)} rows in grade table")

            for idx, row in enumerate(rows):
                # ✅ SAFE: Class attribute check
                classes = self._safe_get_class(row)

                if "md-bg-blue-grey-800" in classes:
                    continue

                cols = row.find_elements(By.TAG_NAME, "td")
                assessment_values = []

                for col_idx, col in enumerate(cols):
                    links = col.find_elements(By.TAG_NAME, "a")

                    if len(links) > 0:
                        try:
                            element = links[0]
                            # Wait for element to be clickable
                            WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable(element)
                            )

                            if self._safe_click(element):
                                time.sleep(0.5)  # Wait for popup/data to load after click
                        except Exception as e:
                            print(f"⚠️ Row {idx}, Col {col_idx}: Click failed: {e}")
                            continue

                        assessment_data = links[0].text.strip().split()
                        if not assessment_data:
                            continue

                        cat_name = assessment_data[0]
                        if cat_name == "Final":
                            continue

                        # ✅ DYNAMIC: Create category if not exists
                        if cat_name not in category_dict:
                            category_dict[cat_name] = {
                                "weightage": "0.0",
                                "obt_percentage": "0.00",
                                "assessments": []
                            }

                        # Safe weightage extraction
                        if len(assessment_data) >= 2:
                            category_dict[cat_name]["weightage"] = str(assessment_data[-2])

                        assessment_name = cat_name
                        next_is_percent = True
                        continue

                    if next_is_percent and assessment_name:
                        # ✅ SAFE: Handle None text
                        col_text = col.text.strip() if col.text else ""
                        if col_text:
                            category_dict[assessment_name]["obt_percentage"] = col_text
                        next_is_percent = False
                        continue

                    # ✅ SAFE: Handle None text for assessment values
                    col_text = col.text.strip() if col.text else ""
                    assessment_values.append(col_text)

                # Create Assessment object if row has complete data
                if len(assessment_values) == 5 and assessment_values[3] not in ["0.00", "", "N/A"]:
                    try:
                        new_assessment = Assessment(
                            name=assessment_values[0],
                            max_mark=assessment_values[1],
                            obtained_mark=assessment_values[2],
                            class_average=assessment_values[3],
                            percentage=assessment_values[4]
                        )
                        if assessment_name and assessment_name in category_dict:
                            category_dict[assessment_name]["assessments"].append(new_assessment)
                    except Exception as e:
                        print(f"⚠️ Failed to create Assessment: {e}")
                        continue

            # Convert dictionary to list of GradeCategory objects
            calc_avg_pct = lambda assessments: (
                f"{sum(float(a.percentage) for a in assessments) / len(assessments):.2f}"
                if assessments else "0.00"
            )

            for cat_name, data in category_dict.items():
                categories.append(GradeCategory(
                    name=cat_name,
                    weightage=str(data["weightage"]),
                    total_obtained=calc_avg_pct(data["assessments"]),
                    assessments=data["assessments"]
                ))

            print(f"✅ Parsed {len(categories)} grade categories")

        except TimeoutException:
            print("❌ Grade table not found or loaded too slowly")
        except Exception as e:
            print(f"❌ Error parsing table: {e}")
            import traceback
            traceback.print_exc()

        return categories

    def ensure_standard_categories(self, categories: List[GradeCategory]) -> List[GradeCategory]:
        """If a standard category is missing, add it with N/A values."""
        standard_names = ["Assignments", "Quiz", "Mid Term", "Final Term"]
        existing_names = [cat.name for cat in categories]

        for std_name in standard_names:
            if not any(std_name in existing for existing in existing_names):
                categories.append(GradeCategory(
                    name=std_name,
                    weightage="N/A",
                    total_obtained="N/A",
                    assessments=[Assessment(name="N/A", max_mark="N/A", obtained_mark="N/A",
                                            class_average="N/A", percentage="N/A")]
                ))
        return categories

    def scrape_full_course_data(self) -> List[GradeCategory]:
        """Main function to get all course data."""
        categories = self.parse_grade_table()
        # categories = self.ensure_standard_categories(categories)
        return categories