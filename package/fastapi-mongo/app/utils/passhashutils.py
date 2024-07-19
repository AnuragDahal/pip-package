from passlib.hash import bcrypt


class Encrypt:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        return bcrypt.verify(password, hash)
