import socket

target = input("ip:") ## Nhập từ bàn phím user với biến là target
x = int(input("nhap day x:")) ## Nhập dãy port từ 1 - x+1 cần quét
dem = 0
dem_dong = 0

def port_scanner(target, x, dem, dem_dong):
    for i in range (1, x+1):
        s = socket.socket() ## Khởi tạo biến socket
        s.settimeout(1) 
        
        result = s.connect_ex((target, i))

        if result == 0: ## Kiểm tra các cổng mở
            print(f"[+] Port {i} OPEN")
            dem=dem+1
        else:
            dem_dong=dem_dong + 1
            
        s.close()
    print(f"{dem} PORT OPEN")
    print(f"{dem_dong} PORT CLOSED")
          

port_scanner(target, x, dem, dem_dong)
