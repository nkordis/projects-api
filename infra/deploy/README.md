# Terraform Deploy and Initialization

This README provides step-by-step instructions for setting up and running Terraform commands for the deploy process using Docker Compose and `aws-vault` for managing AWS credentials.

## Prerequisites

- Docker and Docker Compose installed
- `aws-vault` installed and configured
- AWS credentials configured in `aws-vault`

### 1. Navigate to the deploy Directory

Open your terminal and navigate to the deploy directory.

```sh
cd projects-api/infra/deploy
```

### 2. Authenticate with AWS Using aws-vault

Authenticate your terminal session with AWS to allow Terraform to make requests to the AWS API.

```sh
aws-vault exec <profile-name> --duration=8h
```

### 3. Initialize Terraform

Initialize the Terraform deploy using Docker Compose.

```sh
docker compose run --rm terraform -chdir=deploy init
```

### 4. Format Terraform Code

Format your Terraform code to ensure consistency.

```sh
docker compose run --rm terraform -chdir=deploy fmt
```

### 5. Validate Terraform Configuration

Validate the Terraform configuration to ensure it is correct.

```sh
docker compose run --rm terraform -chdir=deploy validate
```
