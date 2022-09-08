import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = b'admin password'

key = hashlib.sha256("password".encode()).digest()
nonce = "1234567890123456".encode()

cipher = AES.new(key, AES.MODE_EAX, nonce)
ciphertext, tag = cipher.encrypt_and_digest(data)



enounce = base64.b64encode(cipher.nonce).decode('utf-8')
etag = base64.b64encode(tag).decode('utf-8')
etext = base64.b64encode(ciphertext).decode('utf-8')

encoded = "#".join([enounce,etag,etext])
#ENC[AES256_GCM,data:CwE4O1s=,iv:2k=,aad:o=,tag:w==]
print(encoded)


from Crypto.Cipher import AES


enounce , tag , etext = encoded.split("#")

nonce = base64.b64decode(enounce)
tag= base64.b64decode(etag)
ciphertext = base64.b64decode(etext)

# let's assume that the key is somehow available again
cipher = AES.new(key, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)

print(data)
