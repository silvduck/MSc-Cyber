#############################################
# Silvia Sanvicente, 25 oct 2021            #
# Sistemes de Blockchain                    #
# PAC1, Exercici 5                          #
#############################################

# IMPORTS
from binascii import unhexlify, hexlify
from datetime import datetime
from hashlib import sha256
import secrets
import time as t

# FUNCTIONS
# converteix valors de big endian a little endian
def big_endian_to_little_endian(value):
  if type(value) is str:
    value = unhexlify(value)
  return hexlify(value[::-1]).decode("utf-8")

# retorna el temps actual en format hexadecimal (big endian)
def current_time_little_endian():
  now_tm = (datetime.now().strftime('%Y%m%d%H%M%S'))
  time_array = t.strptime(now_tm, '%Y%m%d%H%M%S')
  stamp_tm = int(t.mktime(time_array))
  time_hex_big = hex(stamp_tm)[2:]
  return time_hex_big

# calcula el prefix de zeros del target
def difficulty(sequence):
  count = 0
  for item in sequence:
    if item != "0":
      break
    count += 1
  return "0" * count

# Proof of Work
def proof_of_work(version, prev_hash, merkle_root, bits, target):
  is_end = False
  prefix = difficulty(target)
  while is_end != True:
    # calculem el nonce com un valor aleatori de 4 bytes en big endian
    nonce_big = secrets.token_hex(4)
    nonce_lit = big_endian_to_little_endian(nonce_big)
    timestamp_big = current_time_little_endian()
    timestamp_lit = big_endian_to_little_endian(timestamp_big)
    # concatenem els elements del header
    text = version + prev_hash + merkle_root + timestamp_lit + bits + nonce_lit
    # calcular hash
    text_bin = unhexlify(text)
    hash_block = sha256(sha256(text_bin).digest()).digest()
    result = hexlify(hash_block[::-1]).decode("utf-8")
    #print(result)
    if result.startswith(prefix):
      is_end = True
      print("nonce:", nonce_big)
      print("timestamp:", timestamp_big)
      return result


# VARIABLES
print("=== VARIABLES (big endian)")

# Version (4 bytes) - version = 1
version_big = "00000001"
version_lit = big_endian_to_little_endian(version_big)
print("version:", version_big)

# Previous hash (32 bytes) - Double sha256 of your first name = sha256(sha256("firstname"))
firstname = "silvia"
firstname_bin = firstname.encode('ascii')
firstname_hash = sha256(sha256(firstname_bin).digest()).digest()
prev_hash_big = firstname_hash.hex()
prev_hash_lit = big_endian_to_little_endian(firstname_hash)
print("prev_hash:", prev_hash_big)

# Merkle root (32 bytes)
merkle_root_big = "6dbba50b72ad0569c2449090a371516e3865840e905483cac0f54d96944eee28"
merkle_root_lit = big_endian_to_little_endian(merkle_root_big)
print("merkle_root:", merkle_root_big)

# Bits (4 bytes)
bits_big = "1e0fffff"
bits_lit = big_endian_to_little_endian(bits_big)
print("bits:", bits_big)

# Target
target = "00000fffff000000000000000000000000000000000000000000000000000000"


#RESULTS
print("=== RESULTS (big endian)")
begin = t.time()
result_hash = proof_of_work(version_lit, prev_hash_lit, merkle_root_lit, bits_lit, target)
calcul_time = t.time()- begin
print("hash:", result_hash)
print(round(calcul_time, 4),"s")
