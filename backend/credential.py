"""
Credential Management System
Handles issuance, verification, and storage of digital credentials
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from .identity import IdentityManager
from .blockchain import Blockchain, Transaction


class CredentialManager:
    """Manages digital credentials and their verification"""
    
    def __init__(self, blockchain: Blockchain, identity_manager: IdentityManager):
        self.blockchain = blockchain
        self.identity_manager = identity_manager
        self.credentials: Dict[str, Dict[str, Any]] = {}
    
    def issue_credential(
        self,
        issuer_did: str,
        recipient_did: str,
        credential_type: str,
        credential_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Issue a new credential"""
        # Verify issuer exists
        issuer = self.identity_manager.get_identity(issuer_did)
        if not issuer:
            raise ValueError(f"Issuer with DID {issuer_did} not found")
        
        # Verify recipient exists
        recipient = self.identity_manager.get_identity(recipient_did)
        if not recipient:
            raise ValueError(f"Recipient with DID {recipient_did} not found")
        
        # Generate credential ID
        credential_id = str(uuid.uuid4())
        
        # Create credential
        credential = {
            'credential_id': credential_id,
            'issuer_did': issuer_did,
            'issuer_name': issuer['name'],
            'recipient_did': recipient_did,
            'recipient_name': recipient['name'],
            'credential_type': credential_type,
            'credential_data': credential_data,
            'issued_at': time.time(),
            'status': 'active'
        }
        
        # Sign credential with issuer's private key
        credential_to_sign = {
            'credential_id': credential_id,
            'issuer_did': issuer_did,
            'recipient_did': recipient_did,
            'credential_type': credential_type,
            'credential_data': credential_data,
            'issued_at': credential['issued_at']
        }
        
        signature = self.identity_manager.sign_data(
            credential_to_sign,
            issuer['private_key']
        )
        credential['signature'] = signature
        
        # Hash credential for blockchain storage
        credential_hash = self.identity_manager.hash_credential(credential_to_sign)
        credential['credential_hash'] = credential_hash
        
        # Store credential
        self.credentials[credential_id] = credential
        
        # Create blockchain transaction
        transaction = Transaction(
            transaction_type='credential_issuance',
            data={
                'credential_id': credential_id,
                'credential_hash': credential_hash,
                'issuer_did': issuer_did,
                'recipient_did': recipient_did,
                'credential_type': credential_type
            },
            timestamp=time.time()
        )
        credential['transaction_hash'] = transaction.hash()
        self.blockchain.add_transaction(transaction)
        
        return credential
    
    def verify_credential(self, credential_id: str, verifier_did: Optional[str] = None) -> Dict[str, Any]:
        """Verify a credential"""
        # Get credential
        credential = self.credentials.get(credential_id)
        if not credential:
            return {
                'valid': False,
                'error': 'Credential not found'
            }
        
        # Get issuer
        issuer = self.identity_manager.get_identity(credential['issuer_did'])
        if not issuer:
            return {
                'valid': False,
                'error': 'Issuer not found'
            }
        
        # Reconstruct credential data for verification
        credential_to_verify = {
            'credential_id': credential['credential_id'],
            'issuer_did': credential['issuer_did'],
            'recipient_did': credential['recipient_did'],
            'credential_type': credential['credential_type'],
            'credential_data': credential['credential_data'],
            'issued_at': credential['issued_at']
        }
        
        # Verify signature
        signature_valid = self.identity_manager.verify_signature(
            credential_to_verify,
            credential['signature'],
            issuer['public_key']
        )
        
        # Verify credential hash matches
        expected_hash = self.identity_manager.hash_credential(credential_to_verify)
        hash_valid = credential['credential_hash'] == expected_hash
        
        # Verify credential exists in blockchain
        transaction_hash = credential.get('transaction_hash')
        if transaction_hash:
            blockchain_valid = self.blockchain.verify_transaction_exists(transaction_hash)
        else:
            blockchain_valid = False
            for block in self.blockchain.chain:
                for tx in block.transactions:
                    if (
                        tx.transaction_type == 'credential_issuance'
                        and tx.data.get('credential_id') == credential['credential_id']
                        and tx.data.get('credential_hash') == credential['credential_hash']
                    ):
                        blockchain_valid = True
                        break
                if blockchain_valid:
                    break
            if not blockchain_valid:
                for tx in self.blockchain.pending_transactions:
                    if (
                        tx.transaction_type == 'credential_issuance'
                        and tx.data.get('credential_id') == credential['credential_id']
                        and tx.data.get('credential_hash') == credential['credential_hash']
                    ):
                        blockchain_valid = True
                        break
        
        # Overall verification result
        is_valid = signature_valid and hash_valid and blockchain_valid
        
        return {
            'valid': is_valid,
            'credential_id': credential_id,
            'credential_type': credential['credential_type'],
            'issuer': credential['issuer_name'],
            'recipient': credential['recipient_name'],
            'issued_at': credential['issued_at'],
            'signature_valid': signature_valid,
            'hash_valid': hash_valid,
            'blockchain_valid': blockchain_valid,
            'status': credential['status']
        }
    
    def get_credentials_by_recipient(self, recipient_did: str) -> List[Dict[str, Any]]:
        """Get all credentials for a recipient"""
        return [
            cred for cred in self.credentials.values()
            if cred['recipient_did'] == recipient_did
        ]
    
    def get_credentials_by_issuer(self, issuer_did: str) -> List[Dict[str, Any]]:
        """Get all credentials issued by an issuer"""
        return [
            cred for cred in self.credentials.values()
            if cred['issuer_did'] == issuer_did
        ]
    
    def get_credential(self, credential_id: str) -> Optional[Dict[str, Any]]:
        """Get credential by ID"""
        return self.credentials.get(credential_id)

