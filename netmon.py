import subprocess
import sys
import socket
from scapy.all import ARP, Ether, srp, ICMP
import time
import datetime
import logging

logging.basicConfig(filename='/root/netmon.log', encoding='utf-8', level=logging.INFO)

def write_message(message):
    print(message)
    logging.info(message)

def get_local_ip(interface):
    try:
        local_ip = subprocess.getoutput(f"ip addr show {interface} | grep 'inet ' | awk '{{print $2}}'")
        return local_ip
    except:
        return None

def get_remote_device_info(ip_address):
    try:
        result, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address), timeout=2, verbose=0)
        for sent, received in result:
            return received[ARP].psrc, received[Ether].src
    except:
        return None, None

def is_internet_reachable():
    try:
        socket.create_connection(("www.google.com", 80), timeout=2)
        return True
    except OSError:
        return False
    
def is_plugged_in(interface):
    result = subprocess.getoutput(f"cat /sys/class/net/{interface}/carrier")
    return result == '1' # If cable is connected the result is 1    
    
def enumerate(interface):
    time_stamp = datetime.datetime.now()
    try:
        if not is_plugged_in(interface):
            #write_message(f"[{time_stamp}] Cable is not plugged in. Waiting...")
            pass
        
        else:
            local_ip = get_local_ip(interface)
            if not local_ip:
                write_message(f"[{time_stamp}] Unable to retrieve local IP address.")
            else:
                write_message(f"[{time_stamp}] Local IP address: {local_ip}")
            # Get remote device info
            remote_ip, remote_mac = get_remote_device_info(local_ip)
            if remote_ip and remote_mac:
                write_message(f"[{time_stamp}] Remote Device IP address: {remote_ip}")
                write_message(f"[{time_stamp}] Remote Device MAC address: {remote_mac}")
                # Check internet connectivity via eth0
                if is_internet_reachable():
                    write_message(f"[{time_stamp}] Internet is reachable via {interface}")
                else:
                    write_message(f"[{time_stamp}] No internet connectivity via {interface}")
            shutdown()
            
    except KeyboardInterrupt:
        write_message("Exiting...")
        shutdown()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
def shutdown():
    subprocess.getoutput('sudo shutdown now')

def main():
    interface = "eth0"
    for i in range(12):
        enumerate(interface)    
        time.sleep(5)
    
    time_stamp = datetime.datetime.now()
    write_message(f'[{time_stamp}] No cable detected after 1 minute')
    shutdown()

if __name__ == "__main__":
    main()
