from web3 import HTTPProvider, Web3
import json
import time
userAcc = web3.toChecksumAddress('0xC459cc3AC9f8462Be2EF00aAD02fAc7af2e97b14')
userKey = '0xda09f8cdec20b7c8334ce05b27e6797bef01c1ad79c59381666467552c5012e3'
#此為Uniswap router的合約地址，可以用來做Token的交換
UNI_ROUTER_ADDR = web3.toChecksumAddress('0x7a250d5630b4cf539739df2c5dacb4c659f2488d')
#此為封裝以太(WETH)的合約地址
WETH_ADDR = web3.toChecksumAddress('0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2')
#此為USDT的合約地址
USDT_ADDR = web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7')

#連線到剛啟動的Ganache RPC Server
web3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
block = web3.eth.get_block('latest')
#可以看到目前的區塊高度等資訊
print(block)