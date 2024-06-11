import json
from web3 import Web3
from smart_contract_api.config import get_settings

Setting = get_settings()


class BikeCrankToken:
    def __init__(self, ):
        self.web3 = Web3(Web3.HTTPProvider(Setting.web3_provider))
        with open("ABI.json", 'r') as abi_file:
            abi = json.load(abi_file)
        self.contract = self.web3.eth.contract(address=Setting.contract_address, abi=abi)
        self.from_address = Setting.from_address
        self.private_key = Setting.address_private_key

    def approve(self, to_address, token_id):
        transaction = self.contract.functions.approve(to_address, token_id).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=self.private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)

    def balance_of(self, owner_address):
        return self.contract.functions.balanceOf(owner_address).call()

    def change_registration_status(self, product_id, status):
        transaction = self.contract.functions.changeRegistrationStatus(product_id, status).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=self.private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)

    def get_all_data_ids(self):
        return self.contract.functions.getAllDataIds().call()

    def get_all_token_ids(self):
        return self.contract.functions.getAllTokenIds().call()

    def get_approved(self, token_id):
        return self.contract.functions.getApproved(token_id).call()

    def get_data(self, product_id):
        return self.contract.functions.getData(product_id).call()

    def get_meta_data(self, token_id):
        return self.contract.functions.getMetaData(token_id).call()

    def list_for_sale(self, token_id: int, is_listed: bool):
        transaction = self.contract.functions.listForSale(token_id, is_listed).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=self.private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)

    def name(self):
        return self.contract.functions.name().call()

    def owner(self):
        return self.contract.functions.owner().call()

    def owner_of(self, token_id):
        return self.contract.functions.ownerOf(token_id).call()

    def register_product(self, product_id: int, to_address: str):
        transaction = self.contract.functions.registerProduct(product_id, to_address).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.from_address),
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=self.private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)

    def safe_transfer_from(self, from_address, to_address, token_id, private_key):
        transaction = self.contract.functions.safeTransferFrom(from_address, to_address, token_id).buildTransaction({
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': self.web3.to_wei('50', 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(from_address),
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)

    def symbol(self):
        return self.contract.functions.symbol().call()

    def token_uri(self, token_id):
        return self.contract.functions.tokenURI(token_id).call()

    def upload_data(self, product_id, barcode, manufacture, product_token):
        transaction = self.contract.functions.uploadData(
            product_id, barcode, manufacture, product_token).buildTransaction({
                'chainId': 1,
                'gas': 2000000,
                'gasPrice': self.web3.to_wei('50', 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(self.from_address),
            })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=self.private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.to_hex(txn_hash)
