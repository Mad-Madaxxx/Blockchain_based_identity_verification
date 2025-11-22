"""
Flask Backend API for Blockchain Identity Verification System
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time
import os
from backend.blockchain import Blockchain
from backend.identity import IdentityManager
from backend.credential import CredentialManager
from backend.blockchain import Transaction

# Get the directory where this file is located
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)

# Initialize core components
blockchain = Blockchain()
identity_manager = IdentityManager()
credential_manager = CredentialManager(blockchain, identity_manager)


# ==================== Identity Management Endpoints ====================

@app.route('/api/identity/create', methods=['POST'])
def create_identity():
    """Create a new identity"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        role = data.get('role', 'user')
        
        if not name or not email:
            return jsonify({'error': 'Name and email are required'}), 400
        
        identity = identity_manager.create_identity(name, email, role)
        
        # Create blockchain transaction for identity creation
        transaction = Transaction(
            transaction_type='identity_creation',
            data={
                'did': identity['did'],
                'name': name,
                'email': email,
                'role': role
            },
            timestamp=time.time()
        )
        blockchain.add_transaction(transaction)
        
        # Return identity (including private key for demo purposes)
        response_identity = identity.copy()
        
        return jsonify({
            'success': True,
            'identity': response_identity
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/identity/<did>', methods=['GET'])
def get_identity(did):
    """Get identity by DID"""
    identity = identity_manager.get_identity(did)
    if not identity:
        return jsonify({'error': 'Identity not found'}), 404
    
    # Don't expose private key in GET request
    response_identity = identity.copy()
    response_identity.pop('private_key', None)
    
    return jsonify(response_identity), 200


# ==================== Credential Management Endpoints ====================

@app.route('/api/credential/issue', methods=['POST'])
def issue_credential():
    """Issue a credential"""
    try:
        data = request.json
        issuer_did = data.get('issuer_did')
        recipient_did = data.get('recipient_did')
        credential_type = data.get('credential_type')
        credential_data = data.get('credential_data')
        
        if not all([issuer_did, recipient_did, credential_type, credential_data]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        credential = credential_manager.issue_credential(
            issuer_did,
            recipient_did,
            credential_type,
            credential_data
        )
        
        return jsonify({
            'success': True,
            'credential': credential
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/credential/verify/<credential_id>', methods=['POST'])
def verify_credential(credential_id):
    """Verify a credential"""
    try:
        data = request.json or {}
        verifier_did = data.get('verifier_did')
        
        result = credential_manager.verify_credential(credential_id, verifier_did)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/credential/recipient/<recipient_did>', methods=['GET'])
def get_recipient_credentials(recipient_did):
    """Get all credentials for a recipient"""
    credentials = credential_manager.get_credentials_by_recipient(recipient_did)
    return jsonify({
        'success': True,
        'credentials': credentials
    }), 200


@app.route('/api/credential/issuer/<issuer_did>', methods=['GET'])
def get_issuer_credentials(issuer_did):
    """Get all credentials issued by an issuer"""
    credentials = credential_manager.get_credentials_by_issuer(issuer_did)
    return jsonify({
        'success': True,
        'credentials': credentials
    }), 200


# ==================== Blockchain Endpoints ====================

@app.route('/api/blockchain/mine', methods=['POST'])
def mine_block():
    """Mine pending transactions"""
    try:
        block = blockchain.mine_pending_transactions()
        if not block:
            return jsonify({'message': 'No pending transactions to mine'}), 200
        
        return jsonify({
            'success': True,
            'message': 'Block mined successfully',
            'block': block.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blockchain/chain', methods=['GET'])
def get_chain():
    """Get the entire blockchain"""
    return jsonify({
        'chain': blockchain.get_chain(),
        'length': len(blockchain.chain),
        'valid': blockchain.is_chain_valid()
    }), 200


@app.route('/api/blockchain/status', methods=['GET'])
def get_blockchain_status():
    """Get blockchain status"""
    return jsonify({
        'chain_length': len(blockchain.chain),
        'pending_transactions': len(blockchain.pending_transactions),
        'is_valid': blockchain.is_chain_valid(),
        'difficulty': blockchain.difficulty
    }), 200


# ==================== Frontend Routes ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/create-identity')
def create_identity_page():
    """Create identity page"""
    return render_template('create_identity.html')


@app.route('/issue-credential')
def issue_credential_page():
    """Issue credential page"""
    return render_template('issue_credential.html')


@app.route('/verify-credential')
def verify_credential_page():
    """Verify credential page"""
    return render_template('verify_credential.html')


@app.route('/view-credentials')
def view_credentials_page():
    """View credentials page"""
    return render_template('view_credentials.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

