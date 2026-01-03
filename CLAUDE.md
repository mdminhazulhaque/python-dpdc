# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI tool for interacting with Dhaka Power Distribution Company Limited (DPDC) prepaid electricity account APIs. Unlike the sibling projects, this tool uses **GraphQL** for API communication and requires **two-step authentication** (token generation + authenticated queries).

## Architecture

### Core Components

**dpdc/dpdc.py** - GraphQL API Client Layer
- `DpdcPrepaid` class handles GraphQL communication with DPDC endpoints
- **Two-step authentication**:
  1. POST to `/auth/login/generate-bearer` with client credentials → get bearer token
  2. Use token in subsequent GraphQL queries
- Auth URL: `https://amiapp.dpdc.org.bd/auth/login/generate-bearer`
- Usage URL: `https://amiapp.dpdc.org.bd/usage/usage-service`
- Token cached in `_access_token` instance variable (reused across requests)
- Type hints throughout using `typing` module

**dpdc/main.py** - CLI Layer
- Click-based CLI using decorator pattern (`@app.command(name="...")`)
- Commands use `--customernumber` / `-c` option (STRING type)
- Error handling through `handle_api_error` decorator wrapper
- Entry point: `app()` function mapped to `dpdc-cli` in pyproject.toml
- Uses tabulate for formatted output display

**dpdc/__init__.py** - Package Entry Point
- Exports `DpdcPrepaid` class for programmatic use
- Version controlled by GitHub Actions during release (format: `1.{run_number}.0`)

### Authentication Flow

1. **Generate Bearer Token**:
   - POST to `AUTH_URL` with headers: `clientId`, `clientSecret`, `tenantCode`
   - Empty JSON body `{}`
   - Extract `access_token` from response
   - Cache token in `_access_token` for subsequent requests

2. **Make GraphQL Query**:
   - POST to `USAGE_URL` with headers: `Authorization: Bearer {token}`, `accesstoken`, `tenantCode`
   - JSON payload: `{"query": "..."}`
   - Parse response from `response['data']`

### GraphQL Query Structure

Balance query example:
```graphql
query {
  postBalanceDetails(input: {
    customerNumber: "CUSTOMER_NUMBER",
    tenantCode: "DPDC"
  }) {
    accountId
    customerName
    customerClass
    mobileNumber
    emailId
    accountType
    balanceRemaining
    connectionStatus
    customerType
    minRecharge
  }
}
```

### Authentication Constants

Hard-coded in `dpdc.py`:
- `CLIENT_ID = 'auth-ui'`
- `CLIENT_SECRET = '0yFsAl4nN9jX1GGkgOrvpUxDarf2DT40'`
- `TENANT_CODE = 'DPDC'`

These are required headers for authentication.

## Development Commands

### Setup
```bash
# Install in development mode
pip install -e .

# Or create virtual environment first
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### Testing the CLI
```bash
# Test balance check
dpdc-cli get-balance -c 1234567890

# Test customer info
dpdc-cli get-customer-info -c 1234567890
```

### Building
```bash
# Build distribution packages
python -m pip install build
python -m build

# Output: dist/*.whl and dist/*.tar.gz
```

## Version Management

- Version is defined in `dpdc/__init__.py` as `__version__ = "1.0.0"`
- GitHub Actions workflow (`.github/workflows/pypi.yml`) auto-updates version on push to main
- Version format: `1.{github.run_number}.0`
- Workflow uses sed to replace version string: `sed -i "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" dpdc/__init__.py`

## Publishing

Automated via GitHub Actions on push to main:
1. Version number updated automatically
2. Build artifacts created with `python -m build`
3. Published to PyPI using trusted publisher with OIDC token

Manual workflow dispatch also available via GitHub Actions UI.

## API Response Structure

### Balance Details Response

GraphQL response structure:
```json
{
  "data": {
    "postBalanceDetails": {
      "accountId": "1234567890",
      "customerName": "MD. JOHN DOE",
      "customerClass": "Residential",
      "mobileNumber": "01712345678",
      "emailId": "customer@example.com",
      "accountType": "Prepaid",
      "balanceRemaining": 1250.50,
      "connectionStatus": "Active",
      "customerType": "Domestic",
      "minRecharge": 100
    }
  }
}
```

Returns `List[List[str]]` of `[key, value]` pairs for all fields.

### Customer Info

Uses same `postBalanceDetails` query - no separate endpoint.
Both `get_balance()` and `get_customer_info()` return identical data.

## CLI Design Pattern

Commands using `@app.command(name="...")` decorator pattern:
1. Click decorator defines command with `--customernumber` option (STRING)
2. `@handle_api_error` decorator catches exceptions and exits with error code 1
3. Print status message with emoji
4. Instantiate `DpdcPrepaid(customernumber)`
5. Call API method
6. Format output with tabulate

## Important Notes

- This is part of a multi-repository project with sibling repositories: `python-bpdb`, `python-desco`, and `python-nesco` (similar utility tools for other Bangladesh power companies)
- **Unique architecture**: Only project using GraphQL API
- **Two-step authentication**: Token generation + authenticated queries
- Token caching: `_access_token` cached for request reuse within same instance
- **Hard-coded credentials**: CLIENT_ID and CLIENT_SECRET are in source code (not environment variables)
- Customer number treated as STRING type in CLI
- No SSL verification issues (HTTPS works properly)
- Single GraphQL query returns both balance and customer info
- No separate endpoints for different data types
- Type hints throughout for better IDE support
- Dependencies: Standard set (requests, click, tabulate) - no GraphQL-specific libraries needed
