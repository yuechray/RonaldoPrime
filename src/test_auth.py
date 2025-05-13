import bcrypt


password = "admin"


salt = bcrypt.gensalt()


password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)


print(password_hash.decode('utf-8'))