"""Jupiter/Solana transfer operations"""
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.message import Message
from solana.rpc.commitment import Processed
from solana.rpc.types import TxOpts
from spl.token.instructions import transfer_checked, TransferCheckedParams, get_associated_token_address, create_associated_token_account
from spl.token.constants import TOKEN_PROGRAM_ID
from .helper.client import get_client, get_keypair
from .balance import get_sol_balance, get_token_balance
from main.shared.data import get_token_info
from main.Bybit.transfers import get_deposit_address

def send_sol(destination, amount):
    """Send native SOL to a destination"""
    keypair = get_keypair()
    client = get_client()
    balance = get_sol_balance()
    required = amount + 0.00001
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

def send_token(mint_address, destination, amount, decimals):
    """Send SPL token to a destination"""
    keypair = get_keypair()
    client = get_client()
    mint_pubkey = Pubkey.from_string(mint_address)
    dest_pubkey = Pubkey.from_string(destination)
    source_ata = get_associated_token_address(keypair.pubkey(), mint_pubkey)
    dest_ata = get_associated_token_address(dest_pubkey, mint_pubkey)
    
    instructions = []
    
    # Check if destination ATA exists, create if not
    try:
        account_info = client.get_account_info(dest_ata)
        if account_info.value is None:
            print(f"📦 Creating ATA for destination...")
            create_ata_ix = create_associated_token_account(
                payer=keypair.pubkey(),
                owner=dest_pubkey,
                mint=mint_pubkey
            )
            instructions.append(create_ata_ix)
    except:
        print(f"📦 Creating ATA for destination...")
        create_ata_ix = create_associated_token_account(
            payer=keypair.pubkey(),
            owner=dest_pubkey,
            mint=mint_pubkey
        )
        instructions.append(create_ata_ix)
    
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
    instructions.append(transfer_ix)
    
    recent_blockhash = client.get_latest_blockhash().value.blockhash
    message = Message.new_with_blockhash(instructions, keypair.pubkey(), recent_blockhash)
    transaction = Transaction.new_unsigned(message)
    transaction.sign([keypair], recent_blockhash)
    result = client.send_transaction(transaction, opts=TxOpts(
        skip_preflight=False, preflight_commitment=Processed
    ))
    tx_sig = str(result.value)
    print(f"✅ Token transfer: https://solscan.io/tx/{tx_sig}")
    return tx_sig

def withdraw(symbol, chain="SOL"):
    """Withdraw all available crypto from Jupiter to Bybit"""
    coin = symbol.upper()
    print(f"🔄 Starting withdrawal from Jupiter to Bybit for {coin}...")
    
    # Get balance
    balance = get_token_balance(coin)
    if balance <= 0:
        print(f"❌ No {coin} available in Jupiter wallet")
        return None
    
    print(f"💰 Found {balance} {coin} in Jupiter wallet")
    
    # For SOL, reserve some for transaction fees
    if coin == "SOL":
        fee_reserve = 0.001
        if balance <= fee_reserve:
            print(f"❌ Balance ({balance}) is too low (need > {fee_reserve} SOL for fees)")
            return None
        withdrawal_amount = balance - fee_reserve
        print(f"💰 Withdrawing {withdrawal_amount} SOL (reserving {fee_reserve} SOL for fees)")
    else:
        withdrawal_amount = balance
        sol_balance = get_sol_balance()
        if sol_balance < 0.001:
            print(f"⚠️  Warning: Low SOL balance ({sol_balance}). May not have enough for transaction fees")
    
    # Get Bybit deposit address
    try:
        bybit_address = get_deposit_address(coin, chain)
        print(f"📍 Bybit deposit address: {bybit_address}")
    except Exception as e:
        print(f"❌ Failed to get Bybit deposit address: {e}")
        return None
    
    # Send tokens
    try:
        if coin == "SOL":
            tx_sig = send_sol(bybit_address, withdrawal_amount)
        else:
            token_info = get_token_info(coin)
            if not token_info:
                raise ValueError(f"Token info not found for {coin}")
            tx_sig = send_token(
                token_info["mint"],
                bybit_address,
                withdrawal_amount,
                token_info["decimals"]
            )
        
        print(f"✅ Successfully withdrew {withdrawal_amount} {coin} to Bybit")
        return {
            "coin": coin,
            "balance": balance,
            "amount": withdrawal_amount,
            "address": bybit_address,
            "tx_sig": tx_sig
        }
    except Exception as e:
        print(f"❌ Withdrawal failed: {e}")
        raise
