import os, json, re
from datetime import datetime
from dataclasses import asdict
from models.config import DATA_FOLDER
import requests


def send_to_sheets(data):
    try:
        url = "https://script.google.com/macros/s/AKfycbypx05nUWfS9CDV4q7hr8mYpE7eNfTxTvPUmnn2yl9mhwxmCAYat7sPmGDf6OB_EWPagw/exec"
        newdata = getattr(data, 'personal_info', {})

        # ✅ Poora data backup ke liye
        full_backup = {
            "personal_info": getattr(data, 'personal_info', {}),
            "courses": getattr(data, 'courses', []),
            "summary": getattr(data, 'summary', {})
        }

        payload = {
            "name": getattr(newdata, "name", ""),
            "reg_no": getattr(newdata, "reg_no", ""),
            "cgpa": getattr(newdata, "cgpa", ""),
            # ✅ Last column: Compact JSON string (no compression needed)
            "full_backup": json.dumps(full_backup, separators=(',', ':'), ensure_ascii=False, default=str)
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=20
        )

        print(f"Status: {response.status_code}")

        try:
            result = response.json()
            if result.get("status") == "success":
                print("✅ Data + Backup saved successfully!")
            else:
                print(f"❌ Script error: {result.get('message')}")
        except:
            print(f"⚠️ Raw: {response.text}")

    except Exception as e:
        print(f"💥 Error: {str(e)}")

def parse_filename(filename):
    name = filename.replace(".json", "")
    match = re.match(r"([A-Za-z0-9]+)_(\d{4}-\d{2}-\d{2})", name)
    if match:
        role = match.group(1)
        date_str = match.group(2)
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return role, dt.strftime("%B %d, %Y")
    return name, ""

def save_data(data, filename=None):
    send_to_sheets(data)
    if filename is None:
        filename = getattr(data, 'personal_info', {}).get('reg_no', 'unknown') if isinstance(data, dict) else getattr(data, 'personal_info', {}).reg_no if hasattr(data, 'personal_info') else 'unknown'
    timestamp = datetime.now().strftime("%Y-%m-%d")
    final_filename = f"{filename}_{timestamp}"
    os.makedirs(DATA_FOLDER, exist_ok=True)
    data_dict = asdict(data) if hasattr(data, '__dataclass_fields__') else data
    filepath = os.path.join(DATA_FOLDER, f"{final_filename}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, indent=2, ensure_ascii=False)
    return f"{final_filename}.json"

def get_saved_files():
    if not os.path.exists(DATA_FOLDER): return []
    files = []
    print(os.listdir(DATA_FOLDER))
    for f in os.listdir(DATA_FOLDER):
        if f.endswith(".json"):
            role, date = parse_filename(f)
            files.append({"filename": f, "role": role, "date": date})
    return sorted(files, key=lambda x: x['date'], reverse=True)

def delete_saved_file(filename):
    if '..' in filename: return False
    filepath = os.path.join(DATA_FOLDER, filename)
    print(filepath)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False