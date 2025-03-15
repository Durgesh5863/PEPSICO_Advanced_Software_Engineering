#!/usr/bin/env python
"""
Deployment script for Augur Frontend
This script handles the deployment process for the Augur frontend application.
"""

import os
import sys
import subprocess
import logging
import argparse
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('augur-deploy')

# Define deployment environments
ENVIRONMENTS = {
    'dev': {
        'app_service_name': 'augur-dashboard-dev',
        'resource_group': 'augur-resources-dev',
        'settings': {
            'DEBUG': 'True',
            'ALLOWED_HOSTS': '*.azurewebsites.net',
        }
    },
    'staging': {
        'app_service_name': 'augur-dashboard-staging',
        'resource_group': 'augur-resources-staging',
        'settings': {
            'DEBUG': 'False',
            'ALLOWED_HOSTS': '*.azurewebsites.net',
        }
    },
    'production': {
        'app_service_name': 'augur-dashboard',
        'resource_group': 'augur-resources',
        'settings': {
            'DEBUG': 'False',
            'ALLOWED_HOSTS': '*.azurewebsites.net',
        }
    }
}

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Deploy Augur Frontend to Azure')
    parser.add_argument('--env', choices=['dev', 'staging', 'production'], default='dev',
                        help='Deployment environment')
    parser.add_argument('--collect-static', action='store_true',
                        help='Collect static files before deployment')
    parser.add_argument('--run-tests', action='store_true',
                        help='Run tests before deployment')
    return parser.parse_args()

def collect_static_files(project_dir):
    """Collect static files for Django application"""
    logger.info('Collecting static files...')
    try:
        subprocess.run(
            [sys.executable, 'manage.py', 'collectstatic', '--noinput'],
            cwd=project_dir,
            check=True
        )
        logger.info('Static files collected successfully')
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f'Failed to collect static files: {e}')
        return False

def run_tests(project_dir):
    """Run Django tests"""
    logger.info('Running tests...')
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'test'],
            cwd=project_dir,
            check=False
        )
        if result.returncode == 0:
            logger.info('Tests passed successfully')
            return True
        else:
            logger.error('Tests failed')
            return False
    except Exception as e:
        logger.error(f'Error running tests: {e}')
        return False

def deploy_to_azure(env_config, project_dir):
    """Deploy application to Azure App Service"""
    logger.info(f'Deploying to Azure App Service: {env_config["app_service_name"]}')
    
    # Create app settings JSON file
    settings_path = Path(project_dir) / 'azure_settings.json'
    with open(settings_path, 'w') as f:
        json.dump(env_config['settings'], f)
    
    try:
        # Deploy using Azure CLI
        cmd = [
            'az', 'webapp', 'deployment', 'source', 'config-zip',
            '--resource-group', env_config['resource_group'],
            '--name', env_config['app_service_name'],
            '--src', str(Path(project_dir) / 'deployment.zip')
        ]
        
        subprocess.run(cmd, check=True)
        
        # Update app settings
        settings_cmd = [
            'az', 'webapp', 'config', 'appsettings', 'set',
            '--resource-group', env_config['resource_group'],
            '--name', env_config['app_service_name'],
            '--settings', f'@{settings_path}'
        ]
        
        subprocess.run(settings_cmd, check=True)
        
        logger.info('Deployment completed successfully')
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f'Deployment failed: {e}')
        return False
    finally:
        # Clean up settings file
        if settings_path.exists():
            settings_path.unlink()

def main():
    """Main deployment function"""
    args = parse_arguments()
    env_config = ENVIRONMENTS[args.env]
    
    # Set project directory
    project_dir = Path(__file__).parent.parent / 'Task 3'
    
    # Validate project directory
    if not (project_dir / 'manage.py').exists():
        logger.error(f'Invalid project directory: {project_dir}')
        return 1
    
    # Run tests if requested
    if args.run_tests and not run_tests(project_dir):
        logger.warning('Tests failed, but continuing with deployment')
    
    # Collect static files if requested
    if args.collect_static and not collect_static_files(project_dir):
        logger.error('Failed to collect static files')
        return 1
    
    # Deploy to Azure
    if deploy_to_azure(env_config, project_dir):
        logger.info(f'Successfully deployed to {args.env} environment')
        return 0
    else:
        logger.error(f'Failed to deploy to {args.env} environment')
        return 1

if __name__ == '__main__':
    sys.exit(main())