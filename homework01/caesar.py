def encrypt_caesar(plaintext, shift):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    upper, lower = ord("A"), ord("a")
    text = list(plaintext)
    for index, value in enumerate(text):
        if value.isalpha():
            base = upper if value.isupper() else lower
            text[index] = chr((ord(value) - base + shift) % 26 + base)
    ciphertext = ''.join(text)
    return ciphertext

def decrypt_caesar(ciphertext, shift):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    upper, lower = ord("A"), ord("a")
    text = list(ciphertext)
    for index, value in enumerate(text):
        if value.isalpha():
            base = upper if value.isupper() else lower
            text[index] = chr((ord(value) - base - shift) % 26 + base)
    ciphertext = ''.join(text)
    return ciphertext
