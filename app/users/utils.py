import base64
import hashlib


def hash_email(email: str) -> str:
    sha256_hash = hashlib.sha256(email.encode()).digest()
    base64url_encoded = base64.urlsafe_b64encode(sha256_hash).rstrip(b'=').decode()
    cleaned_hash = ''.join(filter(str.isalnum, base64url_encoded))
    return cleaned_hash
