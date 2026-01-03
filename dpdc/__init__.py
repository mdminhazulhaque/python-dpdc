"""
DPDC Prepaid Python Client

A Python package for interacting with Dhaka Power Distribution Company Limited (DPDC)
prepaid electricity account API endpoints.

Example:
    >>> from dpdc import DpdcPrepaid
    >>> client = DpdcPrepaid("your_customer_number")
    >>> balance = client.get_balance()
    >>> print(balance)
"""

from .dpdc import DpdcPrepaid

# Version will be updated by GitHub Actions during release
__version__ = "1.0.0"
__author__ = "Md Minhazul Haque"
__email__ = "mdminhazulhaque@gmail.com"

__all__ = ["DpdcPrepaid"]
