# Network Rover

Network Rover is a lightweight network scanning tool designed to be compatible with iOS and Pythonista. Network Rover works by pinging possible host addresses and then attempting to open a connection on each of the specified ports. Understanding of basic networking principles are required to manually specify an IP address range. Rover does not attempt to identify any software on the host and is only used to quickly evaluate whether a host is live and if it has any applications listening on the specified ports.

## Dependencies

Make sure you have the following dependencies installed in your Python environment:

- `ping3==4.0.5`
- `pandas==2.1.1`

You can install these dependencies via pip using the provided `dependencies.txt`.
If you are running the script on Pythonista you can install ping3 using pip via StaSh.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/austowe/network-rover.git
    ```

2. Navigate to the cloned directory:

    ```bash
    cd network-rover
    ```

3. Run the `rover.py` script:

    ```bash
    python rover.py
    ```

4. Follow the on-screen prompts to specify the scanning range.

## Features

- **Network Scanning**: Detects live hosts and open ports within a specified network range for specified ports.
- **Customizable Parameters**: Adjust ping timeout, port timeout, target ports, and more through `parameters.py`.
- **Output to CSV**: Optionally saves the scan results to a CSV file.
- **Automatic Private IP Detection**: Quickly scan your network using your device IP, just specify the range you'd like to scan.

## Structure

- **rover.py**: The main script containing functions for network scanning.
- **parameters.py**: Configuration file to customize parameters such as target ports and timeouts.
- **dependencies.txt**: Lists the required dependencies for easy installation.

## License

This project is licensed under the MIT License.
