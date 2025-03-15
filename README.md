# Augur Frontend Project

This repository contains the Augur Frontend application, a dashboard for visualizing and analyzing data.

## Project Structure

- `Task 1`: System architecture and design documentation
- `Task 2`: Engineering tickets and project planning
- `Task 3`: The main Django application code
- `Task 4`: Deployment scripts and CI/CD configuration

## Deployment

### Continuous Deployment

This project uses GitHub Actions for continuous deployment to Azure App Service. The workflow automatically builds and deploys the application when changes are pushed to the main branch.

#### GitHub Actions Workflow

The GitHub Actions workflow is defined in `.github/workflows/azure-deploy.yml` and includes the following steps:

1. Setting up the Python environment
2. Installing dependencies
3. Running tests
4. Collecting static files
5. Creating a deployment package
6. Deploying to Azure App Service

#### Manual Deployment

To manually deploy the application, use the `deploy.py` script in the Task 4 directory:

```bash
python deploy.py --env [dev|staging|production] --collect-static --run-tests
```

### Azure Credentials

To use the GitHub Actions workflow, you need to set up Azure credentials as a GitHub secret named `AZURE_CREDENTIALS`. You can generate these credentials using the Azure CLI:

```bash
az ad sp create-for-rbac --name "AugurGitHubActions" --role contributor \
                          --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
                          --sdk-auth
```

Copy the JSON output and add it as a secret in your GitHub repository settings.