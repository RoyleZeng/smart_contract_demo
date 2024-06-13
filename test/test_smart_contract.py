import json
import pytest
from web3 import Web3
from smart_contract_api.business_model.smart_contract import BikeCrankToken  # 確保這裡引入正確的類別

# 測試設定

from_address = "0xYourAddress"
private_key = "YourPrivateKey"

# 測試數據
data_to_upload = [
    {"id": i, "barcode": [f"barcode_{i}_1", f"barcode_{i}_2"], "manufacture": f"manufacture_{i}",
     "product_token": f"token_{i}"}
    for i in range(1, 21)
]