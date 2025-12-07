# CI/CD Pipeline Documentation

## Overview
This repository has been configured with custom GitHub Actions workflows to automate code quality checks, testing, and validation processes for both backend (Django) and frontend (Vue.js) components.

## Workflow Files

### 1. Backend CI (`backend-ci.yml`)
**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Only when files in `SystemScoutsApi/` or `requirements.txt` change

**Jobs:**
- **lint-and-test**: Runs Python linting and tests
  - Sets up Python 3.12
  - Installs dependencies from `requirements.txt`
  - Runs flake8 linting (critical errors and style warnings)
  - Configures SQLite database (no MySQL needed)
  - Runs Django migrations
  - Executes test suite

### 2. Frontend CI (`frontend-ci.yml`)
**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Only when files in `SystemScoutsClient/` change

**Jobs:**
- **lint-and-build**: Validates frontend code quality
  - Sets up Node.js 20
  - Installs dependencies via npm ci
  - Runs ESLint checks
  - Validates code formatting with Prettier
  - Builds production bundle with Vite

### 3. Code Quality Check (`code-quality.yml`)
**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs:**
- **backend-quality**: Python code quality analysis
  - Critical error detection with flake8
  - Code style and complexity warnings
  
- **frontend-quality**: JavaScript code quality analysis
  - ESLint validation
  - Prettier formatting check
  
- **security-scan**: Security vulnerability scanning
  - npm audit for frontend dependencies
  - Python safety check for backend dependencies

### 4. Pull Request Checks (`pr-checks.yml`)
**Triggers:**
- Pull requests to `main` or `develop` branches

**Jobs:**
- **validate-pr**: General PR validation
  - Detects merge conflicts
  - Validates commit message format
  - Checks for large files (>5MB warning)
  - Validates project structure
  
- **run-backend-tests**: Full backend test suite
  - Identical to Backend CI workflow
  
- **run-frontend-build**: Full frontend build
  - Identical to Frontend CI workflow

## Key Features

### Automatic Testing
- Backend tests run automatically with SQLite database
- Frontend builds validate all production code paths
- No manual setup required for CI environment

### Code Quality Gates
- **Critical errors** fail the build (syntax errors, undefined variables)
- **Style warnings** are reported but don't fail the build
- Security scans alert for vulnerable dependencies

### Smart Triggers
- Workflows only run when relevant files change
- Path filters prevent unnecessary runs
- Separate jobs can run in parallel

### Database Strategy
- CI uses SQLite (automatically configured)
- No need for MySQL service in CI
- Empty database variables force SQLite fallback

## Local Development

### Run Backend Checks Locally
```bash
cd SystemScoutsApi

# Install flake8 if not already installed
pip install flake8

# Check for critical errors
flake8 . --exclude=venv,migrations --select=E9,F63,F7,F82 --show-source --statistics

# Check for style issues
flake8 . --exclude=venv,migrations --max-line-length=127 --statistics

# Run tests
python manage.py test
```

### Run Frontend Checks Locally
```bash
cd SystemScoutsClient

# Lint code
npm run lint

# Check formatting
npx prettier --check src/

# Build
npm run build
```

## Workflow Status

To check workflow status:
1. Go to the repository on GitHub
2. Click the "Actions" tab
3. View recent workflow runs and their status
4. Click on individual runs to see detailed logs

## Troubleshooting

### Backend Tests Failing
- Ensure `.env` file is not required (CI uses environment variables)
- Check that models don't require MySQL-specific features
- Verify migrations are committed to the repository

### Frontend Build Failing
- Check for missing environment variables in build process
- Ensure all dependencies are in `package.json`
- Verify Vite configuration doesn't reference development-only files

### Linting Failures
- Run `npm run lint` or `flake8` locally before pushing
- Fix critical errors (E9, F63, F7, F82 in Python)
- Address style warnings when possible

## Best Practices

1. **Commit Small Changes**: Easier to debug if CI fails
2. **Run Tests Locally First**: Catch issues before pushing
3. **Keep Dependencies Updated**: Regular security updates
4. **Write Descriptive Commits**: Helps with PR validation
5. **Don't Commit Large Files**: Use `.gitignore` properly

## Future Enhancements

Potential improvements to consider:
- Add code coverage reporting
- Deploy to staging environment automatically
- Add performance testing
- Integrate with Dependabot for dependency updates
- Add automated release tagging
- Implement deployment to production on tag creation

## Notes

- All workflows use Ubuntu latest runner
- Python 3.12 is used for backend
- Node.js 20 is used for frontend
- Caching is enabled for pip and npm for faster runs
- Some jobs allow failures (`continue-on-error: true`) to not block PRs
