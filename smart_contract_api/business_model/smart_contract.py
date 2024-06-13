import json
from web3 import Web3
from smart_contract_api.config import get_settings
from smart_contract_api.schema.auth import ETHAccount
from smart_contract_api.schema.smart_contract import ProductData

Setting = get_settings()


class BikeCrankToken:
    def __init__(self, ):
        self.web3 = Web3(Web3.HTTPProvider(Setting.web3_provider))
        with open("ABI.json", 'r') as abi_file:
            abi = json.load(abi_file)
        self.contract = self.web3.eth.contract(address=Setting.contract_address, abi=abi)
        self.from_address = Setting.from_address
        self.private_key = Setting.address_private_key

    def _build_and_send_transaction(self, function, private_key):
        transaction = function.build_transaction({
            'from': self.from_address,
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })
        signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)

    def create_user_account(self) -> ETHAccount:
        account = self.web3.eth.account.create()
        return ETHAccount(address=account.address, private_key=account.key.hex())

    def get_user_account_balance(self, address: str):
        user_acc = self.web3.to_checksum_address(address)
        return self.web3.eth.get_balance(user_acc)

    def get_eth_from_admin(self, to_address: str):
        amount_wei = self.web3.to_wei(number=1, unit='ether')

        transaction = {
            'to': to_address,
            'from': self.from_address,
            'value': amount_wei,
            'gas': 21000,
            'gasPrice': self.web3.to_wei(number='50', unit='gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        }
        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)

    def balance_of(self, owner_address):
        return self.contract.functions.balanceOf(owner_address).call()

    def change_registration_status(self, product_id, status):
        function = self.contract.functions.changeRegistrationStatus(product_id, status)
        return self._build_and_send_transaction(function, self.private_key)

    def get_all_data_ids(self):
        return self.contract.functions.getAllDataIds().call()

    def get_all_token_ids(self):
        return self.contract.functions.getAllTokenIds().call()

    def get_approved(self, token_id):
        return self.contract.functions.getApproved(token_id).call()

    def get_data(self, product_id) -> ProductData:
        response = self.contract.functions.getData(product_id).call()
        return ProductData(id=response[0], barcodes=response[1], manufacture=response[2], product_token=response[3],
                           is_registered=response[4])

    def get_meta_data(self, token_id):
        return self.contract.functions.getMetaData(token_id).call()

    def list_for_sale(self, token_id: int, is_listed: bool):
        function = self.contract.functions.listForSale(token_id, is_listed)
        return self._build_and_send_transaction(function=function, private_key=self.private_key)

    def name(self):
        return self.contract.functions.name().call()

    def owner(self):
        return self.contract.functions.owner().call()

    def owner_of(self, token_id):
        return self.contract.functions.ownerOf(token_id).call()

    def register_product(self, product_id: int, to_address: str):
        function = self.contract.functions.registerProduct(product_id, to_address)
        return self._build_and_send_transaction(function=function, private_key=self.private_key)

    def safe_transfer_from(self, from_address, to_address, token_id, private_key):
        function = self.contract.functions.safeTransferFrom(from_address, to_address, token_id)
        return self._build_and_send_transaction(function=function, private_key=private_key)

    def symbol(self):
        return self.contract.functions.symbol().call()

    def token_uri(self, token_id):
        return self.contract.functions.tokenURI(token_id).call()

    def get_account_all_token_id(self, address):
        return self.contract.functions.getTokensOfOwner(address).call()

    def upload_data(self, product_id, barcode, manufacture, product_token):
        function = self.contract.functions.uploadData(product_id, barcode, manufacture, product_token)
        return self._build_and_send_transaction(function=function, private_key=self.private_key)


if __name__ == "__main__":
    data_to_upload = [
        {"id": i, "barcode": [f"barcode_{i}_1", f"barcode_{i}_2"], "manufacture": f"manufacture_{i}",
         "product_token": f"token_{i}"}
        for i in range(1, 21)
    ]
    bike_crank_token = BikeCrankToken()
    print(bike_crank_token.name())
    new_account = bike_crank_token.create_user_account()
    print(new_account)
    # print(bike_crank_token.get_user_account_balance('0xb2C28090B77E754BfEeaC1e5e4b7aD337f4f17Ad'))
    # bike_crank_token.get_eth_from_admin('0xb2C28090B77E754BfEeaC1e5e4b7aD337f4f17Ad')
    # print(bike_crank_token.get_user_account_balance('0xb2C28090B77E754BfEeaC1e5e4b7aD337f4f17Ad'))

    #
    # for data in data_to_upload:
    #     txn_hash_t = bike_crank_token.upload_data(
    #         data["id"], data["barcode"], data["manufacture"], data["product_token"])
    #     print(f"Uploaded data with transaction hash: {txn_hash_t}")
    # for i in range(1, 11):
    #     bike_crank_token.change_registration_status(i, True)
    #
    # # 註冊和鑄造前 10 比數據
    # for i in range(1, 11):
    #     txn_hash_register = bike_crank_token.register_product(data_to_upload[i - 1]["id"],
    #                                                           to_address="0x3Ebe4671cbe188B8cE7dDD76766e65Bfd7267c47")
    #     print(f"Registered product with transaction hash: {txn_hash_register}")
    #
    #     txn_hash_list = bike_crank_token.list_for_sale(data_to_upload[i - 1]["id"], True)
    #     print(f"Listed product for sale with transaction hash: {txn_hash_list}")

    # print(bike_crank_token.token_uri(1))
    # data = json.loads(bike_crank_token.token_uri(1))
    # print(data['isListedForSale'])
    # addr_token = bike_crank_token.get_account_all_token_id(address="0x3Ebe4671cbe188B8cE7dDD76766e65Bfd7267c47")
    # print(addr_token)
    # print(type(addr_token))
