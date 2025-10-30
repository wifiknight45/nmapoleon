
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Network Monitoring](https://img.shields.io/badge/tool-network%20monitoring-blueviolet.svg)
![Nmap](https://img.shields.io/badge/requires-nmap-red.svg)

# nmapoleon

A Python-based network topology scanner and monitoring tool designed for cybersecurity research and network administration. nmapoleon combines Nmap scanning with SNMP queries to discover, map, and monitor network devices in real-time.

## Features

- **Automated Network Discovery**: Scans specified subnets using Nmap to identify active hosts
- **SNMP Device Profiling**: Queries discovered devices for detailed information using SNMP
- **Visual Topology Mapping**: Generates network topology diagrams showing device relationships
- **Anomaly Detection**: Identifies unknown or rogue devices not in the approved device list
- **Continuous Monitoring**: Supports periodic scanning at configurable intervals
- **Data Export**: Saves topology data in JSON format for further analysis
- **Concurrent Scanning**: Multi-threaded SNMP queries for faster network profiling

## Prerequisites

### System Requirements
- Debian-based Linux distribution (Debian, Ubuntu, Kali, etc.)
- Python 3.7 or higher
- Nmap installed and accessible in PATH

### Install System Dependencies

```bash
# Update package lists
sudo apt update

# Install Nmap
sudo apt install nmap -y

# Install Python3 and venv (if not already installed)
sudo apt install python3 python3-venv python3-pip -y
```

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/wifiknight45/nmapoleon.git

cd nmapoleon
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
```

3. **Activate the virtual environment**
```bash
source venv/bin/activate
```

4. **Install Python dependencies (manually)**
```bash
pip install --upgrade pip
pip install networkx matplotlib pysnmp
```

OR for an easier install method simply install the  `requirements.txt` file provided:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Scan 
Run a single scan of the default subnet (192.168.1.0/12):
```bash
python3 net_topo_mapper.py --iterations 1
```

### Custom Subnet Scan
Scan a different subnet:
```bash
python3 net_topo_mapper.py --subnet 0.0.0.0/00 --iterations 1
```

### Continuous Monitoring
Run continuous monitoring with 60-second intervals:
```bash
python3 net_topo_mapper.py --interval 60
```

### Custom SNMP Configuration
Use a different SNMP community string and port:
```bash
python3 net_topo_mapper.py --community private --snmp-port 161 --iterations 1
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--subnet` | Target subnet to scan (CIDR notation) | 192.168.1.0/24 |
| `--community` | SNMP community string | public |
| `--snmp-port` | SNMP port number | 161 |
| `--interval` | Scan interval in seconds | 30 |
| `--iterations` | Number of scan iterations (0 for continuous) | 0 |

## Output

The tool generates two output files:

1. **network_topology.png**: Visual diagram of the network topology
2. **network_topology.json**: JSON file containing node and edge data

## Configuration

Edit the `DEFAULT_CONFIG` dictionary in `net_topo_mapper.py` to customize:

- Default subnet
- SNMP community string
- Critical devices list (for anomaly detection)
- Scan interval

Example:
```python
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
```

## Security Considerations

**NOTE**: This tool is designed for educational purposes and authorized network security testing only. Any usage of this script confirms comprehension + receipt of this disclaimer and constitutes an agreement to this proviso.  

- Only scan networks you own or have explicit permission to test
- SNMP community strings may be transmitted in plaintext
- Default SNMP credentials ("public") are insecure for production environments
- Consider using SNMPv3 for encrypted authentication in production scenarios
- Be aware of network scanning policies at your organization or institution

## Future Enhancements

This is an ongoing project with the following planned enhancements/improvements:

### Core Functionality
- [ ] SNMPv3 support with encrypted authentication
- [ ] Configuration file support (YAML/JSON)
- [ ] IPv6 subnet scanning
- [ ] Port scanning and service detection integration
- [ ] MAC address vendor lookup
- [ ] Network device type classification (router, switch, AP, etc.)

### Topology & Visualization
- [ ] Interactive web-based topology viewer
- [ ] Multiple layout algorithms (hierarchical, circular, etc.)
- [ ] Device health status indicators (up/down, latency)
- [ ] Historical topology comparison (diff between scans)
- [ ] Export to multiple formats (PDF, SVG, Graphviz DOT)

### Monitoring & Alerting
- [ ] Bandwidth utilization monitoring via SNMP
- [ ] Email/webhook notifications for anomalies
- [ ] Device uptime tracking
- [ ] Custom alerting rules engine
- [ ] Integration with Syslog/SIEM systems

### Database & Storage
- [ ] SQLite/PostgreSQL backend for historical data
- [ ] Time-series data storage for metrics
- [ ] Query API for topology data
- [ ] Automated backup and retention policies

### Security Features
- [ ] Vulnerability scanning integration (OpenVAS, Nessus)
- [ ] Network baseline comparison
- [ ] Rogue device detection with MAC OUI filtering
- [ ] Compliance checking (unauthorized services, open ports)
- [ ] Integration with threat intelligence feeds

### Performance & Scalability
- [ ] Distributed scanning for large networks
- [ ] Scan result caching
- [ ] Optimized SNMP bulk queries
- [ ] Rate limiting and backoff strategies

### User Interface
- [ ] CLI dashboard with real-time updates
- [ ] Web-based management interface
- [ ] RESTful API for external integrations
- [ ] Mobile-friendly topology viewer

### Documentation
- [ ] Detailed API documentation
- [ ] Video tutorials and demos
- [ ] Network topology best practices guide
- [ ] Troubleshooting guide

## Contributing

Contributions are welcome; this project is being developed as part of university cybersecurity research in a sandboxed lab environment.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -am 'Add cool-feature'`)
4. Push to the branch (`git push origin feature/nameOfexample-feature`)
5. create a PR

## License

This is licensed under the M.I.T. License 2.0 see the file titled LICENSE for full details etc. 

## Acknowledgments

- Built with [NetworkX](https://networkx.org/) for graph operations
- Network scanning powered by [Nmap](https://nmap.org/)
- SNMP queries via [PySNMP](https://pysnmp.readthedocs.io/)

## Contact

https://github.com/wifiknight45
wifiknight45@proton.me

---

## Disclaimer

This script is provided as-is for educational and informational purposes. Network scanning and SNMP queries can generate network traffic and might be intrusive in some environments. Ensure you have the necessary permissions before running this script on a network. The anomaly detection is based on a simple list of critical devices and may not catch all types of network anomalies.

 ## this script was powered by excellent playlists + copious quantities of caffeine & nicotine for the purposes of teaching and learning python programming language  

