import os, json, time, traceback , threading
from flask import render_template, request, jsonify,redirect,url_for
from utils.grade_calculator import calculate_course_stats
from utils.file_manager import get_saved_files, delete_saved_file, save_data
from models.config import GRADE_POINTS, DATA_FOLDER

from Codes.course_scraper import GradeBookScraper  # Adjust path if needed

def register_routes(app, driver):
    @app.route("/")
    def landing():
        return render_template("index.html")

    @app.route('/quit', methods=['POST'])
    def quit_bot():

        def shutdown():

            time.sleep(1)

            try:
                if hasattr(app, 'driver') and app.driver:
                    print("Quitting browser...")
                    app.driver.quit()

            except Exception as e:
                print(e)

            os._exit(0)

        threading.Thread(target=shutdown, daemon=True).start()

        return jsonify({
            "status": "shutting_down"
        }), 200
    @app.route("/dashboard")
    def dashboard():
        filename = request.args.get("file")
        if not filename: return "Error: No file specified", 400
        json_path = os.path.join(DATA_FOLDER, filename)
        if not os.path.exists(json_path): return "File not found", 404

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        processed_courses = []
        base_colors = ["#6366f1", "#8b5cf6", "#a855f7", "#d946ef", "#ec4899"]

        for idx, course in enumerate(data.get('courses', [])):
            stats = calculate_course_stats(course,data['personal_info']['name'])
            cat_labels = [c['name'] for c in stats['category_stats']]
            student_vals = [c['weighted_score'] for c in stats['category_stats']]
            class_vals = [(c['class_marks'] / c['max_marks'] * c['weight']) if c['max_marks'] > 0 else 0 for c in stats['category_stats']]

            processed_courses.append({
                'id': f"course-{idx}", 'course': course, 'stats': stats,
                'chart_data': {
                    'labels': cat_labels, 'student_data': student_vals,
                    'class_data': class_vals, 'colors': base_colors[:len(cat_labels)]
                }
            })

        total_qp = sum(float(item['course']['credit_hours']) * GRADE_POINTS.get(item['stats']['estimated_grade']['grade'], 0.0) for item in processed_courses)
        total_credits = sum(float(item['course']['credit_hours']) for item in processed_courses)
        overall_gpa = round(total_qp / total_credits, 2) if total_credits > 0 else 0.00

        return render_template('visualiser.html', student=data.get('personal_info', {}), summary=data.get('summary', {}), courses=processed_courses, overall_gpa=overall_gpa)

    @app.route("/api/files", methods=["GET"])
    def api_get_files():
        return jsonify(get_saved_files())

    @app.route("/api/delete/<filename>", methods=["POST"])
    def api_delete_file(filename):
        if delete_saved_file(filename):
            return jsonify({"status": "success", "message": "🗑️ File deleted successfully"})
        return jsonify({"error": "Not found"}), 404

    @app.route("/scrape", methods=["POST"])
    def api_scrape_data():
        if not driver: return jsonify({"error": "❌ Browser driver not initialized"}), 500
        try:
            from utils.login_handler import LoginHandler
            from Codes.dashboard_scraper import DashboardScraper
            from Codes.course_scraper import GradeBookScraper

            login_handler = LoginHandler(driver)
            if not login_handler.perform_login():
                return jsonify({"error": "❌ Login failed. Check credentials."}), 400

            print("🔍 Scraping dashboard...")
            dashboard_scraper = DashboardScraper(driver)
            student_data = dashboard_scraper.scrape()

            for course in student_data.courses:
                driver.get(f"https://tasjeel.cust.edu.pk/student/course/gradebook/{course.course_identifier}")
                time.sleep(2)
                grade_scraper = GradeBookScraper(driver)
                course.grade_categories = grade_scraper.scrape_full_course_data()
                print(f"✅ Scraped: {course.course_name}")

            saved_filename = save_data(student_data)
            print("opening",saved_filename)
            driver.get(f"http://127.0.0.1:5000/dashboard?file={saved_filename}")
            return
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"❌ Scraping failed: {str(e)}"}), 500

    @app.route("/warning")
    def warning_page():
        return render_template("warning.html")

    @app.route("/continue")
    def continue_after_warning():
        return "<script>window.close();</script><p>✓ Confirmed! Returning to bot...</p>"