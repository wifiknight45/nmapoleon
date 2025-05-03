import networkx as nx
import matplotlib.pyplot as plt
import pysnmp.hlapi as snmp
import subprocess
import json
import time
import requests

# Network topology graph
G = nx.Graph()

# SNMP credentials
COMMUNITY_STRING = "public"
SNMP_PORT = 161

# Network scan function
def scan_network(subnet="192.168.1.0/24"):
    result = subprocess.run(["nmap", "-sn", subnet], capture_output=True, text=True)
    devices = [line.split()[4] for line in result.stdout.split("\n") if "Nmap scan report" in line]
    return devices

# SNMP function to get device type
def get_snmp_info(ip, oid="1.3.6.1.2.1.1.1.0"):
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
    except Exception:
        return "Unknown Device"

# Update topology dynamically
def update_topology():
    devices = scan_network()
    G.clear()
    for ip in devices:
        device_info = get_snmp_info(ip)
        G.add_node(ip, label=device_info)
    
    nx.draw(G, with_labels=True, node_color="lightblue", font_weight="bold")
    plt.title("Network Topology Map")
    plt.show()

# Threat detection (Example: Flag unknown devices)
def detect_anomalies():
    critical_devices = {"192.168.1.1": "Router", "192.168.1.2": "Server"}
    for ip in G.nodes:
        if ip not in critical_devices.keys():
            print(f"[ALERT] Unknown device detected: {ip}")

# Historical view saving
def save_topology():
    with open("network_topology.json", "w") as file:
        json.dump(list(G.nodes), file)

# Run continuously to monitor changes
while True:
    update_topology()
    detect_anomalies()
    save_topology()
    time.sleep(30)  # Scan every 30 seconds
