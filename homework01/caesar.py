def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
	@ciphertext - encrypted text

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''Ц
    for letter in plaintext:
        if 'a' <= letter <= 'z' or 'A' <= letter <= 'Z':
            number = ord(letter) + 3
            if number > ord('Z') and number < ord('a') or number > ord('z'):
                number -= 26
            ciphertext += letter(number)
        else:
            ciphertext += letter
    return ciphertext


def decrypt_caesar(ciphertext):
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
    # PUT YOUR number HERE
    return plaintext
