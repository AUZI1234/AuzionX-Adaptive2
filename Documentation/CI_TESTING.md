# CI Testing Workflow

## Research Tests Workflow

The `research-tests.yml` GitHub Actions workflow automatically runs research unit tests to validate the research module functionality across multiple Python versions.

### Trigger Events

The workflow runs automatically on:

- **Push**: Triggered when code is pushed to `main`, `develop`, or `architecture-review` branches
- **Pull Request**: Triggered on pull requests targeting `main` or `develop` branches
- **Manual Dispatch**: Can be manually triggered via the GitHub Actions UI using `workflow_dispatch`

### What It Does

1. **Environment Setup**
   - Runs on `ubuntu-latest`
   - Tests across Python 3.9, 3.10, and 3.11 using a matrix strategy

2. **Dependency Installation**
   - Upgrades pip
   - Installs dependencies from `requirements.txt` (if present)
   - Installs development dependencies from `requirements-dev.txt` (if present)

3. **Test Execution**
   - Runs: `python -m unittest discover -s Tests/research -p 'test_*.py' -v`
   - Discovers all test files matching the pattern `test_*.py` in the `Tests/research` directory
   - Executes tests in verbose mode for detailed output

### Test Discovery

The workflow uses Python's unittest discovery module to automatically find and run tests:

- **Search Directory**: `Tests/research/`
- **File Pattern**: `test_*.py`
- **Execution**: All matching test files are discovered and executed automatically

### Workflow File

**Location**: `.github/workflows/research-tests.yml`

**Key Configuration**:
- Matrix strategy for multi-version Python testing
- Conditional dependency installation (checks for requirements files before installing)
- Verbose test output for better diagnostics

### Monitoring Test Results

After pushing or creating a pull request:

1. Navigate to the repository's **Actions** tab
2. Find the "Research Tests" workflow run
3. Check the status:
   - ✅ **Success**: All tests passed across all Python versions
   - ❌ **Failure**: Review logs to identify failing tests
   - ⏳ **In Progress**: Workflow is currently running

### Local Development

To run tests locally before pushing:

```bash
python -m unittest discover -s Tests/research -p 'test_*.py' -v
```

Or for a specific test file:

```bash
python -m unittest Tests.research.test_module_name
```

### Troubleshooting

**Workflow Not Running?**
- Verify the workflow file is in `.github/workflows/research-tests.yml`
- Check that branches match the trigger configuration (push: main/develop/architecture-review, PR: main/develop)

**Tests Fail in CI but Pass Locally?**
- Verify Python version compatibility (workflow tests 3.9, 3.10, 3.11)
- Check that all dependencies are listed in `requirements.txt` or `requirements-dev.txt`
- Ensure test paths and imports are correct for the GitHub Actions environment

**No Dependencies Found?**
- The workflow gracefully continues if `requirements.txt` or `requirements-dev.txt` don't exist
- Add these files if your tests have external dependencies

### Future Enhancements

Potential improvements to the workflow:

- Add code coverage reporting and thresholds
- Cache dependencies for faster subsequent runs
- Add linting and code quality checks
- Generate test reports and artifacts
- Notify on failures via Slack or other integrations
