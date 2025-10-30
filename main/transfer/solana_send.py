import os
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.message import Message
from solana.rpc.api import Client
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from spl.token.instructions import transfer_checked, TransferCheckedParams, get_associated_token_address
from spl.token.constants import TOKEN_PROGRAM_ID
from .solana_wallet import get_sol_balance

load_dotenv()


def send_native_sol(destination_address, amount):
    """Send native SOL to a destination address
    
    Args:
        destination_address: Recipient's Solana address
        amount: Amount of SOL to send
        
    Returns:
        str: Transaction signature
    """
    keypair = Keypair.from_base58_string(os.getenv("SOLANA_PRIVATE_KEY"))
    client = Client("https://api.mainnet-beta.solana.com")
    
    # Check balance
    balance = get_sol_balance(keypair, client)
    print(f"💰 Current balance: {balance:.6f} SOL")
    
    # Add buffer for transaction fees (typically ~0.000005 SOL)
    required = amount + 0.00001
    if balance < required:
        raise ValueError(f"Insufficient balance! Have {balance:.6f} SOL, need at least {required:.6f} SOL (including fees)")
    
    dest_pubkey = Pubkey.from_string(destination_address)
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
    print(f"✅ Transfer sent: https://solscan.io/tx/{tx_sig}")
    return tx_sig


def send_spl_token(token_mint, destination_address, amount, decimals):
    """Send SPL token to a destination address
    
    Args:
        token_mint: Token mint address
        destination_address: Recipient's Solana address
        amount: Amount of tokens to send
        decimals: Token decimals
        
    Returns:
        str: Transaction signature
    """
    keypair = Keypair.from_base58_string(os.getenv("SOLANA_PRIVATE_KEY"))
    client = Client("https://api.mainnet-beta.solana.com")
    
    mint_pubkey = Pubkey.from_string(token_mint)
    dest_pubkey = Pubkey.from_string(destination_address)
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
    print(f"✅ Transfer sent: https://solscan.io/tx/{tx_sig}")
    return tx_sig

