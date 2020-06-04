from django.test import TestCase

# Create your tests here.
import random

def coding(id):
    modulus=random.randrange(10, 100)
    random_start=random.randrange(100,1000)
    random_end=random.randrange(1000,10000)
    key=int(id)*modulus
    mix_key=str(modulus)+str(random_start)+str(key)+str(random_end)
    length=str(len(mix_key))[-1:]
    final_key=mix_key+length
    return final_key

def uncoding(id):
    modulus=int(id[:2])
    length=str(len(id)-1)[-1:]
    length_ver=id[-1:]
    id_ver=id[5:-5]
    if length == length_ver:
        id=round(int(id_ver)/modulus,0)
    else:
        id='0'
    return id