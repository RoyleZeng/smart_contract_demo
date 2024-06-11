from web3 import Web3
import json

# 连接到以太坊节点
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
account = w3.eth.account.privateKeyToAccount(private_key_hex)
w3.eth.defaultAccount = account.address

# 智能合约ABI和地址
contract_abi = json.loads('''[{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"},{"internalType":"string","name":"data","type":"string"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"address","name":"signer","type":"address"}],"name":"registerProduct","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"productId","type":"uint256"}],"name":"getProduct","outputs":[{"internalType":"string","name":"","type":"string"},{"internalType":"bytes","name":"","type":"bytes"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]''')
contract_address = 'your_contract_address_here'

# 创建合约实例
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 注册产品
product_id = 12345
tx_hash = contract.functions.registerProduct(
    product_id,
    data_json,
    signature.to_bytes(),
    public_key.to_canonical_address()
).transact()

# 等待交易完成
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Transaction receipt: {tx_receipt}")

# 获取产品信息
product_info = contract.functions.getProduct(product_id).call()
print(f"Product Info: {product_info}")
