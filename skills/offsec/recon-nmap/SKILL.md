---
name: recon-nmap
description: >
  Network reconnaissance and security auditing using Nmap for port scanning, service enumeration,
  and vulnerability detection. Use when: (1) Conducting authorized network reconnaissance and asset
  discovery, (2) Enumerating network services and identifying running versions, (3) Detecting
  security vulnerabilities through NSE scripts, (4) Mapping network topology and firewall rules,
  (5) Performing compliance scanning for security assessments, (6) Validating network segmentation
  and access controls.
version: 0.1.0
maintainer: sirappsec@gmail.com
category: offsec
tags: [reconnaissance, nmap, port-scanning, service-enumeration, network-security, osint]
frameworks: [MITRE-ATT&CK, OWASP, PTES]
dependencies:
  packages: [nmap]
  tools: [python3, masscan]
references:
  - https://nmap.org/book/
  - https://nmap.org/nsedoc/
  - https://attack.mitre.org/techniques/T1046/
---

# Nmap Network Reconnaissance

## Overview

Nmap (Network Mapper) is the industry-standard tool for network discovery, security auditing, and vulnerability assessment. This skill provides structured workflows for authorized reconnaissance operations including port scanning, service enumeration, OS fingerprinting, and vulnerability detection using Nmap Scripting Engine (NSE).

**IMPORTANT**: Network scanning may be disruptive and must only be conducted with proper authorization. Always ensure written permission before scanning networks or systems you do not own.

## Quick Start

Basic host discovery and port scanning:

```bash
# Quick scan of common ports
nmap -F <target-ip>

# Scan top 1000 ports with service detection
nmap -sV <target-ip>

# Comprehensive scan with OS detection and default scripts
nmap -A <target-ip>
```

## Core Workflow

### Network Reconnaissance Workflow

Progress:
[ ] 1. Verify authorization and scope
[ ] 2. Perform host discovery and asset enumeration
[ ] 3. Conduct port scanning on live hosts
[ ] 4. Enumerate services and versions
[ ] 5. Perform OS fingerprinting and detection
[ ] 6. Run NSE scripts for vulnerability detection
[ ] 7. Document findings and generate reports
[ ] 8. Validate results and identify false positives

Work through each step systematically. Check off completed items.

### 1. Authorization Verification

**CRITICAL**: Before any scanning activities:
- Confirm written authorization from network owner
- Review scope document for in-scope IP ranges and domains
- Verify scanning windows and rate-limiting requirements
- Document emergency contact for accidental disruption
- Confirm blacklisted hosts (production databases, critical infrastructure)

### 2. Host Discovery

Identify live hosts in target network:

```bash
# Ping sweep (ICMP echo)
nmap -sn <target-network>/24

# ARP scan (local network only, faster and more reliable)
nmap -sn -PR <target-network>/24

# TCP SYN ping (when ICMP blocked)
nmap -sn -PS22,80,443 <target-network>/24

# UDP ping (for hosts blocking TCP)
nmap -sn -PU53,161 <target-network>/24

# Disable ping, assume all hosts alive
nmap -Pn <target-network>/24
```

**Host discovery techniques**:
- **ICMP Echo (-PE)**: Standard ping, often blocked
- **TCP SYN (-PS)**: Half-open connection to specified ports
- **TCP ACK (-PA)**: Sends ACK packets, useful for stateful firewalls
- **UDP (-PU)**: Sends UDP packets to specified ports
- **ARP (-PR)**: Layer 2 discovery, only works on local network

Output live hosts to file for subsequent scanning:

```bash
nmap -sn <target-network>/24 -oG - | awk '/Up$/{print $2}' > live_hosts.txt
```

### 3. Port Scanning

Scan discovered hosts for open ports:

```bash
# Fast scan (top 100 ports)
nmap -F -iL live_hosts.txt

# Top 1000 ports (default)
nmap -iL live_hosts.txt

# Scan all 65535 ports
nmap -p- -iL live_hosts.txt

# Scan specific ports
nmap -p 22,80,443,3389,8080 -iL live_hosts.txt

# Scan port ranges
nmap -p 1-1024,3000-9000 -iL live_hosts.txt
```

**Scan techniques**:

- **TCP SYN Scan (-sS)**: Default, stealthy half-open scan (requires root)
  ```bash
  sudo nmap -sS <target-ip>
  ```

- **TCP Connect Scan (-sT)**: Full TCP connection (no root required)
  ```bash
  nmap -sT <target-ip>
  ```

- **UDP Scan (-sU)**: Scan UDP ports (slow but critical)
  ```bash
  sudo nmap -sU -p 53,161,500 <target-ip>
  ```

- **Version Detection (-sV)**: Probe services for version information
  ```bash
  nmap -sV <target-ip>
  ```

- **Aggressive Scan (-A)**: Enable OS detection, version detection, script scanning, traceroute
  ```bash
  sudo nmap -A <target-ip>
  ```

**Timing**: `-T0` (paranoid/IDS evasion) through `-T5` (insane/fast); `-T3` is default; `-T4` for reliable networks.

**Rate limiting**: `--max-rate 100` (packets/sec), `--scan-delay 1s` (avoid detection).

### 4. Service Enumeration

Identify services and extract version information:

```bash
# Service version detection
nmap -sV <target-ip>

# Aggressive version detection (more probes)
nmap -sV --version-intensity 5 <target-ip>

# Light version detection (fewer probes, faster)
nmap -sV --version-intensity 0 <target-ip>

# Specific service enumeration
nmap -sV -p 80,443 --script=http-headers,http-title <target-ip>
```

**Service-specific enumeration**:

```bash
# SMB enumeration
nmap -p 445 --script=smb-os-discovery,smb-security-mode <target-ip>

# SSH enumeration
nmap -p 22 --script=ssh-hostkey,ssh-auth-methods <target-ip>

# DNS enumeration
nmap -p 53 --script=dns-nsid,dns-recursion <target-ip>

# HTTP/HTTPS enumeration
nmap -p 80,443 --script=http-methods,http-robots.txt,http-title <target-ip>

# Database enumeration
nmap -p 3306 --script=mysql-info <target-ip>
nmap -p 5432 --script=pgsql-brute <target-ip>
nmap -p 1433 --script=ms-sql-info <target-ip>
```

### 5. Operating System Detection

Identify target operating systems:

```bash
# OS detection
sudo nmap -O <target-ip>

# Aggressive OS detection with version scanning
sudo nmap -A <target-ip>

# Limit OS detection to promising targets
sudo nmap -O --osscan-limit <target-ip>

# Guess OS aggressively
sudo nmap -O --osscan-guess <target-ip>
```

**OS fingerprinting indicators**:
- TCP/IP stack characteristics
- Open port patterns
- Service banners and versions
- TTL values and TCP window sizes

### 6. NSE Script Scanning

Nmap Scripting Engine for advanced reconnaissance and vulnerability detection:

```bash
# Run default NSE scripts
nmap -sC <target-ip>

# Run all scripts in category
nmap --script=vuln <target-ip>
nmap --script=exploit <target-ip>
nmap --script=discovery <target-ip>

# Run specific script
nmap --script=http-sql-injection <target-ip>

# Multiple scripts
nmap --script=smb-vuln-ms17-010,smb-vuln-cve-2017-7494 <target-ip>

# Script with arguments
nmap --script=http-brute --script-args http-brute.path=/admin <target-ip>
```

**NSE script categories**: `auth`, `brute`, `default` (-sC), `discovery`, `exploit`, `intrusive`, `malware`, `safe`, `version`, `vuln`

**Common vulnerability detection scripts**:

```bash
# Check for EternalBlue (MS17-010)
nmap -p 445 --script=smb-vuln-ms17-010 <target-ip>

# Heartbleed detection
nmap -p 443 --script=ssl-heartbleed <target-ip>

# Shellshock detection
nmap --script=http-shellshock --script-args uri=/cgi-bin/test.sh <target-ip>

# Check for weak SSL/TLS
nmap -p 443 --script=ssl-enum-ciphers <target-ip>

# SQL injection testing
nmap -p 80 --script=http-sql-injection <target-ip>

# Check for anonymous FTP
nmap -p 21 --script=ftp-anon <target-ip>
```

### 7. Output and Reporting

Generate reports in multiple formats:

```bash
# Normal output to screen and file
nmap <target-ip> -oN scan_results.txt

# XML output (for parsing/import)
nmap <target-ip> -oX scan_results.xml

# Grepable output (for easy parsing)
nmap <target-ip> -oG scan_results.gnmap

# All formats
nmap <target-ip> -oA scan_results

# Script kiddie output (for fun)
nmap <target-ip> -oS scan_results.skid
```

Convert and process results:

```bash
# Convert XML to HTML report
xsltproc /usr/share/nmap/nmap.xsl scan_results.xml -o report.html

# Parse XML with Python
python3 -c "import xml.etree.ElementTree as ET; tree = ET.parse('scan_results.xml'); root = tree.getroot(); [print(host.find('address').get('addr')) for host in root.findall('host')]"

# Extract open ports from grepable output
grep 'Ports:' scan_results.gnmap | awk '{print $2, $5}'
```

### 8. Firewall and IDS Evasion

```bash
sudo nmap -f <target-ip>                           # Fragment packets
sudo nmap -D RND:10 <target-ip>                    # Random decoys
nmap --randomize-hosts -iL targets.txt             # Randomize order
sudo nmap -sI <zombie-host> <target-ip>            # Idle scan
nmap --proxies http://proxy:8080 <target-ip>       # Use proxy
```

## Security Considerations

- **Written Permission**: Obtain explicit authorization before scanning any network
- **Rate Limiting**: Use `--max-rate` to avoid overwhelming targets; schedule during maintenance windows
- **Disruption Risk**: DOS/exploit scripts can crash services; validate findings before reporting
- **Audit Logging**: Document timestamps, source IP, target ranges, ports, arguments, and findings
- **Compliance**: PTES (reconnaissance), MITRE ATT&CK T1046, PCI-DSS 11.2, ISO 27001 A.12.6

## Common Patterns

### Pattern 1: External Perimeter Assessment

```bash
# Phase 1: Identify live hosts
nmap -sn -PE -PS80,443 -PA3389 <external-network>/24 -oG - | awk '/Up$/{print $2}' > external_hosts.txt

# Phase 2: Scan common external services
nmap -Pn -sV -p 21,22,25,53,80,110,143,443,587,993,995,3389,8080,8443 -iL external_hosts.txt -oA external_scan

# Phase 3: Vulnerability detection
nmap -Pn -sV --script=vuln -p 21,22,25,80,443,3389,8080,8443 -iL external_hosts.txt -oA external_vulns

# Phase 4: SSL/TLS security audit
nmap -Pn -p 443,8443 --script=ssl-enum-ciphers,ssl-cert -iL external_hosts.txt -oA ssl_audit
```

### Pattern 2: Internal Network Mapping

```bash
# Phase 1: Fast host discovery
nmap -sn -PR <internal-network>/24 -oG - | awk '/Up$/{print $2}' > internal_hosts.txt

# Phase 2: Comprehensive port scan
nmap -sV -p- -T4 -iL internal_hosts.txt -oA internal_full_scan

# Phase 3: OS fingerprinting
sudo nmap -O -iL internal_hosts.txt -oA internal_os_detection

# Phase 4: Service enumeration
nmap -sV --script=default,discovery -iL internal_hosts.txt -oA internal_services
```

### Pattern 3: Web Application Discovery

```bash
# Identify web servers
nmap -p 80,443,8000,8080,8443 --open -oG - <target-network>/24 | grep 'open' | awk '{print $2}' > web_servers.txt

# Enumerate web technologies
nmap -sV -p 80,443,8080,8443 --script=http-enum,http-headers,http-methods,http-title,http-server-header -iL web_servers.txt -oA web_enum

# Check for common web vulnerabilities
nmap -p 80,443 --script=http-sql-injection,http-csrf,http-vuln-cve2017-5638 -iL web_servers.txt -oA web_vulns
```

### Pattern 4: SMB/CIFS Security Audit

```bash
# Enumerate SMB hosts
nmap -p 445 --open <target-network>/24 -oG - | grep 'open' | awk '{print $2}' > smb_hosts.txt

# SMB version and configuration
nmap -p 445 --script=smb-protocols,smb-security-mode,smb-os-discovery -iL smb_hosts.txt -oA smb_enum

# Check for SMB vulnerabilities
nmap -p 445 --script=smb-vuln* -iL smb_hosts.txt -oA smb_vulns

# Enumerate shares (authentication may be required)
nmap -p 445 --script=smb-enum-shares,smb-enum-users -iL smb_hosts.txt -oA smb_shares
```

## Integration Points

### CI/CD Integration

```bash
# Fail build if vulnerabilities found
nmap -Pn -sV --script=vuln -p 21,22,25,80,443,3389,8080 "$TARGET_NETWORK" -oA security_scan
grep -i "VULNERABLE" security_scan.nmap && { echo "CRITICAL: Vulnerabilities detected!"; exit 1; }
```

### Security Tools Integration

- **Metasploit**: Import XML with `db_import`
- **Vulnerability Scanners**: Feed results to Nessus, OpenVAS, Qualys
- **SIEM**: Parse Nmap output for security monitoring
- **MITRE ATT&CK**: T1595 (Active Scanning), T1046 (Network Service Scanning)

## Troubleshooting

- **No results despite hosts online**: Try `nmap -Pn` (skip ping) or multiple discovery techniques: `nmap -PE -PS22,80,443 -PA3389 -PU53,161`
- **Scan too slow**: Use `-T4`, scan fewer ports with `-F`, or use `masscan -p 1-65535 --rate 10000` for high-speed pre-scan
- **False positives in vuln scripts**: Verify manually, use `--version-intensity 9`, run specific scripts instead of broad categories
- **Blocked by firewall/IDS**: Use `-T1 --scan-delay 1s`, fragment packets with `-f`, use source port 53 with `-g 53`

## Defensive Considerations

Detect Nmap scanning with Network IDS (Snort/Suricata) signature detection, firewall logs for single-source connection bursts, port scan detection for incomplete SYN sequences, honeypots for decoy service access, and traffic analysis for fragmentation anomalies. Deploy rate limiting on border firewalls and port knocking for sensitive services.

## References

- [Nmap Network Scanning Official Guide](https://nmap.org/book/)
- [NSE Script Documentation](https://nmap.org/nsedoc/)
- [MITRE ATT&CK: Network Service Scanning](https://attack.mitre.org/techniques/T1046/)
- [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/Intelligence_Gathering)
- [OWASP Testing Guide: Information Gathering](https://owasp.org/www-project-web-security-testing-guide/stable/4-Web_Application_Security_Testing/01-Information_Gathering/)
