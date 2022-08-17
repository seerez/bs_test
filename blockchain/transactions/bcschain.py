import json

import requests
from jsonrpclib import jsonrpc
from pycoin.coins.bitcoin.Tx import Spendable
from pycoin.coins.tx_utils import create_tx
from pycoin.ecdsa.secp256k1 import secp256k1_generator
from pycoin.encoding.hexbytes import h2b, h2b_rev
from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.solve.utils import build_hash160_lookup


class BCSNet:

    def __init__(self) -> None:

        self.rpc_url: str = 'http://bcs_tester:iLoveBCS@45.32.232.25:3669'
        self.api_url: str = 'https://bcschain.info/api'
        self.bcs_address: str = 'BRw2i7cq5QHd6DSCXB96Yd4nsShovPKv47'
        self.network = create_bitcoinish_network(
            symbol="BCS",
            network_name="BCS",
            subnet_name="mainnet",
            wif_prefix_hex="80",
            address_prefix_hex="19",
            pay_to_script_prefix_hex="32",
            bip32_prv_prefix_hex="0488ade4",
            bip32_pub_prefix_hex="0488B21E",
            bech32_hrp="bc",
            bip49_prv_prefix_hex="049d7878",
            bip49_pub_prefix_hex="049D7CB2",
            bip84_prv_prefix_hex="04b2430c",
            bip84_pub_prefix_hex="04B24746",
            magic_header_hex="F1CFA6D3",
            default_port=3666
        )

        self.rpcproxy = jsonrpc.ServerProxy(self.rpc_url)

    def getutxo(self) -> str:
        """Получаем значение utxo"""
        utxo = requests.get(
            f'{self.api_url}/address/{self.bcs_address}/utxo'
            )
        utxo = json.loads(utxo.text)[0]
        return utxo

    def sendrawtransaction(self, raw_hex: str):
        """Передает hex представление транзакции"""
        return self.rpcproxy.sendrawtransaction(raw_hex)

    def getnewaddress(self):
        """Возвращает json с ноды"""
        return self.rpcproxy.getnewaddress()

    def decoderawtransaction(self, raw_hex: str):
        """Декодинг строки"""
        return self.rpcproxy.decoderawtransaction(raw_hex)

    def create_tx(self, secret_key: str, payables: list = [],
                  buildhash: callable = build_hash160_lookup,
                  generators: list = [secp256k1_generator]
                  ):
        """Формирует транзакцию"""
        utxo = self.getutxo()
        spendables = Spendable(
                  coin_value=int(utxo['value']),
                  script=h2b(utxo['scriptPubKey']),
                  tx_hash=h2b_rev(utxo['transactionId']),
                  tx_out_index=int(utxo['outputIndex'])
        )
        payables.append((self.bcsaddress, int(utxo['value'] - 10**8)))
        unsigned_tx = create_tx(self.network,
                                spendables,
                                payables,
                                fee='standart'
                                )
        wif = self.network.parse.wif(secret_key)
        exponents = wif.secret_exponent()
        solver = buildhash([exponents], [generators])
        return unsigned_tx.sign(solver).as_hex()
