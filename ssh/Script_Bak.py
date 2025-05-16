import paramiko
import time

def backup_switch(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)

    shell = ssh.invoke_shell()
    shell.send('terminal length 0\n')
    time.sleep(10)
    shell.send('show running-config\n')
    shell.send('show vlan brief\n')
    time.sleep(10)  # زمان کافی برای اجرای دستور

    output = shell.recv(65535).decode('utf-8')
    with open(f'{hostname}_backup.txt', 'w') as f:
        f.write(output)

    ssh.close()

switches = [
    {'hostname': '192.168.30.254', 'username': 'riabi', 'password': '123'},
    
]

for switch in switches:
    backup_switch(switch['hostname'], switch['username'], switch['password'])