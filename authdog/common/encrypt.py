# coding:utf-8
import hashlib
import binascii
import os
import datetime
import logging

import jwt
from pecan import conf

hash_name = "sha256"
iterations = 1000
jwt_algorithm = 'HS256'


logger = logging.getLogger(__name__)


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


def validate_password(input_password, stored_mix_password):
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


def make_token(context, expire=60):
    """
    :param context: a dictionary to update payload
    :param expire: token expire time
    :return:
    """
    global jwt_algorithm
    key = getattr(conf, "SECREATE_KEY", None)
    payload = {'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expire)}
    if isinstance(context, dict):
        payload.update(context)
    if key:
        try:
            token = jwt.encode(payload, key, algorithm=jwt_algorithm)
            return token
        except jwt.exceptions.InvalidAlgorithmError:
            msg = "The specified algorithm is not recognized by PyJWT."
            logger.error(msg)
            raise Exception(msg)
        except Exception:
            msg = "make token failed"
            logger.error(msg)
            raise Exception(msg)
    else:
        msg = "Can not find SECREATE_KEY in config file"
        logger.error(msg)
        raise Exception(msg)


def validate_token(token):
    global jwt_algorithm
    key = getattr(conf, "SECREATE_KEY", None)
    if key:
        try:
            decoded = jwt.decode(token, key, algorithm=jwt_algorithm)
            return decoded
        except jwt.exceptions.ExpiredSignatureError:
            msg = "Token’s exp claim indicates that it has expired"
            logger.error(msg)
            raise Exception(msg)
        except jwt.exceptions.DecodeError:
            msg = " token cannot be decoded because it failed validation"
            logger.error(msg)
            raise Exception(msg)
    else:
        msg = "Can not find SECREATE_KEY in config file"
        logger.error(msg)
        raise Exception(msg)
