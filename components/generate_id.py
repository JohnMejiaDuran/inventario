import random
import string

def generate_anuncio_carga_id():
    # Two random uppercase letters
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    
    # Five random non-repeating digits
    digits = ''.join(random.sample(string.digits, 5))
    
    return letters + digits