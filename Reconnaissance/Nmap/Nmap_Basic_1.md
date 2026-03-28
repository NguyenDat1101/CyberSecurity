# Giới Thiệu
## Nmap 
**Nmap (Network Mapper)** là môt công cụ bảo mật mã nguồn mở được sử dụng để quét các **host** hoặc các **dịch vụ** đang chạy trên một thiết bị kết nối tới mạng, phuc vụ cho việc phân tích mạng, quản trị hệ thống và được sử dụng rộng rãi trong cộng đồng pentester
### Nguyên lý
Nmap được xây dựng dựa trên:
* TCP/IP stack
* RFC protocol
* Response target

Nmap lợi dụng quá trình **TCP 3-way handshake** để scan
Cấu trúc của một đơn vị dữ liệu trong giao thức **TCP** bao gồm 2 phần chính:
* Header
* Data (payload)
### Cú pháp cơ bản của nmap
`nmap [Scan Type(s)] [Options] {target specification}`
* Scan Type: là loại scan mà nmap sử dụng để scan
* Option: các tùy chọn khác của kiểu scan
* target: mục tiêu cần quét
### Thực hiện quét
Hãy thử với một lệnh cơ bản của Nmap là quét **TCP SYN** (SYN SCAN) là phương pháp quét mặc định của Nmap, đầu tiên Nmap sẽ gửi một cờ **SYN** tới **host** nếu host response với một cờ **SYN/ACK** thì nmap sẽ xác nhận port mở và gửi lại môt cờ **RST** để hủy bỏ quá trình handshake

`nmap -sS -p- -T4 127.0.0.1`
* **-sS**: chế độ **SYN Scan**
* **-p-**: quét tất cả các port từ 1-65535
* **-T4**: tốc độ quét của nmap, tối đa là T5 nhưng có thể bị firewall chặn
* **IP**: IP mình chỉ định là IP Localhost, các bạn có thể sử dụng IP khác
``` bash
$ nmap -sS -p- -T4 127.0.0.1
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-28 17:38 +07
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000020s latency).
Not shown: 65532 closed tcp ports (reset)
PORT      STATE SERVICE
80/tcp    open  http

Nmap done: 1 IP address (1 host up) scanned in 0.40 seconds
```
Kết quả nmap quét được `IP:127.0.0.1` có mở port `80` dịch vụ là `HTTP`

<img width="1920" height="1012" alt="Screenshot_20260328_180110" src="https://github.com/user-attachments/assets/5d49d6df-9a20-4249-841d-4e9967a2d6a0" />

Khi xem bằng **Wireshark** ta có thể thấy quá trình nmap gửi đi **SYN** tới port chỉ định, nếu port mở host sẽ gửi lại một **SYN/ACK** nếu không nmap sẽ gửi **RST** kết thúc quá trình bắt tay.
Ngoài **SYN SCAN** chúng ta còn có các kiểu quét khác như **TCP Connect Scan**, **ACK Scan**, **Window Scan**, **UDP Scan**... Mỗi kiểu quét có ưu nhược điểm của nó. Trường hợp **SYN Scan** trả về một **False positive**, chúng ta có thể sử dụng kiểu quét khác nhiều lần để kiểm chứng kết quả
`nmap -sT -T2 127.0.0.1`
Lệnh trên mình sử dụng kiểu quét **TCP Connect** phương pháp quét này sẽ thiết lập kết nối TCP hoàn chỉnh với mục tiêu, có nghĩa là nmap sẽ thực hiện đủ quy trình bắt tay ba bước, kiểu quét này chậm hơn **SYN Scan** và có thể bi hê thống **IDS/IPS** nhận diện, nhưng đổi lại kết quả sẽ chính xác hơn **SYN Scan** 

<img width="1920" height="1012" alt="Screenshot_20260328_180906" src="https://github.com/user-attachments/assets/581efe33-709b-40c7-b133-39655d427109" />

Với **TCP Connect Scan** có thể thấy rõ sự khác biệt với **SYN Scan**, **TCP Connect Scan** hoàn thành đủ quy trình bắt tay ba bước trong quá trình quét
#### OS Fingerprinting
Nmap sử dụng kỹ thuật **“OS fingerprinting”** để xác định hệ điều hành của mục tiêu. Nmap sẽ gửi các gói tin đặc biệt và dựa trên phản hồi để đoán hệ điều hành và các đặc điểm khác của hệ thống, bao gồm cả thời gian hoạt động (uptime) của máy chủ.
`nmap -O 127.0.0.1`
``` bash
$ nmap -O 127.0.0.1
Starting Nmap 7.95 ( https://nmap.org ) at 2026-03-28 18:16 +07
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000062s latency).
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE
80/tcp   open  http
Device type: general purpose
Running: Linux 2.6.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.32 cpe:/o:linux:linux_kernel:5 cpe:/o:linux:linux_kernel:6
OS details: Linux 2.6.32, Linux 5.0 - 6.2
Network Distance: 0 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.43 seconds
```
Việc quét bằng flag `-O` có thể sẽ cho ra kết quả không mong muốn vì để thực hiện tốt quá trình quét **TCP/IP fingerprinting** đòi hỏi mục tiêu cần mở ít nhất 1 port, không bị **firewall** chặn packet và network phải ổn định, để tăng độ chính xác ta có thể dùng
`nmap -O -sV target` hoặc 
`nmap -A target`
* **-sV**: cờ này sẽ thực hiện kết nối vào service để lấy banner và version
* **-A**: bao gồm các cờ như `-O`, `-sV`, `-sC`

Đó là những khái niệm và cú pháp cơ bản của nmap, folder này mình sẽ chia ra nhiều part để làm. 
