from Crypto.Cipher import AES

IV="F01D86CDBB7E1CD88815BEB4106A558C".decode('hex')

key = "AngeWouldLoveIt!"

aes = AES.new(key, AES.MODE_CBC, IV)

with open("flag.png", "rb") as f:
	d = f.read()

d = aes.encrypt(d)

with open("out", "wb") as f:
	f.write(d)
