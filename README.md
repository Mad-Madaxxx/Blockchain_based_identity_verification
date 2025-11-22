# Blockchain Identity Verification System

A simple blockchain-based identity verification system built with Python and Flask. This system allows users to create decentralized identities, issue credentials, and verify credentials without using smart contracts.

## Features

- 🔑 **Decentralized Identity (DID) Creation**: Generate unique identities with cryptographic key pairs
- 📜 **Credential Issuance**: Issue verifiable digital credentials
- ✅ **Credential Verification**: Verify the authenticity of credentials using cryptographic signatures
- ⛓️ **Blockchain Storage**: Store credential hashes on a simple blockchain
- 🎨 **Modern Web Interface**: Beautiful and intuitive frontend for all operations

## Technology Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Cryptography**: RSA key pairs for signing and verification
- **Blockchain**: Simple proof-of-work blockchain implementation

## Project Structure

```
blockchain-identity-verification/
├── backend/
│   ├── __init__.py
│   ├── blockchain.py      # Blockchain implementation
│   ├── identity.py        # Identity management
│   └── credential.py      # Credential management
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── create_identity.html
│   ├── issue_credential.html
│   ├── verify_credential.html
│   └── view_credentials.html
├── static/
│   ├── style.css
│   └── main.js
├── app.py                 # Flask application
├── requirements.txt
└── README.md
```

## Installation

1. **Clone the repository** (if already on GitHub):
   ```bash
   git clone <repository-url>
   cd blockchain-identity-verification
   ```

   **Or if setting up locally first**, see SETUP.md for GitHub linking instructions.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### 1. Create Identity
- Navigate to "Create Identity"
- Enter your name, email, and role
- Save your private key securely (it won't be shown again)

### 2. Issue Credential
- Use an issuer DID to create credentials
- Enter recipient DID, credential type, and data
- Credential will be signed and stored on blockchain

### 3. Verify Credential
- Enter a credential ID to verify
- System checks signature, hash, and blockchain record
- View detailed verification results

### 4. View Credentials
- Enter a DID to view all credentials
- View as recipient or issuer
- See all credential details

## API Endpoints

### Identity Management
- `POST /api/identity/create` - Create a new identity
- `GET /api/identity/<did>` - Get identity by DID

### Credential Management
- `POST /api/credential/issue` - Issue a new credential
- `POST /api/credential/verify/<credential_id>` - Verify a credential
- `GET /api/credential/recipient/<recipient_did>` - Get credentials for recipient
- `GET /api/credential/issuer/<issuer_did>` - Get credentials issued by issuer

### Blockchain
- `POST /api/blockchain/mine` - Mine pending transactions
- `GET /api/blockchain/chain` - Get entire blockchain
- `GET /api/blockchain/status` - Get blockchain status

## How It Works

1. **Identity Creation**: Users generate a Decentralized Identifier (DID) with RSA public/private key pair
2. **Credential Issuance**: Issuers create credentials, sign them with their private key, and hash them
3. **Blockchain Storage**: Credential hashes are stored in blockchain transactions
4. **Verification**: Verifiers check:
   - Cryptographic signature validity
   - Credential hash integrity
   - Blockchain record existence

## Security Features

- RSA 2048-bit key pairs for signing
- SHA-256 hashing for credential integrity
- Cryptographic signature verification
- Blockchain immutability for audit trail

## Notes

- This is a simplified implementation for educational purposes
- Private keys are stored in memory (not recommended for production)
- Blockchain uses simple proof-of-work consensus
- No network/distributed blockchain (single node)

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created as a blockchain identity verification demonstration project.

