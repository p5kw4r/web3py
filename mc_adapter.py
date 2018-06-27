from binascii import hexlify, unhexlify
from mcrpc import RpcClient


class MCAdapter():
    host = 'localhost'
    port = '7324'
    rpcuser = 'multichainrpc'
    rpcpassword = 'GkHfnch8QBgqvZJeMLyb57h42h6TZREr25Uhp5iZ8T2E'
    client = RpcClient(host, port, rpcuser, rpcpassword)
    default_address = '1RuG62c89Vk1V6psGhtAwywan9mWsvFvBv2cLM'
    private_key = 'VAUWVB6KStqzemdzXqak77cbkaz6tyYyRbcG3pqBcpP2xNFzAvT8bt2E'
    encoding = 'utf-8'

    def retrieve(self, transaction_hash):
        tx = self.get_raw_transaction(transaction_hash)
        data_hex = self.extract_data(tx)
        return self.to_text(data_hex)

    def get_raw_transaction(self, transaction_hash):
        return self.client.getrawtransaction(transaction_hash, verbose=1)

    @staticmethod
    def extract_data(transaction):
        return transaction['vout'][1]['data'][0]

    def to_text(self, data_hex):
        text_bytes = unhexlify(data_hex)
        return text_bytes.decode(encoding=self.encoding)

    def store(self, text):
        data_hex = self.to_hex(text)
        tx_hex = self.create_raw_send_from(data_hex)
        signed_tx_hex = self.sign_raw_transaction(tx_hex)
        return self.send_raw_transaction(signed_tx_hex)

    def create_raw_send_from(
            self,
            data_hex,
            sender=default_address,
            recipient=default_address,
            amount=0):
        return self.client.createrawsendfrom(
            sender,
            {recipient: amount},
            [data_hex])

    def to_hex(self, text):
        text_bytes = bytes(text, encoding=self.encoding)
        return hexlify(text_bytes)

    def sign_raw_transaction(self, transaction_hex):
        parent_outputs = []
        signed = self.client.signrawtransaction(
            transaction_hex,
            parent_outputs,
            [self.private_key])
        if signed['complete']:
            return signed['hex']

    def send_raw_transaction(self, transaction_hash):
        return self.client.sendrawtransaction(transaction_hash)