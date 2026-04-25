# EC2 Deployment Guide

This repository contains everything needed to deploy the Image Captioning Model on an AWS EC2 instance using Docker.

## Prerequisites

1.  **EC2 Instance**: An Ubuntu instance (t2.medium or larger recommended due to TensorFlow memory requirements) is recommended.
2.  **Security Group**: Ensure port **80** (HTTP) and **22** (SSH) are open.

## Step-by-Step Deployment

### 1. Connect to your EC2 instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 2. Install Docker and Docker Compose
```bash
# Update packages
sudo apt-get update

# Install Docker and Git LFS
sudo apt-get install -y docker.io git-lfs

# Initialize Git LFS
git lfs install

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to the docker group (optional, requires logout/login)
sudo usermod -aG docker $USER
```

### 3. Clone the Repository
```bash
git clone https://github.com/Samgoldwin/Image-captioning-model.git
cd Image-captioning-model
# Ensure all large model files are downloaded
git lfs pull
```

### 4. Build and Run with Docker Compose
```bash
sudo docker-compose up -d --build
```

### 5. Access the App
Open your browser and navigate to `http://your-ec2-ip`.

## Troubleshooting
- **Memory Issues**: TensorFlow can be memory-intensive. If the container crashes, check if your EC2 instance has enough RAM (at least 4GB recommended).
- **Logs**: View logs using `sudo docker-compose logs -f`.

---

## Alternative: Manual Deployment (No Docker)

If you have limited disk space or want to avoid Docker, follow these steps to run the app directly on the EC2 host.

### 1. Install Python and Git LFS
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git-lfs
git lfs install
```

### 2. Clone and Pull Models
```bash
git clone https://github.com/Samgoldwin/Image-captioning-model.git
cd Image-captioning-model
git lfs pull
```

### 3. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the App
```bash
# Run in background using nohup
nohup streamlit run app.py --server.port 80 --server.address 0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false &
```
*(Note: Running on port 80 requires sudo or special permissions. Alternatively, use port 8501 and open it in your Security Group).*
