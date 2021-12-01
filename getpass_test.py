from netmiko import ConnectHandler
from getpass import getpass


my_device = {
    "device_type": "cisco_ios",
    "host": "k20lab-other",
    "username": "danieldh",
    "password": ("4516+"+getpass()),
    "session_log": "k20lab-other.txt",
}

with ConnectHandler(**my_device) as net_connect:
    output = net_connect.send_command('show configuration')
    print (output)
