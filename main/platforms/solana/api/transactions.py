"""
Solana transaction operations
"""
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.message import Message
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from spl.token.instructions import transfer_checked, TransferCheckedParams, get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID
from .client import get_client, get_keypair
from .wallet import get_sol_balance


def send_sol(destination: str, amount: float) -> str:
    """Send native SOL to a destination
    
    Args:
        destination: Destination address
        amount: Amount in SOL
        
    Returns:
        str: Transaction signature
        
    Raises:
        ValueError: If insufficient balance
    """
    keypair = get_keypair()
    client = get_client()
    
    # Check balance
    balance = get_sol_balance()
    required = amount + 0.00001  # Buffer for fees
    if balance < required:
        raise ValueError(f"Insufficient balance! Have {balance:.6f} SOL, need {required:.6f} SOL")
    
    dest_pubkey = Pubkey.from_string(destination)
    lamports = int(amount * 1e9)
    
    transfer_ix = transfer(TransferParams(
        from_pubkey=keypair.pubkey(),
        to_pubkey=dest_pubkey,
        lamports=lamports
    ))
    
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = Message.new_with_blockhash([transfer_ix], keypair.pubkey(), recent_blockhash)
    transaction = Transaction.new_unsigned(message)
    transaction.sign([keypair], recent_blockhash)
    
    result = client.send_transaction(transaction, opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    
    tx_sig = str(result.value)
    print(f"✅ SOL transfer: https://solscan.io/tx/{tx_sig}")
    return tx_sig


def send_token(mint_address: str, destination: str, amount: float, decimals: int) -> str:
    """Send SPL token to a destination
    
    Args:
        mint_address: Token mint address
        destination: Destination address
        amount: Amount in token units
        decimals: Token decimals
        
    Returns:
        str: Transaction signature
    """
    keypair = get_keypair()
    client = get_client()
    
    mint_pubkey = Pubkey.from_string(mint_address)
    dest_pubkey = Pubkey.from_string(destination)
    source_ata = get_associated_token_address(keypair.pubkey(), mint_pubkey)
    dest_ata = get_associated_token_address(dest_pubkey, mint_pubkey)
    amount_lamports = int(amount * (10 ** decimals))
    
    transfer_ix = transfer_checked(TransferCheckedParams(
        program_id=TOKEN_PROGRAM_ID,
        source=source_ata,
        mint=mint_pubkey,
        dest=dest_ata,
        owner=keypair.pubkey(),
        amount=amount_lamports,
        decimals=decimals
    ))
    
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = Message.new_with_blockhash([transfer_ix], keypair.pubkey(), recent_blockhash)
    transaction = Transaction.new_unsigned(message)
    transaction.sign([keypair], recent_blockhash)
    
    result = client.send_transaction(transaction, opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    
    tx_sig = str(result.value)
    print(f"✅ Token transfer: https://solscan.io/tx/{tx_sig}")
    return tx_sig

