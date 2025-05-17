#!/usr/bin/env python3
import argparse
import logging
import networkx as nx
import matplotlib.pyplot as plt
import pysnmp.hlapi as snmp
import subprocess
import json
import time
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging for detailed error and status reporting.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Global network graph
G = nx.Graph()

# Default configuration values
DEFAULT_CONFIG = {
    'subnet': '192.168.1.0/24',
    'community_string': 'public',
    'snmp_port': 161,
    'scan_interval': 30,
    'critical_devices': {
        "192.168.1.1": "Router",
        "192.168.1.2": "Server"
    }
}

def check_nmap_installed():
    """Ensure that Nmap is installed and accessible."""
    if not shutil.which("nmap"):
        logger.error("Nmap is not installed or not in PATH. Please install Nmap before running the scan.")
        return False
    return True

def scan_network(subnet):
    """
    Scan the network using Nmap and return discovered devices.
    Returns a list of IP addresses.
    """
    if not check_nmap_installed():
        logger.error("Network scan aborted due to missing Nmap tool.")
        return []

    try:
        # Run a ping scan (-sn) on the subnet.
        result = subprocess.run(["nmap", "-sn", subnet], capture_output=True, text=True, check=True)
        devices = []
        for line in result.stdout.splitlines():
            if "Nmap scan report for" in line:
                parts = line.split()
                # Check for hostname with IP in parentheses (e.g., "hostname (192.168.1.10)")
                if "(" in line and ")" in line:
                    ip = line.split("(")[-1].split(")")[0]
                else:
                    ip = parts[-1]
                devices.append(ip)
        logger.info(f"Discovered devices: {devices}")
        return devices
    except subprocess.CalledProcessError as e:
        logger.error(f"Network scan failed: {e}")
        return []

def get_snmp_info(ip, community, snmp_port, oid="1.3.6.1.2.1.1.1.0"):
    """
    Retrieve device information using SNMP.
    Returns a string describing the device or 'Unknown Device' on error.
    """
    try:
        iterator = snmp.getCmd(
            snmp.SnmpEngine(),
            snmp.CommunityData(community, mpModel=0),
            snmp.UdpTransportTarget((ip, snmp_port), timeout=2, retries=1),
            snmp.ContextData(),
            snmp.ObjectType(snmp.ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            logger.debug(f"SNMP error for {ip}: {errorIndication}")
            return "Unknown Device"
        if errorStatus:
            logger.debug(f"SNMP error for {ip} at index {errorIndex}: {errorStatus.prettyPrint()}")
            return "Unknown Device"
        return str(varBinds[0][1])
    except Exception as e:
        logger.error(f"SNMP query failed for {ip}: {e}")
        return "Unknown Device"

def update_topology(subnet, community, snmp_port):
    """
    Scans the network, performs SNMP queries concurrently for each discovered device,
    updates the network graph, and saves a visualization.
    """
    devices = scan_network(subnet)
    if not devices:
        logger.warning("No devices found on the network.")
        return

    # Clear existing topology data.
    G.clear()

    # Perform SNMP queries concurrently to speed up scanning.
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_ip = {executor.submit(get_snmp_info, ip, community, snmp_port): ip for ip in devices}
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            device_info = future.result()
            G.add_node(ip, label=device_info)

    # Optional: add edges to simulate a star topology for critical devices.
    critical_devices = DEFAULT_CONFIG['critical_devices']
    for crit_ip in critical_devices.keys():
        if crit_ip in G:
            for node in G.nodes:
                if node != crit_ip:
                    G.add_edge(crit_ip, node)

    # Visualize the network topology.
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    node_labels = {node: data.get("label", node) for node, data in G.nodes(data=True)}
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color="lightblue", font_size=10, edge_color="gray")
    plt.title("Network Topology Map")
    plt.savefig("network_topology.png")
    plt.close()  # Close the figure to avoid blocking
    logger.info("Topology updated and visualization saved as 'network_topology.png'.")

def detect_anomalies(critical_devices):
    """
    Checks for unknown or rogue devices by comparing discovered IPs against known critical devices.
    Logs a warning for each device not in the critical devices list.
    """
    for ip in G.nodes:
        if ip not in critical_devices:
            logger.warning(f"ALERT: Unknown device detected: {ip}")

def save_topology(file_name="network_topology.json"):
    """
    Saves the current network topology to a JSON file.
    The JSON includes node details and edges between devices.
    """
    data = {
        "nodes": [{"ip": n, "label": G.nodes[n].get("label", n)} for n in G.nodes],
        "edges": [{"source": u, "target": v} for u, v in G.edges]
    }
    try:
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
        logger.info(f"Topology data saved to '{file_name}'.")
    except Exception as e:
        logger.error(f"Failed to save topology: {e}")

def main():
    parser = argparse.ArgumentParser(description="Network Topology Scanner and Monitor")
    parser.add_argument("--subnet", type=str, default=DEFAULT_CONFIG['subnet'],
                        help="Subnet to scan (default: %(default)s)")
    parser.add_argument("--community", type=str, default=DEFAULT_CONFIG['community_string'],
                        help="SNMP community string (default: %(default)s)")
    parser.add_argument("--snmp-port", type=int, default=DEFAULT_CONFIG['snmp_port'],
                        help="SNMP port (default: %(default)s)")
    parser.add_argument("--interval", type=int, default=DEFAULT_CONFIG['scan_interval'],
                        help="Scan interval in seconds (default: %(default)s)")
    parser.add_argument("--iterations", type=int, default=0,
                        help="Number of iterations (0 for continuous run)")
    args = parser.parse_args()

    loop_forever = (args.iterations == 0)
    count = 0

    while loop_forever or (count < args.iterations):
        start_time = time.time()
        logger.info(f"Scan iteration {count+1} starting.")
        update_topology(args.subnet, args.community, args.snmp_port)
        detect_anomalies(DEFAULT_CONFIG['critical_devices'])
        save_topology()
        count += 1

        # Compute elapsed time and sleep the remainder of the scan interval.
        elapsed = time.time() - start_time
        sleep_time = max(args.interval - elapsed, 0)
        logger.info(f"Sleeping for {sleep_time:.2f} seconds before next scan.")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
