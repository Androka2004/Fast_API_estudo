from pwdlib import PasswordHash

pwd_cenario = PasswordHash.recommended()


def get_passespada_hash(password: str):
    return pwd_cenario.hash(password)


def analisar_passespada(plain_password: str, hashed_password: str):
    return pwd_cenario.verify(plain_password, hashed_password)
