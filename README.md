# scalable-project
## CI/CD Pipeline

This project uses a CI/CD pipeline for the frontend:

### Continuous Integration (CI)
- Automated through GitHub Actions
- Triggered on every push to the main branch
- Builds and tests the frontend code
- Validates that the code meets quality standards

### Continuous Deployment (CD)
- Semi-automated through a deployment script
- After CI passes, run `./deploy.sh` from the Cloud9 environment
- Builds and deploys the frontend to S3

To deploy a new version:
1. Push your changes to GitHub
2. Wait for the CI workflow to complete (check GitHub Actions tab)
3. Run `./deploy.sh` from Cloud9