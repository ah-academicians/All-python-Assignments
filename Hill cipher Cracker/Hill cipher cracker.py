import numpy as np

def decryptHillCipher(encryptedMsg, key):
    # Inverse matrix
    determinant = key[0][0] * key[1][1] - key[0][1] * key[1][0]
    determinant = determinant % 26
    multiplicative_inverse = findMultiplicativeInverse(determinant)
    inverseOfkey = key
    # Swap d <-> a
    inverseOfkey[0][0], inverseOfkey[1][1] = inverseOfkey[1, 1], inverseOfkey[0, 0]
    # multiplying diagonal elements with -1
    key[1][0] = key[1][0] * -1
    key[0][1] = key[0][1] * -1
    
    for row in range(2):
        for column in range(2):
            inverseOfkey[row][column] = inverseOfkey[row][column] * multiplicative_inverse
            inverseOfkey[row][column] = inverseOfkey[row][column] % 26

    P = stringToMatrixGenerator(encryptedMsg)
    msg_len = int(len(encryptedMsg) / 2)
    decrypted_msg = ""
    for i in range(msg_len):
        # Dot product
        column_0 = P[0][i] * inverseOfkey[0][0] + P[1][i] * inverseOfkey[0][1]
        # Modulate and add 65 to get back to the A-Z range in ascii
        integer = int(column_0 % 26 + 65)
        # Change back to chr type and add to text
        decrypted_msg += chr(integer)
        # Repeat for the second column
        column_1 = P[0][i] * inverseOfkey[1][0] + P[1][i] * inverseOfkey[1][1]
        integer = int(column_1 % 26 + 65)
        decrypted_msg += chr(integer)
    if decrypted_msg[-1] == "0":
        decrypted_msg = decrypted_msg[:-1]
    return decrypted_msg

def findMultiplicativeInverse(determinant):
    multiplicative_inverse = -1
    for i in range(26):
        inverse = determinant * i
        if inverse % 26 == 1:
            multiplicative_inverse = i
            break
    return multiplicative_inverse


def keyGenerator():
     # Make sure cipher determinant is relatively prime to 26 and only a/A - z/Z are given
    determinant = 0
    C = None
    while True:
        cipher = input("Input 4 letter key: ")
        # a valid key is fdfs
        C = stringToMatrixGenerator(cipher)
        determinant = C[0][0] * C[1][1] - C[0][1] * C[1][0]
        determinant = determinant % 26
        inverse_element = findMultiplicativeInverse(determinant)
        if inverse_element == -1:
            print("Invalid key Determinant is not relatively prime to 26, uninvertible key")
        elif np.amax(C) > 26 and np.amin(C) < 0:
            print("Only a-z characters are accepted")
            print(np.amax(C), np.amin(C))
        else:
            break
    return C

def stringToMatrixGenerator(string):
    integers = [CaracterToInteger(c) for c in string]
    length = len(integers)
    M = np.zeros((2, int(length / 2)), dtype=np.int32)
    iterator = 0
    for column in range(int(length / 2)):
        for row in range(2):
            M[row][column] = integers[iterator]
            iterator += 1
    return M

def CaracterToInteger(char):
    # Uppercase the char to get into range 65-90 in ascii table
    char = char.upper()
    # Cast chr to int and subtract 65 to get 0-25
    integer = ord(char) - 65
    return integer

def BruteForcekeyGenerator(randomkey):
     # Make sure cipher determinant is relatively prime to 26 and only a/A - z/Z are given
    determinant = 0
    C = None
    while True:
        C = stringToMatrixGenerator(randomkey)
        determinant = C[0][0] * C[1][1] - C[0][1] * C[1][0]
        determinant = determinant % 26
        inverse_element = findMultiplicativeInverse(determinant)
        if inverse_element == -1:
            print("Invalid key Determinant is not relatively prime to 26, uninvertible key")
            return 1
            break
        elif np.amax(C) > 26 and np.amin(C) < 0:
            print("Only a-z characters are accepted")
            print(np.amax(C), np.amin(C))
        else:
            break
    return C

def main():
    encrypted_msg = input("Enter encrypted Message: ")
    key = keyGenerator()
    decrypted_msg = decryptHillCipher(encrypted_msg, key)
    print("decrypted message is :",decrypted_msg)

def cracker(ciphertext, plaintext):
    plaintext = plaintext.upper()
    #list of all combination of four characters
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ciphers = []
    for i in range(26):
        for j in range(26):
            for k in range(26):
                for l in range(26):
                    ciphers.append(alphabet[i]+ alphabet[j]+ alphabet[k]+alphabet[l])
    for cipher in ciphers:
        print(cipher)
        key = BruteForcekeyGenerator(cipher)
        print(key)
        try:
            if str(key) == '1':
                continue
            else:
                decrypted_msg = decryptHillCipher(ciphertext, key)
                print("with key", cipher, "decrypted text is", decrypted_msg)
                if decrypted_msg == plaintext:
                    print("key is", cipher)
                    break
        except:
            continue
#cracker('rvnn','lina')

#test
key = BruteForcekeyGenerator("fdfs")
print(key)
print(decryptHillCipher("rvnn", key))