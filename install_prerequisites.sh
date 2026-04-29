#!/bin/bash
# Kelnic Solutions – Prerequisites Installer (Linux/macOS)
# Detects OS and installs all required tools.

set -e

echo "🛠️ Installing prerequisites for Kelnic Solutions..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    # Update package list
    sudo apt update
    # Install core packages
    sudo apt install -y git curl wget python3 python3-pip
    # Install Docker
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
    fi
    # Install Docker Compose plugin
    sudo apt install -y docker-compose-plugin
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    # Install Homebrew if missing
    if ! command -v brew &> /dev/null; then
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install git curl wget python3
    brew install --cask docker
    # Docker Compose is included with Docker Desktop
else
    echo "Unsupported OS. Exiting."
    exit 1
fi

# Install Node.js via nvm
if ! command -v node &> /dev/null; then
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 18
    nvm use 18
fi

# Install global npm packages
npm install -g vercel @railway/cli

# Install OCI CLI
if ! command -v oci &> /dev/null; then
    curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh -o install_oci.sh
    chmod +x install_oci.sh
    ./install_oci.sh --accept-all-defaults
fi

# Install AWS CLI (optional)
if ! command -v aws &> /dev/null; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm -rf aws awscliv2.zip
fi

echo "✅ Prerequisites installed."
echo "Please run 'oci setup config' and log in to Railway/Vercel."
