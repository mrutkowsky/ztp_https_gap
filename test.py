import hashlib


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

password = "admin123"

hash_password = hash_password(password)

print(hash_password)