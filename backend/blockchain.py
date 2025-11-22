"""
Simple Blockchain Implementation for Identity Verification
Stores credential hashes and identity records without smart contracts
"""

import hashlib
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    """Represents a transaction on the blockchain"""
    transaction_type: str  # 'identity_creation', 'credential_issuance', 'credential_verification'
    data: Dict[str, Any]
    timestamp: float
    signature: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary for hashing"""
        return {
            'transaction_type': self.transaction_type,
            'data': self.data,
            'timestamp': self.timestamp
        }
    
    def hash(self) -> str:
        """Generate hash of transaction"""
        transaction_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()


@dataclass
class Block:
    """Represents a block in the blockchain"""
    index: int
    previous_hash: str
    transactions: List[Transaction]
    timestamp: float
    merkle_root: str = ""
    nonce: int = 0
    hash: str = ""
    
    def calculate_merkle_root(self) -> str:
        """Calculate Merkle root of transactions"""
        if not self.transactions:
            return ""
        
        # Convert transactions to hashes
        transaction_hashes = [tx.hash() for tx in self.transactions]
        
        # Build Merkle tree
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 == 1:
                transaction_hashes.append(transaction_hashes[-1])
            
            new_level = []
            for i in range(0, len(transaction_hashes), 2):
                combined = transaction_hashes[i] + transaction_hashes[i + 1]
                new_level.append(hashlib.sha256(combined.encode()).hexdigest())
            transaction_hashes = new_level
        
        return transaction_hashes[0] if transaction_hashes else ""
    
    def calculate_hash(self) -> str:
        """Calculate hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'previous_hash': self.previous_hash,
            'merkle_root': self.merkle_root,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2) -> None:
        """Mine the block with proof of work"""
        self.merkle_root = self.calculate_merkle_root()
        prefix = '0' * difficulty
        
        while not self.hash.startswith(prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'transactions': [asdict(tx) for tx in self.transactions],
            'timestamp': self.timestamp,
            'merkle_root': self.merkle_root,
            'nonce': self.nonce,
            'hash': self.hash
        }


class Blockchain:
    """Simple blockchain implementation for identity verification"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = 2
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis_transaction = Transaction(
            transaction_type='genesis',
            data={'message': 'Genesis block for Identity Verification System'},
            timestamp=time.time()
        )
        genesis_block = Block(
            index=0,
            previous_hash='0' * 64,
            transactions=[genesis_transaction],
            timestamp=time.time()
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the latest block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to pending transactions"""
        self.pending_transactions.append(transaction)
    
    def mine_pending_transactions(self) -> Block:
        """Mine pending transactions into a new block"""
        if not self.pending_transactions:
            return None
        
        block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            transactions=self.pending_transactions.copy(),
            timestamp=time.time()
        )
        
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = []
        
        return block
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if block links to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Check if Merkle root is valid
            if current_block.merkle_root != current_block.calculate_merkle_root():
                return False
        
        return True
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """Get the entire chain as a list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Transaction]:
        """Get all transactions of a specific type"""
        transactions = []
        for block in self.chain:
            for tx in block.transactions:
                if tx.transaction_type == transaction_type:
                    transactions.append(tx)
        return transactions
    
    def verify_transaction_exists(self, transaction_hash: str) -> bool:
        """Verify if a transaction exists in the blockchain"""
        for block in self.chain:
            for tx in block.transactions:
                if tx.hash() == transaction_hash:
                    return True
        for tx in self.pending_transactions:
            if tx.hash() == transaction_hash:
                return True
        return False

