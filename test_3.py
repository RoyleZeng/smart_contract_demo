from web3 import Web3
import json

# 連接到本地的以太坊節點（或者替換為你的Infura節點URL）
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

with open("ABI.json") as f:
    abi = json.load(f)


contract_address = '0xfeB7294761d7e18Cd2e57Ff2e1C32cF221a4304D'

# 加載合約
contract = w3.eth.contract(address=contract_address, abi=abi)

# 檢查連接狀態
print(w3.is_connected())
private_key = 'PRIVATE_KEY'  # 從環境變量中讀取私鑰
account = w3.eth.account.privateKeyToAccount(private_key)
w3.eth.default_account = account.address
# 設置交易發送者


# 上傳生產數據
def upload_data(_id, _barcode, _manufacture, _description):
    tx_hash = contract.functions.uploadData(_id, _barcode, _manufacture, _description).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


# 更改註冊狀態
def change_registration_status(_id, _status):
    tx_hash = contract.functions.changeRegistrationStatus(_id, _status).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


# 查詢生產數據
def get_data(_id):
    data = contract.functions.getData(_id).call()
    return {
        "id": data[0],
        "barcode": data[1],
        "manufacture": data[2],
        "description": data[3],
        "is_registered": data[4]
    }


# 測試範例
upload_receipt = upload_data(2, ["123456", "789012"], "Manufacturer A", "Product Description")
print(f"Upload receipt: {upload_receipt}")

status_receipt = change_registration_status(1, True)
print(f"Status change receipt: {status_receipt}")

data = get_data(1)
print(f"Production data: {data}")
