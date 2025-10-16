import networkx as nx
import matplotlib.pyplot as plt
import pysnmp.hlapi as snmp
import subprocess
import json
import time

# Initialize network topology graph
G = nx.Graph()

# SNMP credentials
COMMUNITY_STRING = "public"
SNMP_PORT = 161

# Optimized network scan function
def scan_network(subnet="192.168.1.0/24"):
    """Scan the network using Nmap and return discovered devices."""
    try:
        result = subprocess.run(["nmap", "-sn", subnet], capture_output=True, text=True)
        devices = [line.split()[4] for line in result.stdout.split("\n") if "Nmap scan report" in line]
        return devices
    except subprocess.CalledProcessError:
        print("[ERROR] Network scan failed!")
        return []

# Improved SNMP function to get device type
def get_snmp_info(ip, oid="1.3.6.1.2.1.1.1.0"):
    """Retrieve device info using SNMP."""
    try:
        iterator = snmp.getCmd(
            snmp.SnmpEngine(),
            snmp.CommunityData(COMMUNITY_STRING, mpModel=0),
            snmp.UdpTransportTarget((ip, SNMP_PORT)),
            snmp.ContextData(),
            snmp.ObjectType(snmp.ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication or errorStatus:
            return "Unknown Device"
        return str(varBinds[0][1])
    except Exception as e:
        print(f"[ERROR] SNMP query failed for {ip}: {e}")
        return "Unknown Device"

# Update topology dynamically with improved visualization
def update_topology():
    """Scans the network and updates the topology graph."""
    devices = scan_network()
    if not devices:
        print("[WARNING] No devices found on the network.")
        return

    G.clear()
    for ip in devices:
        device_info = get_snmp_info(ip)
        G.add_node(ip, label=device_info)

    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color="lightblue", font_size=10, edge_color="gray")
    plt.title("Network Topology Map")
    plt.savefig("network_topology.png")  # Save topology image
    plt.show()

# Enhanced threat detection logic
def detect_anomalies():
    """Checks for unknown or rogue devices."""
    critical_devices = {"192.168.1.1": "Router", "192.168.1.2": "Server"}
    for ip in G.nodes:
        if ip not in critical_devices.keys():
            print(f"[ALERT] Unknown device detected: {ip}")

# Save topology data in JSON format
def save_topology():
    """Saves current network topology as a JSON file."""
    with open("network_topology.json", "w") as file:
        json.dump(list(G.nodes), file)

# Run continuously for monitoring
while True:
    update_topology()
    detect_anomalies()
    save_topology()
    time.sleep(30)  # Scan every 30 seconds
