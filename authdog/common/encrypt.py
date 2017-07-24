# coding:utf-8
import hashlib
import binascii
import os


hash_name = "sha256"
iterations = 1000


def encrypt_password(password, hex_salt):
    global hash_name
    global iterations
    encrypted_password = hashlib.pbkdf2_hmac(hash_name, password, hex_salt, iterations)
    hex_password = binascii.hexlify(encrypted_password)
    return hex_password


def new_password(password):
    global hash_name
    global iterations
    random_key = os.urandom(16)
    hex_salt = binascii.hexlify(random_key)
    # pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)
    # iterations = 1000
    encrypted_password = hashlib.pbkdf2_hmac(hash_name, password, hex_salt, iterations)
    hex_password = binascii.hexlify(encrypted_password)
    return [hex_password, hex_salt]


def mix_password_salt(hex_password, hex_salt):
    seq = [hex_password, hex_salt]
    mix_str = ":".join(seq)
    return mix_str


def parse_mix_str(mix_str):
    hex_password, hex_salt = mix_str.strip().split(":")
    return [hex_password, hex_salt]


def compare_password(input_password, stored_mix_password):
    # input_password is from request, stored_password is from db
    stored_hex_password, stored_hex_salt = parse_mix_str(stored_mix_password)
    encrypted_password = encrypt_password(input_password, stored_hex_salt)
    if encrypted_password == stored_hex_password:
        return True
    else:
        return False


def make_password(password):
    seq = new_password(password)
    mix_str = mix_password_salt(*seq)
    return mix_str
