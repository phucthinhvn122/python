from flask import Flask, render_template, request, jsonify
import requests
import os
import time

base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

GLOBAL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/json",
}
TOKEN_FILE = os.path.join(os.environ.get("TEMP", "/tmp"), "token.txt")
def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()
            if token:
                return token
    return None

def save_token(token):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(token.strip())

def check_token_logic(token):
    if not token:
        return False, None
    h = GLOBAL_HEADERS.copy()
    h["Authorization"] = token
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=h)
        if r.status_code == 200:
            return True, r.json()
        return False, None
    except:
        return False, None

def capsolver_solve(sitekey, rqdata, api_key):
    if not api_key:
        return None
        
    create_task_payload = {
        "clientKey": api_key,
        "task": {
            "type": "HCaptchaEnterpriseTaskProxyLess",
            "websiteURL": "https://discord.com/login",
            "websiteKey": sitekey,
            "enterprisePayload": {
                "rqdata": rqdata
            }
        }
    }
    
    try:
        r = requests.post("https://api.capsolver.com/createTask", json=create_task_payload)
        task_data = r.json()
        
        if task_data.get("errorId") != 0:
            return None
            
        task_id = task_data.get("taskId")
        
        max_retries = 30
        for _ in range(max_retries):
            time.sleep(3)
            res = requests.post("https://api.capsolver.com/getTaskResult", json={
                "clientKey": api_key,
                "taskId": task_id
            })
            res_data = res.json()
            status = res_data.get("status")
            
            if status == "ready":
                return res_data.get("solution", {}).get("gRecaptchaResponse")
            elif status == "failed":
                return None
                
        return None
    except:
        return None

# --- FLASK ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save_token', methods=['POST'])
def api_save_token():
    data = request.json
    token = data.get('token')
    is_valid, _ = check_token_logic(token)
    if is_valid:
        save_token(token)
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Token không hợp lệ hoặc đã chết (Die)"})

@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.json
    # Neu truyen token tu client thi lay, khong thi load tu file text
    token = data.get('token') or load_token()
    
    is_valid, user_data = check_token_logic(token)
    if is_valid:
        return jsonify({"success": True, "user": user_data})
    return jsonify({"success": False, "message": "Token không hợp lệ."})

@app.route('/api/join', methods=['POST'])
def api_join():
    data = request.json
    invite = data.get('invite')
    token = data.get('token') or load_token()
    
    if not token:
        return jsonify({"success": False, "message": "Vui lòng cung cấp Token hoặc lưu Token trước."})
        
    is_valid, _ = check_token_logic(token)
    if not is_valid:
        return jsonify({"success": False, "message": "Token bạn cung cấp (hoặc token đang lưu) đã Die hoặc không đúng."})

    invite_code = invite.split("/")[-1].split("?")[0].strip()
    
    h = GLOBAL_HEADERS.copy()
    h["Authorization"] = token
    
    try:
        r = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=h, json={})
        
        if r.status_code in [200, 201]:
            guild_data = r.json().get("guild", {})
            return jsonify({"success": True, "guild_name": guild_data.get('name')})
        elif r.status_code == 404:
            return jsonify({"success": False, "message": "Invite Code không tồn tại hoặc đã hết hạn!"})
        elif "captcha-required" in r.text:
            return jsonify({"success": False, "message": "Server bật chống bot, yêu cầu phải giải Captcha để Join Server."})
        return jsonify({"success": False, "message": f"Lỗi không xác định: {r.text}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route('/api/login_email', methods=['POST'])
def api_login_email():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    capsolver_key = data.get('capsolver_key')
    
    # 2FA verify flow
    mfa_code = data.get('mfa_code')
    ticket = data.get('ticket')
    
    if mfa_code and ticket:
        r_mfa = requests.post("https://discord.com/api/v9/auth/mfa/totp", 
                              json={"code": mfa_code, "ticket": ticket}, 
                              headers=GLOBAL_HEADERS)
        if r_mfa.status_code == 200:
            token = r_mfa.json().get("token")
            save_token(token)
            return jsonify({"success": True, "token": token})
        return jsonify({"success": False, "message": "Sai mã OTP hoặc Ticket đã hết hạn."})

    # Normal Login Flow
    payload = {"login": email, "password": password}
    
    # Neu payload co san captcha_key tuc la da thuc hien verify bot thanh cong -> thuc hien de quy
    def do_login(payload_data):
        r = requests.post("https://discord.com/api/v9/auth/login", json=payload_data, headers=GLOBAL_HEADERS)
        res = r.json()
        
        if r.status_code == 200:
            token = res.get("token")
            save_token(token)
            return jsonify({"success": True, "token": token})
            
        elif "ticket" in r.text and "mfa" in r.text:
            return jsonify({"success": False, "require_mfa": True, "ticket": res.get("ticket")})
            
        elif "captcha_key" in r.text:
            # Discord bat captcha
            sitekey = res.get("captcha_sitekey")
            rqdata = res.get("captcha_rqtoken") or res.get("captcha_rqdata")
            
            if payload_data.get("captcha_key"):
                # Captcha vua giai xong van bi Discord tu choi
                return jsonify({"success": False, "message": "Captcha đã giải bị Discord từ chối."})
                
            if capsolver_key:
                # Automate it
                solved_token = capsolver_solve(sitekey, rqdata, capsolver_key)
                if solved_token:
                    payload_data["captcha_key"] = solved_token
                    return do_login(payload_data) # recursive try again
                else:
                    return jsonify({"success": False, "message": "Sử dụng CapSolver giải Captcha thất bại."})
            else:
                return jsonify({"success": False, "message": "Discord bắt Capctcha. Bạn cần sử dụng CapSolver API Key để tự động Bypass."})
        else:
            return jsonify({"success": False, "message": r.text})

    return do_login(payload)

if __name__ == '__main__':
    app.run(port=8000)
