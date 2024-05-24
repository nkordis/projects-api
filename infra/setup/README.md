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

If your AWS account requires MFA, make sure your `~/.aws/config` has the `mfa_serial` configured for your profile. Here is an example of what it should look like:

```ini
[profile <profile-name>]
region = us-east-1
mfa_serial = arn:aws:iam::123456789012:mfa/your-mfa-device

Authenticate your terminal session with AWS to allow Terraform to make requests to the AWS API.

```sh
aws-vault exec <profile-name> --duration=12h
```

You will be prompted to enter your MFA token from your MFA device.

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

### 6. Plan Terraform Changes

Generate and review the execution plan for Terraform changes.

```sh
docker compose run --rm terraform -chdir=setup plan
```

### 7. Apply Terraform Configuration

Apply the Terraform configuration to create the defined infrastructure.

```sh
docker compose run --rm terraform -chdir=setup apply
```



