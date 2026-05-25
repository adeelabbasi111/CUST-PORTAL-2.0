# CUST PORTAL REWORKED

A Windows-based student portal scraper and visualizer for the CUST student dashboard.

This project combines a Selenium-driven web scraper, a Flask-powered browser UI, and a packaged Windows executable build process to fetch dashboard data, grade breakdowns, and course summaries from the CUST portal.

## Key Features

- **Automated portal scraping** for student profile, course list, attendance, and gradebook details
- **Dashboard visualizer** built with Flask and rich HTML templates
- **Grade breakdown analysis** by course and assessment category
- **Standalone Windows executable build** using PyInstaller
- **Browser automation** with Microsoft Edge support
- **Persistent student data storage** in JSON format

## What This Project Contains

- `main.py` — GUI entry point and browser startup flow
- `Codes/WebHandler.py` — Flask application wrapper
- `Codes/dashboard_scraper.py` — dashboard data extraction
- `Codes/course_scraper.py` — gradebook and course assessment scraping
- `utils/` — utilities for browser control, login flow, routing, file management, and grade calculations
- `models/` — data model definitions for student, course, grade category, and assessments
- `Build Files/` — build scripts, packaging guides, and quick-start instructions
- `StudentData/` — data storage directory for saved JSON outputs

## Architecture Overview

1. `main.py` launches a Tkinter window for browser selection and user guidance.
2. `BrowserManager` sets up a Selenium session with browser profile and automation options.
3. `LoginHandler` navigates the user through Microsoft login and waits for portal access.
4. `DashboardScraper` extracts personal info, course cards, attendance, and summary fields.
5. `GradeBookScraper` opens course gradebooks and parses grade categories and assessments.
6. Scraped data is saved as JSON and then displayed via Flask templates.

## Prerequisites

- Windows 10 or later
- Python 3.7+
- Microsoft Edge installed
- Internet access to reach the CUST portal

## Dependencies

The project relies on:

- `selenium>=4.34.0`
- `flask>=3.1.1`
- `Werkzeug>=3.1.3`
- `requests>=2.32.4`
- `PyInstaller>=6.14.2`

Install them with:

```bash
pip install -r "Build Files/requirements.txt"
```

## Running the Project Locally

1. Open a terminal in the repository root:

```bash
cd c:\Users\adeel\PycharmProjects\Student-Portal
```

2. Install dependencies if needed:

```bash
pip install -r "Build Files/requirements.txt"
```

3. Run the application:

```bash
python main.py
```

4. Follow the on-screen prompts to select your browser and close existing browser sessions.

## Building a Standalone Executable

This repository includes a complete executable build kit inside `Build Files/`.

### Recommended build method

- Double-click `Build Files/build.bat`

### Command line build

```bash
cd c:\Users\adeel\PycharmProjects\Student-Portal
Build Files\build.bat
```

### Alternative build methods

- `Build Files\build.ps1` — PowerShell script
- `Build Files\build_exe.py` — Python build script

### Build output

After a successful build, the executable is available at:

```bash
dist\StudentPortal\StudentPortal.exe
```

## Usage Flow

- The app launches a GUI warning and browser choice prompt.
- It requires all active Microsoft Edge browser tabs to be closed before scraping.
- Once login is completed, the application opens a local Flask dashboard.
- The dashboard shows saved session files, visualizations, and course grade details.
- Saved JSON files are managed and deleted through the application interface.

## Data Storage

Student data is persisted in a JSON format under a Documents folder managed by the app.

The default storage path is:

```python
~/Documents/Portal Scraper/StudentData
```

## Project Structure

```text
Student-Portal/
├── main.py
├── Build Files/
│   ├── build.bat
│   ├── build.ps1
│   ├── build_exe.py
│   ├── requirements.txt
│   ├── BUILD_GUIDE.md
│   ├── QUICK_START.md
│   └── BUILD_SUMMARY.md
├── Codes/
│   ├── WebHandler.py
│   ├── course_scraper.py
│   ├── dashboard_scraper.py
│   ├── templates/
│   └── static/
├── models/
│   ├── config.py
│   └── student_data.py
├── utils/
│   ├── browser_manager.py
│   ├── login_handler.py
│   ├── web_routes.py
│   ├── file_manager.py
│   ├── grade_calculator.py
│   └── feedback.py
├── StudentData/
└── README.md
```

## Troubleshooting

### Common issues

- **Browser tabs are open**: close all Edge windows before starting the scraper.
- **Executable fails to launch**: run it from Command Prompt to inspect error output.
- **Portal login fails**: verify your Microsoft credentials and that the CUST portal is reachable.

### Helpful checks

- Run `Build Files\verify.bat` to validate build prerequisites.
- Confirm that the browser profile folder exists in `models/config.py`.
- If packaging fails, delete `dist/`, `build/`, and `StudentPortal.spec` before rebuilding.

## Notes

- The app uses Selenium automation with browser profile support and anti-detection options.
- The primary browser path in the current code is Microsoft Edge.
- The scraper is tailored for the CUST portal selectors defined in `models/config.py`.

## License

Add license information here if you want to share the project publicly.

## Contact

Contact me on :
Mail : adeelabbasipersonal@gmail.com
