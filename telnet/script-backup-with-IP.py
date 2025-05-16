import telnetlib
import time
import os
# لیست سوییچ‌ها (IP, یوزرنیم, پسورد, پسورد Enable)
switches = [
    ("192.168.30.254", "riabi", "123"),
]

def backup_switch(host, username, password, backup_path):
    try:
        print(f"اتصال به {host} ...")
        tn = telnetlib.Telnet(host, 23)

        # ورود به سوییچ
        tn.read_until(b"Username:")
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b"Password:")
        tn.write(password.encode('ascii') + b"\n")

        # ورود به حالت enable
        # tn.read_until(b">")
        # tn.write(b"enable\n")
        # tn.read_until(b"Password:")
        # tn.write(enable_password.encode('ascii') + b"\n")

        # دریافت کانفیگ سوییچ
        tn.read_until(b"#")
        tn.write(b"terminal length 0\n")
        tn.write(b"show running-config\n")

        time.sleep(3)  # زمان برای دریافت کامل خروجی
        output = tn.read_very_eager().decode('ascii')

        # بررسی و ایجاد مسیر بکاپ در صورت عدم وجود
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        # ذخیره در فایل مخصوص هر سوییچ
        backup_file = os.path.join(backup_path, f"{host}_backup.txt")
        with open(backup_file, 'w') as f:
            f.write(output)

        print(f"✅ بکاپ از {host} ذخیره شد: {backup_file}")

        # خروج از تلنت
        tn.write(b"exit\n")
        tn.close()

    except Exception as e:
        print(f"❌ خطا در اتصال به {host}: {e}")

backup_path = r"\\192.168.30.2\backups"  # مسیر شبکه‌ای ذخیره بکاپ‌ها

# اجرای بکاپ برای همه سوییچ‌ها
for switch in switches:
    backup_switch(*switch, backup_path)

print("تمام بکاپ‌ها گرفته شد.")
