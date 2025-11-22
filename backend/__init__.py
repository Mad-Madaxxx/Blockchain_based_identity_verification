"""
Backend package for Blockchain Identity Verification System
"""

from .blockchain import Blockchain, Block, Transaction
from .identity import IdentityManager
from .credential import CredentialManager

__all__ = ['Blockchain', 'Block', 'Transaction', 'IdentityManager', 'CredentialManager']

