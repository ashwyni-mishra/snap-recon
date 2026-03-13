# ⚡ Snap-Recon: Rapid Reconnaissance Framework

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="Maintained">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

**Snap-Recon** is a professional-grade, modular, and high-performance reconnaissance framework designed for bug hunters and security researchers. It automates the initial phase of an engagement by gathering critical intelligence across multiple vectors simultaneously.

Developed with a focus on speed, modularity, and actionable output.

---

## 🚀 Key Features

*   🔍 **WHOIS Intelligence**: Comprehensive domain ownership and registration data.
*   🌐 **DNS Enumeration**: Deep-dive into A, AAAA, MX, NS, and TXT records.
*   📡 **Subdomain Discovery**: Multi-threaded active resolving with custom wordlist support.
*   🛡️ **Security Header Inspection**: Analyzes HSTS, CSP, X-Frame-Options, and more for misconfigurations.
*   🛠️ **Tech Detection**: Identifies server-side technologies, CMS, and web servers.
*   📁 **Directory Brute-Forcing**: Rapid discovery of hidden files and exposed directories.
*   🏗️ **Port Scanner & Banner Grabbing**: Identifies open services and retrieves service banners.
*   🔒 **SSL/TLS Scanner**: Comprehensive certificate analysis and expiry tracking.
*   ⏳ **Wayback Machine Integration**: Extracts historical URLs to find forgotten or hidden assets.
*   🧠 **Smart Wordlist Expansion**: Dynamically extracts keywords from found subdomains to sharpen discovery.
*   📊 **Actionable Reporting**: Generates structured Markdown reports with a calculated **Recon Risk Score**.

---

## 🛠️ Installation & Setup

### For Kali Linux / Linux Users (Quick Setup)

This script creates a virtual environment, installs dependencies, and adds an alias for easy access.

```bash
# Clone the repository
git clone https://github.com/ashwyni-mishra/snap-recon.git
cd snap-recon

# Run the setup script
chmod +x setup.sh
./setup.sh
```
After setup, run it from anywhere using:
```bash
snaprecon -d example.com --all
```

### Standard Installation
```bash
# Using Makefile
sudo make install

# OR using pip manually
pip install -r requirements.txt
pip install .
```

---

## 📖 Usage Examples

### 1. Full Surface Scan
Run every module, including new SSL and Wayback modules:
```bash
snaprecon -d example.com --all
```

### 2. Targeted Intelligence Gathering
```bash
snaprecon -d example.com --ssl --wayback --dns
```

### 3. Multiple Wordlist Support
Run discovery against multiple wordlists at once (e.g., small + medium lists):
```bash
snaprecon -d example.com --dirs -w wordlists/default.txt,wordlists/seclist_directories.txt
```

### 4. Manage Wordlists
```bash
# List all available wordlists
snaprecon --list-wordlists

# Download professional SecLists
snaprecon --download-wordlist
```

---

## 📂 Project Structure

```text
snap-recon/
├── core/           # Framework engine and CLI logic
├── modules/        # Pluggable reconnaissance modules
├── wordlists/      # Built-in and downloaded wordlists
├── reports/        # Automated Markdown findings
└── tests/          # Quality assurance suite
```

---

## 🧑‍💻 Developer Info

*   **Author**: syn9
*   **GitHub**: [ashwyni-mishra](https://github.com/ashwyni-mishra)
*   **Version**: 1.0.0

---

## ⚠️ Disclaimer

This tool is for **authorized ethical security testing only**. Use it only on targets you have explicit permission to test. The author is not responsible for any misuse or damage caused by this program.

---
<p align="center">
  Developed by <b>syn9</b> • 2026
</p>
