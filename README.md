# nginx-test

This repository sets up an Nginx reverse proxy server and a Flask application on an AWS EC2 instance, running in the `eu-central-1` region.

## Prerequisites

- AWS CLI installed and configured
- Terraform installed
- Ansible installed on your local machine
- `wscat` (for Linux) or `websocat` (for macOS) installed if you plan to test WebSocket functionality

## Set Up Nginx Proxy Server on EC2 Instance

### 1. Set up AWS Credentials

1. **Create an IAM user** in AWS with the necessary permissions and generate access keys.
2. **Save the credentials** under `~/.aws/credentials` using the following template, replacing the asterisks with your actual AWS access keys:

    ```ini
    [personal_acc]
    aws_access_key_id     = AKIA***
    aws_secret_access_key = ******
    ```

### 2. Create an SSH Key Pair

1. **Create a key pair** in the EC2 service with the name `test`.
2. **Save the private key** as `~/.ssh/test.pem` and set the correct permissions:

    ```bash
    chmod 600 ~/.ssh/test.pem
    ```

### 3. Launch EC2 Instance with Terraform

1. Navigate to the `terraform` directory:

    ```bash
    cd terraform
    ```

2. Initialize Terraform and apply the configuration:

    ```bash
    terraform init
    terraform apply
    ```

    This will create the EC2 instance with the necessary configuration.

### 4. Configure Nginx and Flask App on the Instance

Once the EC2 instance is running, configure the Nginx proxy and Flask app:

1. Run the following Ansible playbook to copy the configuration files and start the services:

    ```bash
    ansible-playbook -i "$(terraform output -raw nginx_public_ip)," playbook.yml
    ```

### 5. Access the Application

Once the setup is complete, you can access your application via the public IP of the EC2 instance. You can check the IP by running:

```bash
terraform output nginx_public_ip
```

#### General Case:
Visit the EC2 instance's public IP in your browser:

```
http://<public_ip>
```

#### Basic HTTP Authentication:
The `/admin` route is protected by basic HTTP authentication. To access it, use the following URL:

```
http://<public_ip>/admin
```

Login credentials:

- **Username:** admin
- **Password:** passwd

#### WebSocket Support

To interact with the WebSocket functionality, you’ll need to install `wscat` on Linux or `websocat` on macOS.

##### For Linux (using `wscat`):
1. Install `wscat`:

    ```bash
    sudo apt-get install npm
    npm install -g wscat
    ```

2. Use `wscat` to connect to the WebSocket server:

    ```bash
    wscat -c ws://<public_ip>/ws
    ```

##### For macOS (using `websocat`):
1. Install `websocat`:

    ```bash
    brew install websocat
    ```

2. Use `websocat` to connect to the WebSocket server:

    ```bash
    websocat ws://<public_ip>/ws
    ```


## Debugging

If you encounter any issues, here are some helpful commands to troubleshoot:

1. **Manually run the Flask app** to check for issues:

    ```bash
    python3 /home/ubuntu/servers.py
    ```

2. **Check the Flask app status**:

    ```bash
    sudo systemctl status flask-app
    ```

3. **View Nginx error logs**:

    ```bash
    sudo tail -f /var/log/nginx/error.log
    ```

4. **View Nginx access logs**:

    ```bash
    sudo tail -f /var/log/nginx/access.log
    ```