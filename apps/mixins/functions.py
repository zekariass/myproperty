import random
import string
import uuid

def generate_unique_code(length):

        code1_len = length // 2
        code2_len = length - code1_len
        characters = string.ascii_uppercase + string.digits
        code1 = ''.join(random.choice(characters) for _ in range(code1_len)) 

        code2  = uuid.uuid4().hex[:code2_len].upper()

        code = code1 + code2

        return code