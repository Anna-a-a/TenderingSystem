import bcrypt


def hash_password(password: str) -> str:
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Return the hashed password as a string
    return hashed_password.decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    # Encode the password and hashed password to bytes
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    # Check if the password matches the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)