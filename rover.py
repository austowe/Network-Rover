import socket
from ipaddress import IPv4Network
from ping3 import ping
import sys
import parameters
import pandas as pd
import os
import platform

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('google.com', 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = 'N/A'
    return ip

def ping_host(ip):
    try:
        response = ping(ip, timeout=parameters.ping_timeout)  # lower is faster, less consistent
        if response is not None and response != False:
            return response is not None
        else:
            return None
    except socket.error:
        return False

def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(parameters.port_timeout)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

def scan_network(network, target_ports, verbose_output):
    live_hosts = []
    open_ports = []
    network = IPv4Network(network, strict=False)
    port_dict = {}

    print("Scanning in progress...\n")

    try:
        for ip in network.hosts():
            ip = str(ip)
            if verbose_output:
                sys.stdout.write('\r' + f'\rPinging {ip}...       ')

            if ping_host(ip):
                if verbose_output:
                    print("\nHost is alive. Scanning ports... ")
                else:
                    print(f"{ip} is alive.")
                live_hosts.append(ip)
                port_dict[ip] = []
                counter = 1
                for port in target_ports:
                    if verbose_output:
                        percentage = counter / len(target_ports) * 20
                        message = "["
                        print_percentage = 0
                        while print_percentage < percentage:
                            message += "="
                            print_percentage += 1
                        while len(message) < 21:
                            message += " "
                        message += "]"
                        sys.stdout.write('\r' + message + f" {port} ")
                    if is_port_open(ip, port):
                        sys.stdout.write('\r' + f"Port {port} open              \n")
                        open_ports.append(f"{ip}:{port}")
                        port_dict[ip].append(port)
                    counter += 1
                if verbose_output:
                    sys.stdout.write("\r[====================] Done  \n")
            else:
                cont = True

    except KeyboardInterrupt:
        print("\nScanning interrupted.")

    return live_hosts, open_ports, port_dict

def main():
    # Automatically detect the local network address
    local_ip = get_local_ip()
    if local_ip == 'N/A':
        print("Error: Unable to detect local IP address.")
        return
    system_info = platform.system()
    if system_info == 'Darwin' and 'iPhone' in platform.machine():
        print('\nNetworkRover\n')
    else:
        print(''' _   _      _                      _     ______                    
| \ | |    | |                    | |    | ___ \                   
|  \| | ___| |___      _____  _ __| | __ | |_/ /_____   _____ _ __ 
| . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ / |    // _ \ \ / / _ \ '__|
| |\  |  __/ |_ \ V  V / (_) | |  |   <  | |\ \ (_) \ V /  __/ |   
\_| \_/\___|\__| \_/\_/ \___/|_|  |_|\_\ \_| \_\___/ \_/ \___|_|   
                                                                   ''')
    print('Built by github.com/austowe\n')
    print('Current settings:')
    print(f' - Ping timeout: {parameters.ping_timeout}')
    print(f' - Port timeout: {parameters.port_timeout}')
    print(f' - Output to CSV: {parameters.output_to_csv}')
    print(f' - Verbose Output: {parameters.verbose_output}\n')


    #build scan range based on selection
    print("Select scanning mode:")
    print("1. Last two octets")
    print("2. Last octet")
    print("3. Manual specification")

    mode_choice = input("\nEnter the mode number: ")

    if mode_choice == '1':
        network_address = f"{local_ip.split('.')[0]}.{local_ip.split('.')[1]}.0.0/16"
    elif mode_choice == '2':
        network_address = f"{local_ip.rsplit('.', 1)[0]}.0/24"
    elif mode_choice == '3':
        manual_network = input("Enter the network address (CIDR format): ")
        network_address = manual_network
    else:
        print("Invalid mode selection. Exiting.")
        return

    #specify the target ports to scan from parameters.py
    target_ports = parameters.target_ports
    verbose_output = parameters.verbose_output
    
    try:
        print(f"Scanning network {network_address} for specified ports...\n")
        live_hosts, open_ports, port_dict = scan_network(network_address, target_ports, verbose_output)

        if live_hosts:
            print("\n\nFindings:\nLive hosts:")
            for host in live_hosts:
                print(f"- {host}")

            if open_ports:
                print("\nOpen ports:")
                for port in open_ports:
                    print(f"- {port}")
            else:
                print("No open ports found.")

            print("\nSummary:")
            print(f"Total live hosts found: {len(live_hosts)}")
            print(f"Total open ports found: {len(open_ports)}")

            if parameters.output_to_csv:
                data = {
                    'Hosts':[],
                    'Ports':[],
                }
                #print(port_dict)
                for host in live_hosts:
                    ports = ''
                    for port in port_dict[host]:
                        ports += f'{port};'
                    data["Hosts"].append(host)
                    data["Ports"].append(ports)
                df = pd.DataFrame(data)
                counter = 1
                filename = "output.csv"
                while os.path.exists(filename):
                    #increment for unique filename
                    filename = f"output_{counter}.csv"
                    counter += 1
    
                #save dataframe
                df.to_csv(filename, index=False)

        else:
            print("No live hosts found.")

    except KeyboardInterrupt:
        print("\nScanning stopped.")

if __name__ == "__main__":
    main()