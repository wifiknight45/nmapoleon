
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Network Monitoring](https://img.shields.io/badge/tool-network%20monitoring-blueviolet.svg)
![Nmap](https://img.shields.io/badge/requires-nmap-red.svg)

# nmapoleon 
an Interactive Network Topology Mapper that visualizes network augmentation 

Version 1 (v1) updates:
Real-Time Graph Updates: The script continuously scans the network and refreshes the topology.

Device Classification: Identifies and labels devices using SNMP.

Threat Detection: Flags unknown devices for security monitoring.

Historical View: Saves topology snapshots for forensic analysis.

Interactive Web-Based UI: Can be enhanced with Flask to visualize topology interactively.

Automated Alerts: Can notify admins via email or Slack if anomalies are detected.

# Nmapoleon: Network Topology Discovery and Monitoring Tool

## Overview

**Nmapoleon** is a Python script designed to automatically discover devices on a network, visualize the network topology, and identify potential anomalies by detecting unknown devices. It leverages the power of `nmap` for network scanning and SNMP to gather basic device information. The script continuously monitors the network, updates the topology, and saves the current state.

## Features

* **Network Discovery:** Uses `nmap` to scan a specified subnet and identify active hosts.
* **Device Information Retrieval:** Attempts to retrieve basic device information (like system description) using SNMP.
* **Dynamic Topology Visualization:** Creates a graphical representation of the network topology using `networkx` and `matplotlib`, saving the image as `network_topology.png` and displaying it.
* **Anomaly Detection:** Flags devices that are present on the network but not listed in a predefined set of critical devices.
* **Topology Persistence:** Saves the list of discovered devices to a `network_topology.json` file.
* **Continuous Monitoring:** Runs in a loop, periodically scanning the network, updating the topology, and checking for anomalies.

## Prerequisites

Before running Nmapoleon, ensure you have the following installed:

* **Python 3:** The script is written in Python 3.
* **Required Python Libraries:** Install the necessary libraries using pip:
    ```bash
    pip install networkx matplotlib pysnmp
    ```
* **Nmap:** The `nmap` command-line tool must be installed and accessible in your system's PATH. You can usually install it using your operating system's package manager (e.g., `sudo apt-get install nmap` on Debian/Ubuntu, `brew install nmap` on macOS, or by downloading it from the official Nmap website for Windows).

## Setup and Configuration

1.  **Download the Script:** Save the provided Python code as `nmapoleon.py`.
2.  **SNMP Configuration:**
    * The script currently uses the default public community string (`public`) and SNMP port (`161`).
    * If your network devices use a different community string, modify the `COMMUNITY_STRING` variable in the script.
    * Ensure that SNMP is enabled on the network devices you want to monitor and that they allow SNMP queries from the machine running the script.
3.  **Network Subnet:**
    * The default subnet to scan is `192.168.1.0/01`.
    * You can change the `subnet` parameter in the `scan_network()` function call within the main loop if you need to monitor a different network segment.
4.  **Critical Devices:**
    * The `detect_anomalies()` function uses a dictionary `critical_devices` to define known and trusted devices.
    * Modify this dictionary to include the IP addresses and (optional) names of the essential devices on your network (e.g., routers, servers). This helps the script identify any other devices as potential anomalies.

## Running Nmapoleon

1.  **Open a terminal or command prompt.**
2.  **Navigate to the directory where you saved `nmapoleon.py`.**
3.  **Run the script using the Python interpreter:**
    ```bash
    python nmapoleon.py
    ```
4.  The script will start scanning the network, display the network topology, and print any detected anomalies in the console. It will continue to run and update periodically (every 30 seconds by default).
5.  A `network_topology.png` file will be created in the same directory, containing the visual representation of the network topology.
6.  The list of discovered devices will also be saved in `network_topology.json`.

## Understanding the Output

* **Console Output:**
    * Displays information about the network scan process.
    * Prints alerts for any devices found on the network that are not listed in the `critical_devices` dictionary.
    * Shows error messages if the network scan or SNMP queries fail.
* **`network_topology.png`:** A graphical image showing the discovered devices as nodes and their connections (although explicit connections between devices are not determined in this version, it provides a visual inventory). The labels on the nodes are the SNMP system descriptions, if available, or "Unknown Device" otherwise.
* **`network_topology.json`:** A JSON file containing a list of the IP addresses of all the devices currently present on the network according to the latest scan.

## Stopping the Script

To stop the continuous monitoring, press `Ctrl + C` in the terminal where the script is running.

This script provides a basic framework for network topology discovery and anomaly detection.


## Disclaimer

This script is provided as-is for educational and informational purposes. Network scanning and SNMP queries can generate network traffic and might be intrusive in some environments. Ensure you have the necessary permissions before running this script on a network. The anomaly detection is based on a simple list of critical devices and may not catch all types of network anomalies.

Acknowledgements: Alphabet ~ Google Colab ~ Gemini AI ~ Microsoft Copilot
This is licensed under the M.I.T. License 2.0
+ powered by excellent playlists +  copious quantities of caffeine & nicotine. 

