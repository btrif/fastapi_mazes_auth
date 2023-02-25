#  Created by btrif Trif on 06-02-2023 , 11:10 AM.
# https://passlib.readthedocs.io/en/stable/


from passlib.hash import pbkdf2_sha256

# generate new salt, hash password
hashed = pbkdf2_sha256.hash("bogdan")
print(f"hashed password : \n{hashed}")

# verifying the password

correct_verification = pbkdf2_sha256.verify("bogdan", hashed)
print(f"Correct verification : {correct_verification}")

false_verification = pbkdf2_sha256.verify("toomanysecrets", hashed)
print(f"Correct verification : {false_verification}")


