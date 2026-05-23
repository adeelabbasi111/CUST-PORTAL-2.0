import time
import threading

from utils.browser_manager import BrowserManager
from Codes.WebHandler import WebHandler

warning = r"""

██╗    ██╗ █████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗
██║    ██║██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝
██║ █╗ ██║███████║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗
██║███╗██║██╔══██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║
╚███╔███╔╝██║  ██║██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝
╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝

Agar Microsoft Edge open ha to sab tabs Close kar ka Enter Press Kar do !!!
"""

def main():
    print(warning)
    input("✅ Press Enter to start...")

    # 3. Setup Browser & Attach Driver
    browser_mgr = BrowserManager("edge")
    browser_mgr.kill_processes()
    driver = browser_mgr.setup_driver()

    # 1. Initialize Flask Handler
    handler = WebHandler(data_folder="StudentData", driver=driver)


    # 2. Run Flask in Background Thread
    def run_flask():
        handler.run(debug=True, host="127.0.0.1", port=5000)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("⏳ Starting Flask server...")
    time.sleep(2)
    print("✅ Flask running at http://127.0.0.1:5000")




    # 4. Open Flask App in Same Browser
    driver.get("http://127.0.0.1:5000")
    print("🌐 Browser opened. Use UI to click 'Scrape'.")

    # 5. Keep Alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
    finally:
        if 'driver' in locals():
            driver.quit()
            print("🔒 Browser closed.")

if __name__ == "__main__":
    main()