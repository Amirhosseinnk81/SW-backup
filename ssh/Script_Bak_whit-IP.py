import paramiko
import time
import os

def backup_switch(hostname, username, password, backup_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password, timeout=10)

        shell = ssh.invoke_shell()
        shell.send('terminal length 0\n')
        time.sleep(2)
        shell.send('show running-config\n')
        shell.send('show vlan brief\n')
        time.sleep(10)

        output = shell.recv(65535).decode('utf-8')

        # بررسی و ایجاد مسیر بکاپ در صورت عدم وجود
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        # ذخیره فایل در مسیر مشخص‌شده
        backup_file = os.path.join(backup_path, f"{hostname}_backup.txt")
        with open(backup_file, 'w') as f:
            f.write(output)

        print(f"✅ بکاپ {hostname} ذخیره شد در {backup_file}")

        ssh.close()

    except Exception as e:
        print(f"❌ خطا در بکاپ‌گیری از {hostname}: {e}")

switches = [
    {'hostname': 'IP', 'username': 'username', 'password': 'password'},
]

backup_path = r"\\192.168.30.2\backups"  # مسیر شبکه‌ای ذخیره بکاپ‌ها

for switch in switches:
    backup_switch(switch['hostname'], switch['username'], switch['password'], backup_path)
