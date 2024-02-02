import json
import subprocess
import socket
from datetime import datetime
import sqlite3
import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_content_generator import build_html_message  # 假設您已經將生成 HTML 內容的邏輯移到這個文件中
# 讀取配置檔案
with open('config.json', 'r') as f:
    config = json.load(f)

# 初始化 SQLite 資料庫連接
db_conn = sqlite3.connect('netguardian.db')
cursor = db_conn.cursor()

# 確保 send_email 函數中使用正確的變量名
def send_email(subject, message, html=False):
    server_address = config["email_server"]
    port = config["email_port"]
    sender_email = config["email_sender"]
    receiver_emails = config["email_receiver"]  # 現在是一個列表
    password = config["email_password"]
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)  # 將收件人列表轉換為字符串
    msg['Subject'] = subject
    
    if html:
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))
    
    try:
        # 修正: 使用正確的變量名建立SMTP連接
        with smtplib.SMTP(server_address, port) as mail_server:
            mail_server.starttls()
            mail_server.login(sender_email, password)
            mail_server.sendmail(sender_email, receiver_emails, msg.as_string())
            print("郵件已發送")
    except Exception as e:
        print(f"郵件發送失敗: {e}")

# 添加 fetch_device_statuses 函數
def fetch_device_statuses():
    # 假設您的 SQLite 版本支援窗口函數
    query = """
    SELECT ip, hostname, alive, timestamp FROM (
      SELECT *, ROW_NUMBER() OVER (PARTITION BY ip ORDER BY timestamp DESC) AS rn
      FROM scan_results
    ) WHERE rn = 1
    """
    cursor.execute(query)
    return cursor.fetchall()




def update_device_status(ip, hostname, open_ports, alive, timestamp):
    """更新設備狀態到資料庫並發送郵件通知"""
    # 檢查上一次的狀態
    cursor.execute("SELECT alive, timestamp FROM scan_results WHERE ip = ?", (ip,))
    result = cursor.fetchone()
    last_alive = result[0] if result else None
    last_timestamp = result[1] if result else None
    
    # 更新資料庫
    cursor.execute('''INSERT OR REPLACE INTO scan_results (ip, hostname, open_ports, alive, timestamp)
                      VALUES (?, ?, ?, ?, ?)''',
                   (ip, hostname, json.dumps(open_ports), "alive" if alive else "dead", timestamp))
    db_conn.commit()

    # 打印並根據狀態變化發送通知
    if alive:
        if last_alive == "dead":
            duration = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S") - datetime.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")
            # 格式化 duration 的輸出
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_duration = f"{int(hours)} 小時 {int(minutes)} 分鐘 {int(seconds)} 秒"
            subject = f"設備 {ip} 已恢復連線"
            message = f"設備 {ip} 於 {timestamp} 恢復連線，斷線時間持續了 {formatted_duration}"

            print(message)  # 在終端機中打印狀態
            send_email(subject, message)
        else:
            print(f"設備 {ip} 仍然連線中。")  # 設備持續連線，不需要發送郵件
    else:
        if last_alive != "dead":
            subject = f"設備 {ip} 斷線警告"
            message = f"設備 {ip} 於 {timestamp} 斷線"
            print(message)  # 在終端機中打印狀態
            send_email(subject, message)
        else:
            print(f"設備 {ip} 仍然斷線中。")  # 設備持續斷線，不需要重複發送郵件




def scan_device(ip):
    """掃描指定設備"""
    ping_cmd = ["ping", "-c", "1", ip] if subprocess.os.name != 'nt' else ["ping", "-n", "1", ip]
    ping_result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    alive = ping_result.returncode == 0
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = "Unknown"
    open_ports = []
    if alive:
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            pass
        for port in config["ports"]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                if sock.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
    update_device_status(ip, hostname, open_ports, alive, timestamp)


# main 函數中調用 fetch_device_statuses 並生成HTML郵件內容
def main():
    while True:
        print("開始一輪設備狀態檢查...")
        devices = fetch_device_statuses()
        if devices:
            html_message = build_html_message(devices)
            subject = "主機監控儀表板"
            send_email(subject, html_message, html=True)
        else:
            print("目前沒有設備資料可提供。")
        print("完成一輪設備狀態檢查，將在 {} 秒後進行下一輪檢查。".format(config['ping_interval']))
        time.sleep(config['ping_interval'])


if __name__ == "__main__":
    main()

