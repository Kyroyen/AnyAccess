from uuid import uuid4

def get_unique_id(**kwargs):
    return uuid4().hex