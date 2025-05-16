import telnetlib
import time

# لیست سوییچ‌ها (IP, یوزرنیم, پسورد, پسورد Enable)
switches = [
    ("192.168.30.254", "riabi", "123"),
]

def backup_switch(host, username, password):
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

        # ذخیره در فایل مخصوص هر سوییچ
        filename = f"backup_{host}.txt"
        with open(filename, "w") as file:
            file.write(output)

        print(f"✅ بکاپ از {host} ذخیره شد: {filename}")

        # خروج از تلنت
        tn.write(b"exit\n")
        tn.close()

    except Exception as e:
        print(f"❌ خطا در اتصال به {host}: {e}")

# اجرای بکاپ برای همه سوییچ‌ها
for switch in switches:
    backup_switch(*switch)

print("تمام بکاپ‌ها گرفته شد.")
