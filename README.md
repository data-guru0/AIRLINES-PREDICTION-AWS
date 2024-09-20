

# Deploying Streamlit App on AWS EC2

This guide walks you through the steps of deploying a Streamlit app on an AWS EC2 instance.

## Prerequisites

1. **AWS Account:** Ensure you have an AWS account to access EC2 instances.
2. **Git Repository:** Ensure your Streamlit app is hosted on a Git repository (e.g., GitHub).
3. **AWS EC2 Instance:** Launch an EC2 instance, preferably with Ubuntu.

## Deployment Steps

### 1. Launch an EC2 Instance

1. **Log in to your AWS Management Console** and navigate to the **EC2 Dashboard**.
2. **Launch a new EC2 instance**:
   - Choose an appropriate instance type (e.g., `t2.micro` for free tier).
   - Use **Ubuntu** as the machine image (AMI).
   - Ensure you configure security groups to allow inbound traffic on port `8501` (Streamlit default port).
   
   For port mapping:
   - Add a custom TCP rule to open port `8501` in the security group.
   - Set the source to `0.0.0.0/0` (or restrict it to specific IP addresses).

### 2. Connect to Your EC2 Instance

Once your EC2 instance is running, connect to it via SSH:

```bash
ssh -i path-to-your-key.pem ubuntu@your-ec2-public-ip
```

### 3. Install Required Packages

Run the following commands to update the instance and install necessary dependencies:

```bash
# Update package list and upgrade all packages
sudo apt update
sudo apt-get update
sudo apt upgrade -y

# Install essential packages
sudo apt install git curl unzip tar make sudo vim wget -y

# Install Python 3 and pip3 (Python package manager)
sudo apt install python3-pip -y
```

### 4. Clone Your Git Repository

Clone your Streamlit app from your Git repository:

```bash
git clone https://github.com/your-username/your-repository.git
```

Navigate to the project directory:

```bash
cd your-repository
```

### 5. Install Python Dependencies

Install the required Python packages listed in `requirements.txt`:

```bash
# Install virtualenv if you don't have it already
sudo apt install python3-venv

# Create a virtual environment (name it as `venv`)
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Now install your requirements
pip install -r requirements.txt
```

### 6. Run the Streamlit App

#### Temporary Running

You can run your Streamlit app temporarily using the following command:

```bash
python3 -m streamlit run app.py
```

The app will run at `http://your-ec2-public-ip:8501`.

#### Permanent Running

To keep the app running even after you log out of the SSH session, use `nohup`:

```bash
nohup python3 -m streamlit run app.py &
```

This command will run the Streamlit app in the background and allow it to persist.

### 7. Access the Streamlit App

Open a browser and go to:

```
http://your-ec2-public-ip:8501
```

Ensure that port `8501` is open in your EC2 security group, as described in step 1.

## Notes

- **Port 8501** is the default port for Streamlit apps.
- To stop the background process, use the following command to find the process ID and kill it:

```bash
ps aux | grep streamlit
kill <process-id>
```

---

## Conclusion

Your Streamlit app should now be successfully deployed on an AWS EC2 instance!