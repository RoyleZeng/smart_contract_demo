from web3 import Web3

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Check if connected
if not w3.is_connected():
    raise Exception("Failed to connect to the Ethereum node")

# Replace with your contract address and ABI
contract_address = '0xC14913846E34ea082711178D6DA60D322CCCAC73'
abi = [
    {
        "inputs": [
            {
                "internalType": "int256",
                "name": "_value",
                "type": "int256"
            }
        ],
        "name": "addValue",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_index",
                "type": "uint256"
            }
        ],
        "name": "deleteValue",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getValues",
        "outputs": [
            {
                "internalType": "int256[]",
                "name": "",
                "type": "int256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Instantiate the contract
contract = w3.eth.contract(address=contract_address, abi=abi)
userAcc = w3.to_checksum_address('0xf3B8fbe988fb34b2D49FFd8AA7105189CF52c562')
userKey = '0xd8099f0f6fc6fe726e332fa80da32ac6292bdab6b02ebd6b8ebbd80c11185f63'

# Set up the account (you need to unlock the account if using a local node)
balance_eth = w3.eth.get_balance(userAcc)
print('ETH:', balance_eth, 'wei')
# # Add a value
# tx_add = contract.functions.addValue(42).build_transaction({
#     'from': account,
#     'nonce': w3.eth.get_transaction_count(account),
#     'gas': 2000000,
#     'gasPrice': w3.to_wei('50', 'gwei')
# })
# signed_tx_add = w3.eth.account.sign_transaction(tx_add, private_key='0x84bf49828eacdcb3c5c02cb8d5645e6378584558793b962b9a5d77006048c377')
# tx_add_hash = w3.eth.send_raw_transaction(signed_tx_add.rawTransaction)
# w3.eth.wait_for_transaction_receipt(tx_add_hash)
#
# # Get values
# values = contract.functions.getValues().call()
# print("Values after adding 42:", values)
#
# # Delete a value
# tx_delete = contract.functions.deleteValue(0).build_transaction({
#     'from': account,
#     'nonce': w3.eth.get_transaction_count(account),
#     'gas': 2000000,
#     'gasPrice': w3.to_wei('50', 'gwei')
# })
# signed_tx_delete = w3.eth.account.sign_transaction(tx_delete, private_key='0x84bf49828eacdcb3c5c02cb8d5645e6378584558793b962b9a5d77006048c377')
# tx_delete_hash = w3.eth.send_raw_transaction(signed_tx_delete.rawTransaction)
# w3.eth.wait_for_transaction_receipt(tx_delete_hash)
#
# # Get values again
# values = contract.functions.getValues().call()
# print("Values after deleting index 0:", values)