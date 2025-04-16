import pickle
data = bytes.fromhex("8004950a000000000000008c064e65796d6172942e")
obj = pickle.loads(data)
print(obj)
