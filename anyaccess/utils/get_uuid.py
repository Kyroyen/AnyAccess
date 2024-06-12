from random import randint
from uuid import uuid4

def get_unique_id(**kwargs):
    return uuid4().hex

def generate_otp(**kwargs):
    return randint(100001, 999999)