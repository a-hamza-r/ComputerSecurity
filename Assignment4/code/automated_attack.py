#!/usr/bin/python3
import socket
from binascii import hexlify, unhexlify

# XOR two bytearrays
def xor(first, second):
   return bytearray(x^y for x,y in zip(first, second))

class PaddingOracle:

    def __init__(self, host, port) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        ciphertext = self.s.recv(4096).decode().strip()
        self.ctext = unhexlify(ciphertext)

    def decrypt(self, ctext: bytes) -> None:
        self._send(hexlify(ctext))
        return self._recv()

    def _recv(self):
        resp = self.s.recv(4096).decode().strip()
        return resp 

    def _send(self, hexstr: bytes):
        self.s.send(hexstr + b'\n')

    def __del__(self):
        self.s.close()


if __name__ == "__main__":
    oracle = PaddingOracle('10.9.0.80', 6000)

    # Get the IV + Ciphertext from the oracle
    iv_and_ctext = bytearray(oracle.ctext)
    length = len(iv_and_ctext)
    cyphers = [iv_and_ctext[i:i+16] for i in range(0, length, 16)]
    plaintexts = []

    for i in range(len(cyphers)-1, 0, -1):
        C1 = cyphers[i-1]
        C2 = cyphers[i]
        D2 = bytearray(16)
        CC1 = bytearray(16)

        CC1[0]  = 0x00
        CC1[1]  = 0x00
        CC1[2]  = 0x00
        CC1[3]  = 0x00
        CC1[4]  = 0x00
        CC1[5]  = 0x00
        CC1[6]  = 0x00
        CC1[7]  = 0x00
        CC1[8]  = 0x00
        CC1[9]  = 0x00
        CC1[10] = 0x00
        CC1[11] = 0x00
        CC1[12] = 0x00
        CC1[13] = 0x00
        CC1[14] = 0x00
        CC1[15] = 0x00

        for K in range(1,17):
            byte_K = K.to_bytes(1, byteorder="big")
            for j in range(16-K+1, 16):
                current_D_j = D2[j].to_bytes(1, byteorder="big")
                current_CC1_j = xor(current_D_j, byte_K)
                CC1[j] = current_CC1_j[0]
            for i in range(256):
                CC1[16 - K] = i
                status = oracle.decrypt(CC1 + C2)
                if status == "Valid":
                    byte_i = i.to_bytes(1, byteorder="big")
                    D_Kth_last = xor(byte_i, byte_K)
                    C1_Kth_last = C1[16 - K].to_bytes(1, byteorder="big")
                    plainText = xor(D_Kth_last, C1_Kth_last)
                    D2[16 - K] = D_Kth_last[0]

        plaintext = xor(C1, D2)
        plaintexts.append(plaintext)

    print("plaintext with padding: ")
    for pt in plaintexts[::-1]:
        print(pt.hex())

    print("\nplaintext without padding: ")
    padding = plaintexts[0][-1].to_bytes(1, byteorder="big")
    plaintexts[0] = plaintexts[0].rstrip(padding)
    for pt in plaintexts[::-1]:
        print(pt.hex())
    
    print("\nplaintext as string: ")
    for pt in plaintexts[::-1]:
        print(pt.decode('utf-8'), end='')
    print()
