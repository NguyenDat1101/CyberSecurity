import socket
import threading

target = input("IP:")
Port = int(input("Port:"))
Port_Open = 0
Port_Closed = 0

def port_scanner(target, Port, Port_Open, Port_Closed):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, Port))

    if result == 0:
        print(f"[+] {Port} Open")
        Port_Open = Port_Open + 1
    else:
        Port_Closed = Port_Closed + 1
    s.close()

for port in range(1, Port+1):
    t = threading.Thread(target = port_scanner, args=(target, port, Port_Open, Port_Closed))
    t.start()


