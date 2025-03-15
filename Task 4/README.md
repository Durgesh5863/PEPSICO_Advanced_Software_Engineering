# Augur Frontend CI/CD Pipeline

This directory contains the continuous delivery pipeline configurations for the Augur frontend application. The pipelines automatically build and deploy the application to Azure App Service whenever changes are pushed to the main branch.

## Pipeline Components

### 1. GitHub Actions Workflow

The `.github/workflows/azure-deploy.yml` file defines the GitHub Actions workflow with the following steps:

- Setting up the Python environment
- Installing dependencies
- Running tests
- Collecting static files
- Creating a deployment package
- Deploying to Azure App Service

### 2. Azure DevOps Pipeline Configuration

The `azure-pipelines.yml` file defines the CI/CD pipeline with the following stages:

- **Build Stage**: Installs dependencies, runs tests, collects static files, and packages the application
- **Deploy Stage**: Deploys the application to Azure App Service and configures application settings

### 3. Deployment Script

The `deploy.py` script provides a command-line utility for manual deployments with the following features:

- Environment-specific deployments (dev, staging, production)
- Static file collection
- Test execution
- Azure App Service deployment

## Setup Instructions

### Prerequisites

1. GitHub repository with Actions enabled or Azure DevOps account with appropriate permissions
2. Azure subscription with resources provisioned
3. Service connection configured in Azure DevOps or GitHub Secrets configured for GitHub Actions

### Configuration

#### For GitHub Actions

1. Set up Azure credentials as a GitHub secret named `AZURE_CREDENTIALS`. You can generate these credentials using the Azure CLI:

```bash
az ad sp create-for-rbac --name "AugurGitHubActions" --role contributor \
                          --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
                          --sdk-auth
```

2. Copy the JSON output and add it as a secret in your GitHub repository settings.

#### For Azure DevOps

1. Create a service connection in Azure DevOps named `AugurAzureServiceConnection`
2. Create the following Azure resources:
   - Resource Group: `augur-resources`
   - App Service: `augur-dashboard`
   - Deployment slots for staging and production

### Pipeline Variables

#### GitHub Actions Variables

The GitHub Actions workflow uses the following environment variables:

- `PYTHON_VERSION`: Python version to use (default: 3.10)
- `ENVIRONMENT`: Deployment environment (dev, staging, or production)
- `APP_NAME`: Name of the Azure App Service
- `RESOURCE_GROUP`: Name of the Azure Resource Group

#### Azure DevOps Variables

The Azure DevOps pipeline uses the following variables that can be customized:

- `pythonVersion`: Python version to use (default: 3.10)
- `azureServiceConnection`: Name of the Azure service connection
- `webAppName`: Name of the Azure App Service
- `resourceGroupName`: Name of the Azure Resource Group

## Manual Deployment

To manually deploy the application, use the `deploy.py` script:

```bash
python deploy.py --env [dev|staging|production] --collect-static --run-tests
```

## Environments

The pipeline supports the following environments:

- **Development**: For testing new features
- **Staging**: For pre-production validation
- **Production**: For live application

Each environment has its own configuration settings defined in the deployment script.