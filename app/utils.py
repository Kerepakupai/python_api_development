from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def find_item(id, items):
    for p in items:
        if p['id'] == id:
            return p


def find_index(id, items):
    for i, p in enumerate(items):
        if p['id'] == id:
            return i


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)