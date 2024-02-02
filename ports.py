import socket

# 常見的易受攻擊端口列表
vulnerable_ports = [22, 23, 80, 443, 3389]

def print_warning(message):
    # ANSI 代碼 93 是亮黃色
    print(f"\033[93m{message}\033[0m")  # \033[0m 用於重置顏色

def scan_all_ports(ip):
    print("開始掃描...")
    open_ports = []
    total_ports = 1024  # 範例中僅掃描到 1024 端口以減少掃描時間
    for port in range(1, total_ports + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    print(f" 端口 {port} 是開放的。")
                    if port in vulnerable_ports:
                        print_warning(f"⚠️ 警告：端口 {port} 常見於易受攻擊的服務，建議系統管理員檢查並考慮關閉。")
                    open_ports.append(port)
                # 顯示掃描進度
                progress = (port / total_ports) * 100
                print(f"\r掃描進度：{progress:.2f}%", end="")
        except Exception as e:
            print(f"\r掃描端口 {port} 時發生錯誤: {e}")
    print("\n掃描完成。")
    return open_ports

# 範例使用
ip = '10.6.51.226'  # 要掃描的 IP 地址
open_ports = scan_all_ports(ip)
print(f"開放的端口列表: {open_ports}")
