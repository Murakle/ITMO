import math

def ip2int(addr):
    return int(ipaddress.IPv4Address(addr))

def int2ip(addr):
    str(ipaddress.IPv4Address(addr))


if __name__ == '__main__':
    print("Enter ip:")
    ip = input()
    print("Enter mask:")
    mask = input()
    print(ip + "/" + mask)
    ip = ip2int(ip)
    network_size = []
    for i in range
