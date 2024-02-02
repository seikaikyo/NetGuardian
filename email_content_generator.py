# generate_html.py
import sqlite3

def fetch_device_statuses(db_path='netguardian.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, hostname, alive, timestamp FROM scan_results")
    devices = cursor.fetchall()
    conn.close()
    return devices

def build_html_message(devices):
    html_content = """
    <html>
        <head></head>
        <body>
            <p>您好，當您收到這封信，表示您已被加入網路設備與伺服器監控異常回報清單內。</p>
            <table border="1">
                <tr>
                    <th>IP 地址</th>
                    <th>主機名</th>
                    <th>狀態</th>
                    <th>最後檢查時間</th>
                </tr>
    """
    for device in devices:
        status_color = "#f8d7da" if device[2] == "dead" else "#d4edda"
        html_content += f"""
                <tr bgcolor="{status_color}">
                    <td>{device[0]}</td>
                    <td>{device[1]}</td>
                    <td>{'存活' if device[2] == 'alive' else '不可達'}</td>
                    <td>{device[3]}</td>
                </tr>
        """
    html_content += """
            </table>
        </body>
    </html>
    """
    return html_content
