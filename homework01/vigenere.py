def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    upper, lower = ord("A"), ord("a")
    text = list(plaintext)
    for index, value in enumerate(text):
        if value.isalpha():
            base = upper if value.isupper() else lower
            shift = ord(keyword[index % len(keyword)]) - base
            text[index] = chr((ord(value) - base + shift) % 26 + base)
    ciphertext = ''.join(text)
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    upper, lower = ord("A"), ord("a")
    text = list(ciphertext)
    for index, value in enumerate(text):
        if value.isalpha():
            base = upper if value.isupper() else lower
            shift = ord(keyword[index % len(keyword)]) - base
            text[index] = chr((ord(value) - base - shift) % 26 + base)
    ciphertext = ''.join(text)
    return ciphertext
