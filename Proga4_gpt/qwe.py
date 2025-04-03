from typing import Annotated
import hashlib

def func2():
    return 2+2
def func(rts : Annotated[int, func2]):
    print(rts)

func(2)

secret_key="secret".encode('utf-8')
print(hashlib.sha256(secret_key).hexdigest())

def get_pass_hash(pssw: str) -> str:
    return hashlib.sha256(f'{secret_key}{pssw}'.encode('utf-8')).hexdigest()