import socket
import argparse
import concurrent.futures
import time
from datetime import datetime

open_ports = []


def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)

            result = sock.connect_ex((target, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "Unknown"

                print(f"[+] Port {port:<5} OPEN  ({service})")
                open_ports.append((port, service))

    except Exception:
        pass


def save_results(target):
    filename = f"scan_results_{target}.txt"

    with open(filename, "w") as file:
        file.write(f"Port Scan Results for {target}\n")
        file.write(f"Scan Date: {datetime.now()}\n")
        file.write("-" * 40 + "\n")

        for port, service in sorted(open_ports):
            file.write(f"Port {port:<5} OPEN ({service})\n")

    print(f"\nResults saved to: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Python Port Scanner"
    )

    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Target IP address"
    )

    parser.add_argument(
        "-s", "--start",
        type=int,
        default=1,
        help="Starting port (default: 1)"
    )

    parser.add_argument(
        "-e", "--end",
        type=int,
        default=1024,
        help="Ending port (default: 1024)"
    )

    args = parser.parse_args()

    target = args.target
    start_port = args.start
    end_port = args.end

    print("=" * 50)
    print(f"Scanning Target : {target}")
    print(f"Port Range      : {start_port}-{end_port}")
    print(f"Started At      : {datetime.now()}")
    print("=" * 50)

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, target, port)

    end_time = time.time()

    print("\n" + "=" * 50)

    if open_ports:
        print(f"Open Ports Found: {len(open_ports)}")
    else:
        print("No open ports found.")

    print(f"Scan completed in {end_time - start_time:.2f} seconds")

    save_results(target)


if __name__ == "__main__":
    main()