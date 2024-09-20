def decrypt_message(encrypted_message, key):
    decrypted_message = []

    for char in encrypted_message:
        if char.isalpha():  # Only decrypt alphabetic characters
            shift_base = 65 if char.isupper() else 97  # Use ASCII base for upper or lower case
            # Perform the Caesar shift and wrap around using modulo
            decrypted_char = chr((ord(char) - shift_base - key) % 26 + shift_base)
            decrypted_message.append(decrypted_char)
        else:
            # Non-alphabetic characters remain unchanged
            decrypted_message.append(char)

    return ''.join(decrypted_message)
