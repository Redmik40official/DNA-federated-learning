"""
DNA Cryptography Module
Handles all DNA encoding, chaotic maps, encryption, and decryption.
"""

import numpy as np
import hashlib
import json

ENCODING = {
    1: {'00': 'A', '01': 'C', '10': 'G', '11': 'T'},
    2: {'00': 'A', '01': 'G', '10': 'C', '11': 'T'},
    3: {'00': 'C', '01': 'A', '10': 'T', '11': 'G'},
    4: {'00': 'C', '01': 'T', '10': 'A', '11': 'G'},
    5: {'00': 'G', '01': 'A', '10': 'T', '11': 'C'},
    6: {'00': 'G', '01': 'T', '10': 'A', '11': 'C'},
    7: {'00': 'T', '01': 'C', '10': 'G', '11': 'A'},
    8: {'00': 'T', '01': 'G', '10': 'C', '11': 'A'},
}

DECODING = {
    r: {v: k for k, v in rule.items()}
    for r, rule in ENCODING.items()
}

XOR = {
    ('A','A'):'A', ('A','C'):'C', ('A','G'):'G', ('A','T'):'T',
    ('C','A'):'C', ('C','C'):'A', ('C','G'):'T', ('C','T'):'G',
    ('G','A'):'G', ('G','C'):'T', ('G','G'):'A', ('G','T'):'C',
    ('T','A'):'T', ('T','C'):'G', ('T','G'):'C', ('T','T'):'A',
}

ADD = {
    ('A','A'):'A', ('A','C'):'C', ('A','G'):'G', ('A','T'):'T',
    ('C','A'):'C', ('C','C'):'G', ('C','G'):'T', ('C','T'):'A',
    ('G','A'):'G', ('G','C'):'T', ('G','G'):'A', ('G','T'):'C',
    ('T','A'):'T', ('T','C'):'A', ('T','G'):'C', ('T','T'):'G',
}

SUB = {
    ('A','A'):'A', ('A','C'):'T', ('A','G'):'G', ('A','T'):'C',
    ('C','A'):'C', ('C','C'):'A', ('C','G'):'T', ('C','T'):'G',
    ('G','A'):'G', ('G','C'):'C', ('G','G'):'A', ('G','T'):'T',
    ('T','A'):'T', ('T','C'):'G', ('T','G'):'C', ('T','T'):'A',
}

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary) - 7, 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def binary_to_dna(binary, rule=1):
    if len(binary) % 2 != 0:
        binary += '0'
    return ''.join(ENCODING[rule][binary[i:i+2]] for i in range(0, len(binary), 2))

def dna_to_binary(dna, rule=1):
    return ''.join(DECODING[rule][b] for b in dna)

def logistic_map(x0, r, n):
    seq = []
    x = x0
    for _ in range(n):
        x = r * x * (1 - x)
        seq.append(x)
    return seq

def chaotic_to_dna(seq):
    bases = ['A', 'C', 'G', 'T']
    return ''.join(bases[int(v * 4) % 4] for v in seq)

def make_key(password, length):
    h = hashlib.sha256(password.encode()).hexdigest()
    b = bin(int(h, 16))[2:].zfill(256)
    while len(b) < length * 2:
        b += b
    return binary_to_dna(b[:length * 2], rule=1)

def dna_xor(s1, s2):
    return ''.join(XOR[(a, b)] for a, b in zip(s1, s2))

def dna_add(s1, s2):
    return ''.join(ADD[(a, b)] for a, b in zip(s1, s2))

def dna_sub(s1, s2):
    return ''.join(SUB[(a, b)] for a, b in zip(s1, s2))

def encrypt(plaintext, password, rule=1, x0=0.5, r=3.99):
    binary = text_to_binary(plaintext)
    dna = binary_to_dna(binary, rule)
    pk = make_key(password, len(dna))
    ck = chaotic_to_dna(logistic_map(x0, r, len(dna)))
    combined = dna_xor(pk, ck)
    enc = dna_xor(dna, combined)
    final = dna_add(enc, ck)
    return {'cipher': final, 'rule': rule, 'x0': x0, 'r': r}

def decrypt(cipher_dict, password):
    final = cipher_dict['cipher']
    rule = cipher_dict['rule']
    x0 = cipher_dict['x0']
    r = cipher_dict['r']
    ck = chaotic_to_dna(logistic_map(x0, r, len(final)))
    enc = dna_sub(final, ck)
    pk = make_key(password, len(enc))
    combined = dna_xor(pk, ck)
    dna = dna_xor(enc, combined)
    binary = dna_to_binary(dna, rule)
    return binary_to_text(binary)

def encrypt_weights(weights_dict, password, rule=1, x0=0.5, r=3.99):
    encrypted = {}
    for name, w in weights_dict.items():
        flat = w.flatten().tolist()
        text = json.dumps(flat)
        enc = encrypt(text, password, rule, x0, r)
        enc['shape'] = list(w.shape)
        encrypted[name] = enc
    return encrypted

def decrypt_weights(encrypted_dict, password):
    weights = {}
    for name, enc in encrypted_dict.items():
        text = decrypt(enc, password)
        flat = json.loads(text)
        shape = enc['shape']
        weights[name] = np.array(flat).reshape(shape)
    return weights
