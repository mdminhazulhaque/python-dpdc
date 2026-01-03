#!/usr/bin/env python3
"""
DPDC Prepaid API Client

A Python client for interacting with Dhaka Power Distribution Company Limited (DPDC)
prepaid electricity account API endpoints using GraphQL.
"""

import requests
from typing import Dict, Any, List


class DpdcPrepaid:
    """
    A client for interacting with DPDC prepaid electricity account API.

    This class provides methods to retrieve account balance and customer information
    for DPDC prepaid accounts using GraphQL queries.
    """

    # API Configuration
    AUTH_URL = 'https://amiapp.dpdc.org.bd/auth/login/generate-bearer'
    USAGE_URL = 'https://amiapp.dpdc.org.bd/usage/usage-service'

    # Authentication headers
    CLIENT_ID = 'auth-ui'
    CLIENT_SECRET = '0yFsAl4nN9jX1GGkgOrvpUxDarf2DT40'
    TENANT_CODE = 'DPDC'

    def __init__(self, customer_number: str) -> None:
        """
        Initialize the DPDC prepaid client.

        Args:
            customer_number (str): The DPDC prepaid customer number
        """
        self.customer_number = str(customer_number)
        self._access_token = None

    def _get_access_token(self) -> str:
        """
        Get an access token from the DPDC authentication endpoint.

        Returns:
            str: The access token for API requests

        Raises:
            requests.RequestException: If the authentication request fails
        """
        if self._access_token:
            return self._access_token

        headers = {
            'clientId': self.CLIENT_ID,
            'clientSecret': self.CLIENT_SECRET,
            'tenantCode': self.TENANT_CODE,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                self.AUTH_URL,
                headers=headers,
                json={},
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            self._access_token = data.get('access_token')

            if not self._access_token:
                raise requests.RequestException("Failed to get access token from response")

            return self._access_token

        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to authenticate with DPDC API: {e}")

    def _make_graphql_request(self, query: str) -> Dict[str, Any]:
        """
        Make a GraphQL request to the DPDC usage service.

        Args:
            query (str): The GraphQL query string

        Returns:
            dict: The JSON response from the API

        Raises:
            requests.RequestException: If the API request fails
        """
        access_token = self._get_access_token()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'accesstoken': access_token,
            'tenantCode': self.TENANT_CODE,
            'Content-Type': 'application/json'
        }

        payload = {'query': query}

        try:
            response = requests.post(
                self.USAGE_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch data from DPDC API: {e}")

    def get_balance(self) -> List[List[str]]:
        """
        Get current account balance and customer information.

        Returns:
            List[List[str]]: A list of [key, value] pairs containing balance and customer information
        """
        query = f"""query{{
            postBalanceDetails(input: {{
                customerNumber: "{self.customer_number}",
                tenantCode: "{self.TENANT_CODE}"
            }}) {{
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
            }}
        }}"""

        response = self._make_graphql_request(query)

        data = []
        if 'data' in response and 'postBalanceDetails' in response['data']:
            balance_details = response['data']['postBalanceDetails']
            for key, value in balance_details.items():
                data.append([key, str(value) if value is not None else ''])

        return data

    def get_customer_info(self) -> List[List[str]]:
        """
        Get detailed customer information.

        This method returns the same data as get_balance() since the DPDC API
        combines balance and customer information in a single query.

        Returns:
            List[List[str]]: A list of [key, value] pairs containing customer information
        """
        return self.get_balance()
