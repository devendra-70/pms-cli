# 🚑 PMS CLI

A powerful **Python Command-Line Interface (CLI)** tool for managing your **Patient Management System (PMS)** microservices. Add patients, check analytics, and interact with your Kafka-powered backend seamlessly.

## ✨ Features

- ➕ **Add Patients**: Interactive patient registration with validation
- 📊 **Analytics Dashboard**: Real-time patient statistics and metrics
- 🔗 **Microservices Integration**: Connects to your Kafka-powered backend
- ⚡ **Lightweight**: Simple installation with pip
- 🌐 **Cross-Platform**: Works on Linux, Windows, and macOS

## 📋 Prerequisites

- Python 3.7 or higher
- pip package manager
- Running PMS microservices backend

## 🚀 Installation

### Method 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/pms-cli.git
cd pms-cli

# Create and activate virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies and package
pip install -r requirements.txt
pip install .
```

### Method 2: Development Installation

```bash
# For development with editable installation
pip install -e .
```

### Method 3: Build and Install Wheel

```bash
# Build the package
pip install build
python -m build

# Install the built wheel
pip install dist/*.whl
```

## 🎯 Usage

After installation, the `pms` command will be available in your terminal.

### Add a New Patient

```bash
pms add-patient
```

You'll be prompted to enter:
- **Name**: Patient's full name
- **Email**: Valid email address
- **Address**: Patient's address
- **Date of Birth**: In YYYY-MM-DD format

### Check System Analytics

```bash
pms status
```

**Example output:**
```
📊 PMS Analytics Dashboard
═══════════════════════════
Patients Added: 15
Patients Updated: 8
```

### Help and Commands

```bash
# Show all available commands
pms --help

# Get help for specific command
pms add-patient --help
```


### Project Structure

```
pms-cli/
├── pms/                    # CLI package
│   ├── __init__.py
│   ├── api.py             # API interactions
│   ├── cli.py             # CLI commands
│   └── config.py          # Configuration
├── pyproject.toml         # Build configuration
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

## 🐛 Troubleshooting

### Common Issues

**Command not found after installation:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Verify installation
pip list | grep pms-cli
```

**Connection errors:**
```bash
# Check if microservices are running
curl http://localhost:4004/health
curl http://localhost:4002/health
```

**Permission errors on Linux:**
```bash
# Use user installation if needed
pip install --user .
```

## 🔄 Updating

```bash
# Pull latest changes
git pull origin main

# Reinstall package
pip install --upgrade .
```

## 📝 Environment Variables

You can customize the CLI behavior using environment variables:

```bash
# Set custom service URLs
export PMS_PATIENT_SERVICE_URL="http://localhost:4004"
export PMS_ANALYTICS_SERVICE_URL="http://localhost:4002"

# Set Kafka configuration
export PMS_KAFKA_BROKER="localhost:9092"
```

## 👨‍💻 Author

**Your Name**
- GitHub: [@devendra-70](https://github.com/devendra-70)

---

⭐ **Star this repository if you find it helpful!**
