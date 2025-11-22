"""
Identity Management System
Handles Decentralized Identifiers (DIDs), key generation, and cryptographic signatures
"""

import hashlib
import json
import time
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64


class IdentityManager:
    """Manages decentralized identities and cryptographic operations"""
    
    def __init__(self):
        self.identities: Dict[str, Dict[str, Any]] = {}
    
    def generate_did(self) -> str:
        """Generate a new Decentralized Identifier (DID)"""
        # Simple DID format: did:identity:hash
        random_data = str(time.time()) + str(hash(time.time()))
        did_hash = hashlib.sha256(random_data.encode()).hexdigest()[:16]
        return f"did:identity:{did_hash}"
    
    def generate_key_pair(self) -> tuple:
        """Generate RSA key pair for signing"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key
    
    def serialize_private_key(self, private_key) -> str:
        """Serialize private key to PEM format string"""
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem.decode('utf-8')
    
    def serialize_public_key(self, public_key) -> str:
        """Serialize public key to PEM format string"""
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    
    def deserialize_private_key(self, pem_string: str):
        """Deserialize private key from PEM format string"""
        return serialization.load_pem_private_key(
            pem_string.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
    
    def deserialize_public_key(self, pem_string: str):
        """Deserialize public key from PEM format string"""
        return serialization.load_pem_public_key(
            pem_string.encode('utf-8'),
            backend=default_backend()
        )
    
    def create_identity(self, name: str, email: str, role: str = "user") -> Dict[str, Any]:
        """Create a new identity with DID and key pair"""
        did = self.generate_did()
        private_key, public_key = self.generate_key_pair()
        
        identity = {
            'did': did,
            'name': name,
            'email': email,
            'role': role,
            'public_key': self.serialize_public_key(public_key),
            'private_key': self.serialize_private_key(private_key),
            'created_at': time.time()
        }
        
        self.identities[did] = identity
        return identity
    
    def sign_data(self, data: Dict[str, Any], private_key_pem: str) -> str:
        """Sign data with private key"""
        private_key = self.deserialize_private_key(private_key_pem)
        
        # Convert data to string for signing
        data_string = json.dumps(data, sort_keys=True)
        data_bytes = data_string.encode('utf-8')
        
        # Sign the data
        signature = private_key.sign(
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Encode signature as base64
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, data: Dict[str, Any], signature: str, public_key_pem: str) -> bool:
        """Verify signature with public key"""
        try:
            public_key = self.deserialize_public_key(public_key_pem)
            
            # Convert data to string
            data_string = json.dumps(data, sort_keys=True)
            data_bytes = data_string.encode('utf-8')
            
            # Decode signature
            signature_bytes = base64.b64decode(signature)
            
            # Verify signature
            public_key.verify(
                signature_bytes,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def get_identity(self, did: str) -> Optional[Dict[str, Any]]:
        """Get identity by DID"""
        return self.identities.get(did)
    
    def hash_credential(self, credential_data: Dict[str, Any]) -> str:
        """Generate hash of credential data"""
        credential_string = json.dumps(credential_data, sort_keys=True)
        return hashlib.sha256(credential_string.encode()).hexdigest()

