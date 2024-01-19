# Rabin.py
import prime

# encryption function

def encryption(plaintext, n):
    # c = m^2 mod n
    #plaintext = padding(plaintext)
    return plaintext ** 2 % n


# padding 16 bits to the end of a number
def padding(plaintext):
    binary_str = bin(plaintext)     # convert to a bit string
    output = binary_str + binary_str[-16:]      # pad the last 16 bits to the end
    return int(output, 2)       # convert back to integer


# encryption function
def decryption(a, p, q):
    n = p * q
    r, s = 0, 0
    # find sqrt
    # for p
    if p % 4 == 3:
        r = prime.sqrt_p_3_mod_4(a, p)
    elif p % 8 == 5:
        r = prime.sqrt_p_5_mod_8(a, p)
    # for q
    if q % 4 == 3:
        s = prime.sqrt_p_3_mod_4(a, q)
    elif q % 8 == 5:
        s = prime.sqrt_p_5_mod_8(a, q)

    gcd, c, d = prime.egcd(p, q)
    x = (r * d * q + s * c * p) % n
    y = (r * d * q - s * c * p) % n
    lst = [x, n - x, y, n - y]

    #plaintext = choose(lst)
    #string = bin(plaintext)
    #string = string[:-16]
    #plaintext = int(string, 2)

    return lst


# decide which answer to choose
def choose(lst):

    for i in lst:
        binary = bin(i)
        append = binary[-16:]   # take the last 16 bits
        binary = binary[:-16]   # remove the last 16 bits
        if append == binary[-16:]:
            return i
    return

if __name__ == '__main__':
    p = 7
    q = 11
    n = 77
    m = 20
    # encryption(plaintext, n)
    c = encryption(m, n)
    print(c)
    # lst = [x, n - x, y, n - y]
    lst = decryption(c, 73, 61)
    print(lst)
    print(choose(lst))
