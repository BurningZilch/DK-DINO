import socket
import fcntl
import struct

def get_ip_address(interface):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            sock.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', interface[:15].encode('utf-8'))
        )[20:24])
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    wlan0_ip = get_ip_address("wlan0")
    if wlan0_ip:
        print("IP address of wlan0:", wlan0_ip)
    else:
        print("Failed to retrieve IP address of wlan0")

