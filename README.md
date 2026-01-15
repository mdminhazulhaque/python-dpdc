# 🔌 DPDC Prepaid CLI

[![PyPI version](https://badge.fury.io/py/dpdc.svg)](https://badge.fury.io/py/dpdc)
[![Python Versions](https://img.shields.io/pypi/pyversions/dpdc.svg)](https://pypi.org/project/dpdc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/dpdc)](https://pepy.tech/project/dpdc)

A Python CLI tool to collect information about **Dhaka Power Distribution Company Limited (DPDC)** prepaid electricity accounts. Get real-time balance, customer information, and account details directly from your terminal.

## ✨ Features

- 💰 **Balance Check**: Get current balance and account information
- 👤 **Customer Info**: Retrieve detailed customer and meter information
- 🔐 **Secure Authentication**: Automatic token-based authentication with DPDC API
- 🚀 **Fast & Lightweight**: Built with Python and designed for speed
- 🔒 **GraphQL API**: Modern API integration with DPDC's official endpoints

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install dpdc
```

### From Source
```bash
git clone https://github.com/mdminhazulhaque/python-dpdc.git
cd python-dpdc
pip install -e .
```

## 🚀 Quick Start

After installation, use the `dpdc-cli` command:

```bash
# Get help
dpdc-cli --help

# Check balance
dpdc-cli get-balance -c YOUR_CUSTOMER_NUMBER

# Get customer information
dpdc-cli get-customer-info -c YOUR_CUSTOMER_NUMBER
```

## 📖 Usage

```
Usage: dpdc-cli [OPTIONS] COMMAND [ARGS]...

  A CLI tool for DPDC Prepaid electricity account management.

Options:
  --help  Show this message and exit.

Commands:
  get-balance        Get current account balance and customer information
  get-customer-info  Get detailed customer information
```

## 💡 Examples

### 💰 Check Balance

Get your current account balance and information:

```bash
$ dpdc-cli get-balance -c 1234567890
```

**Sample Output:**
```
accountId            1234567890
accountType          Pre Paid
balanceRemaining     1250.50
connectionStatus     Active
```

### 👤 Get Customer Information

Retrieve comprehensive customer details:

```bash
$ dpdc-cli get-customer-info -c 1234567890
```

**Sample Output:**
```
accountId            1234567890
customerName         MD. JOHN DOE
customerClass        Residential
mobileNumber         01712345678
```

## 🛠️ Development

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setting up for Development

1. Clone the repository:
```bash
git clone https://github.com/mdminhazulhaque/python-dpdc.git
cd python-dpdc
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .
```

### Dependencies

- `requests` - HTTP library for API calls
- `click` - Command line interface framework
- `tabulate` - Pretty-print tabular data

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an unofficial tool. Use at your own discretion. The authors are not responsible for any issues that may arise from using this tool.
