# Terraform Setup and Initialization

This README provides step-by-step instructions for setting up and running Terraform commands for the setup process using Docker Compose and `aws-vault` for managing AWS credentials.

## Prerequisites

- Docker and Docker Compose installed
- `aws-vault` installed and configured
- AWS credentials configured in `aws-vault`

### 1. Navigate to the Setup Directory

Open your terminal and navigate to the setup directory.

```sh
cd projects-api/infra/setup
```

### 2. Authenticate with AWS Using aws-vault

Authenticate your terminal session with AWS to allow Terraform to make requests to the AWS API.

```sh
aws-vault exec <profile-name> --duration=8h
```

### 3. Initialize Terraform

Initialize the Terraform setup using Docker Compose.

```sh
docker compose run --rm terraform -chdir=setup init
```

### 4. Format Terraform Code

Format your Terraform code to ensure consistency.

```sh
docker compose run --rm terraform -chdir=setup fmt
```

### 5. Validate Terraform Configuration

Validate the Terraform configuration to ensure it is correct.

```sh
docker compose run --rm terraform -chdir=setup validate
```





