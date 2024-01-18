# You will need
- Raspberry Pi, or some other portable Linux box with a network port.
- Power
- Ethernet cable

# Setup

1. Install headless raspbian image (for fast boot) using the Raspbian installer https://www.raspberrypi.com/software/
2. Customize the image if you'd like.
3. First boot/installation

4. Download the files
```
git clone <repo>
```

5. Install dependancies
```
sudo apt update && sudo apt install python3-scapy -y
```

6. Set up a cronjob
```
sudo crontab -e
```

7. Add the following line to crontab (must run as root to send Layer 2 packets)
```
@reboot python3 <full path to python script>
```

# Usage

1. Find a lonely network port
1. Plug pi into network port
1. Give pi power
1. Wait for end signal -- green light off, or push notification (slack webhook is on the wishlist)
    - Success takes about 45 seconds from power on.
    - Failure may take up to a minute.