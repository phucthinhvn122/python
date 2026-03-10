import requests
import json
import os
import time

GLOBAL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "application/json",
}

TOKEN_FILE = "token.txt"

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
    print(f"[+] Đã lưu cấu hình Token vào file {TOKEN_FILE}")

def check_token(token, verbose=True):
    if not token:
        if verbose:
            print("[-] Token không hợp lệ hoặc trống.")
        return False
        
    h = GLOBAL_HEADERS.copy()
    h["Authorization"] = token
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=h)
        if r.status_code == 200:
            u = r.json()
            if verbose:
                print(f"[+] Token đang sử dụng: {token[:10]}...{token[-5:]}")
                print(f"[+] USER: {u.get('username')} (ID: {u.get('id')})")
                print(f"[+] EMAIL: {u.get('email')} | SĐT: {u.get('phone')}")
            return True
        else:
            if verbose:
                print(f"[-] Token không hợp lệ hoặc tài khoản đã đăng nhập bị Die (Mã lỗi: {r.status_code})")
            return False
    except Exception as e:
        if verbose:
            print(f"[-] Lỗi kết nối khi kiểm tra token: {e}")
        return False

def capsolver_solve(sitekey, rqdata):
    api_key = input("\n[?] Nhập API Key CapSolver của bạn (Enter để bỏ qua giải Captcha thủ công): ").strip()
    if not api_key:
        print("[-] Đã bỏ qua tự động giải Captcha.")
        return None
        
    print(f"[*] Đang gửi yêu cầu giải hCaptcha lên CapSolver...")
    
    # Payload cho Discord hCaptcha
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
            print(f"[-] Lỗi tạo Task CapSolver: {task_data.get('errorDescription')}")
            return None
            
        task_id = task_data.get("taskId")
        print(f"[*] Đã tạo Task ({task_id}), đợi 10-30s để hệ thống AI giải mã...")
        
        # Vòng lặp lấy kết quả
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
                token = res_data.get("solution", {}).get("gRecaptchaResponse")
                print("[+] Đã giải Captcha thành công!")
                return token
            elif status == "failed":
                print(f"[-] AI giải thất bại: {res_data.get('errorDescription')}")
                return None
                
            print(" [.] Đang chờ kết quả Captcha...")
            
        print("[-] Hết thời gian chờ Captcha (Timeout).")
        return None
        
    except Exception as e:
        print(f"[-] Lỗi API CapSolver: {e}")
        return None

def mfa_verify(ticket, captcha_key=None):
    otp = input("[!] Tài khoản có bật 2FA. Nhập mã OTP/Auth: ")
    payload_mfa = {"code": otp, "ticket": ticket}
    if captcha_key:
        payload_mfa["captcha_key"] = captcha_key
        
    r_mfa = requests.post("https://discord.com/api/v9/auth/mfa/totp", json=payload_mfa, headers=GLOBAL_HEADERS)
    
    if r_mfa.status_code == 200:
        token = r_mfa.json().get("token")
        if check_token(token):
            save_token(token)
            return token
    else:
        print(f"[-] Sai OTP hoặc OTP hết hạn: {r_mfa.text}")
    return None

def do_discord_login(email, pw, captcha_key=None):
    payload = {"login": email, "password": pw}
    if captcha_key:
        payload["captcha_key"] = captcha_key
        
    print("[*] Đang gửi yêu cầu đăng nhập lên API Discord...")
    r = requests.post("https://discord.com/api/v9/auth/login", json=payload, headers=GLOBAL_HEADERS)
    response_data = r.json()
    
    # 1. Login thành công không cần 2FA
    if r.status_code == 200:
        token = response_data.get("token")
        if check_token(token):
            save_token(token)
            return token, None
            
    # 2. Bị yêu cầu MFA (2FA)        
    elif "ticket" in r.text and "mfa" in r.text:
        ticket = response_data.get("ticket")
        token = mfa_verify(ticket)
        if token:
            return token, None
            
    # 3. Bị yêu cầu Captcha
    elif "captcha-required" in r.text or "captcha_key" in r.text:
        sitekey = response_data.get("captcha_sitekey")
        rqdata = response_data.get("captcha_rqtoken") or response_data.get("captcha_rqdata")
        
        print("\n[-] LỖI CAPTCHA TỪ DISCORD!")
        print(f"==> Discord yêu cầu Captcha Sitekey: {sitekey}")
        
        # Nếu đã thử giải nhưng vẫn lỗi
        if captcha_key:
            print("[-] Captcha vừa giải không hợp lệ hoặc bị Discord từ chối.")
            return None, None
            
        print("==> Khởi chạy chức năng Auto-Solver qua CapSolver (hoặc 2Captcha)...")
        solved_g_captcha = capsolver_solve(sitekey, rqdata)
        
        if solved_g_captcha:
            print("[*] Thử đăng nhập lại với Captcha token vừa giải...")
            return do_discord_login(email, pw, captcha_key=solved_g_captcha)
            
        else:
            print("[-] Không có Bot giải Captcha. Hủy thao tác đăng nhập.\n")
            return None, None
            
    # 4. Các lỗi khác (sai mật khẩu, sai mail)
    else:
        print(f"[-] Đăng nhập thất bại: {r.text}")
        
    return None, None

def login_email_pass():
    email = input(">> Nhập Email: ")
    pw = input(">> Nhập Password: ")
    try:
        token, _ = do_discord_login(email, pw)
        return token
    except Exception as e:
        print(f"[-] Lỗi kết nối gửi thông tin: {e}")
    return None

def join_server(token):
    if not token:
        print("[-] Vui lòng đăng nhập trước!")
        return

    invite_link = input(">> Nhập Invite Code (hoặc link đầy đủ discord.gg/abc): ")
    invite_code = invite_link.split("/")[-1].split("?")[0].strip()
    
    h = GLOBAL_HEADERS.copy()
    h["Authorization"] = token
    payload = {} 
    
    print(f"[*] Đang yêu cầu join server với mã '{invite_code}'...")
    try:
        r = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=h, json=payload)
        
        if r.status_code in [200, 201]:
            guild_data = r.json().get("guild", {})
            print(f"[+] THAM GIA THÀNH CÔNG: Server \"{guild_data.get('name')}\" (ID: {guild_data.get('id')})")
            
        elif r.status_code == 404:
            print("[-] LỖI: Invite Code không tồn tại hoặc đã hết hạn!")
            
        elif "captcha-required" in r.text:
            print("[-] LỖI CAPTCHA: Server bật chế độ bảo vệ chống bot (Cần giải Captcha bằng giao diện Web)")
            
        elif r.status_code == 401:
            print("[-] LỖI: Token không có quyền hợp lệ.")
            
        else:
            print(f"[-] Tham gia thất bại (Lỗi {r.status_code}): {r.text}")
            
    except Exception as e:
        print(f"[-] Lỗi kết nối khi tham gia server: {e}")

def main():
    current_token = load_token()
    if current_token:
        print("[*] Đã tìm thấy Token lưu trước đó, đang kiểm tra...")
        if not check_token(current_token, verbose=False):
            print("[-] Lưu ý: Token lưu trước đó đã hết hạn/Die. Vui lòng đăng nhập lại.")
            current_token = None
            
    while True:
        print("\n" + "="*40)
        print("    ★ DISCORD TOOL PRO V3 ★    ")
        print("    [ Tích hợp CapSolver AI ]  ")
        print("="*40)
        
        if current_token:
            print(f"[✓] TRẠNG THÁI: Đã Đăng Nhập ({current_token[:10]}...{current_token[-5:]})")
        else:
            print("[X] TRẠNG THÁI: Chưa Đăng Nhập")
            
        print("\n-- MENU CHỨC NĂNG --")
        print(" 1. Auto Login [Email / Pass] (Tự giải Captcha)")
        print(" 2. Login trực tiếp bằng [Token] (Nhanh nhất)")
        print(" 3. Xem thông tin Tài khoản (Check live token)")
        print(" 4. Join Server bằng Invite Code (Tự động)")
        print(" 5. Đăng xuất (Xóa token)")
        print(" 6. Thoát")
        
        mode = input("\n>> Nhập lựa chọn (1-6): ").strip()
        print("-" * 40)
        
        if mode == "1":
            new_token = login_email_pass()
            if new_token:
                current_token = new_token
                
        elif mode == "2":
            token_input = input(">> Nhập Token lấy từ trình duyệt: ").strip()
            if check_token(token_input):
                current_token = token_input
                save_token(current_token)
                
        elif mode == "3":
            if current_token:
                check_token(current_token)
            else:
                print("[-] Chưa đăng nhập.")
                
        elif mode == "4":
            join_server(current_token)
            
        elif mode == "5":
            if current_token:
                current_token = None
                if os.path.exists(TOKEN_FILE):
                    os.remove(TOKEN_FILE)
                print("[+] Đã xóa file lưu token.")
            else:
                print("[-] Không có token để xóa.")
                
        elif mode == "6":
            print("[*] Tạm biệt, chúc bạn vui vẻ!")
            break
            
        else:
            print("[-] Option không hợp lệ. Vui lòng chọn lại (1-6).")

if __name__ == "__main__":
    main()