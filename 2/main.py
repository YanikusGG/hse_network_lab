import argparse
import subprocess
import platform
import ipaddress
import socket


MIN_MTU = 68
MAX_MTU = 17966
HEADER_SIZE = 28
PING_COUNT = 1
PING_TIMEOUT = 1.0


def check_host(host):
    try:
        socket.gethostbyname(host)
    except:
        try:
            ipaddress.ip_address(host)
        except:
            return False

    return True

def do_ping_command(host, mtu, system):
    if system == "Windows":
        ping_command = ["ping", "-4", "-f", "-n", str(PING_COUNT), "-w", str(int(PING_TIMEOUT * 1000.0)), "-l", str(mtu - HEADER_SIZE), host]
    else:
        ping_command = ["ping", "-4", "-M", "do", "-c", str(PING_COUNT), "-W", str(PING_TIMEOUT), "-s", str(mtu - HEADER_SIZE), host]
    return subprocess.run(ping_command, capture_output=True)

def main():
    parser = argparse.ArgumentParser(prog='MTUFinder', description='Find best MTU')
    parser.add_argument('host')
    args = parser.parse_args()

    host = args.host
    if not check_host(host):
        print("The argument should be a hostname or an IP address")
        exit(1)

    system = platform.system()
    try:
        response = do_ping_command(host, MIN_MTU, system)
        assert response.returncode == 0
    except:
        print('Host is unreachable or icmp was blocked.')
        exit(1)

    l, r = MIN_MTU, MAX_MTU
    while r - l > 1:
        print(f"min={l} max={r}")
        mid = (l + r) // 2

        try:
            response = do_ping_command(host, mid, system)
        except:
            print('Host is unreachable or icmp was blocked')
            exit(1)

        if response.returncode == 0:
            l = mid
        else:
            r = mid

    print(f"Best MTU = {l}")

if __name__ == '__main__':
    main()
