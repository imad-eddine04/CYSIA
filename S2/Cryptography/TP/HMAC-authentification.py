import hmac
import hashlib

# Define a secret key for the HMAC
secret_key = b'my_secret_key'

# Define the message to be authenticated
message = b'my_message'
message2=b'message faux'

# Generate the HMAC for the message using the secret key and SHA-256 hashing algorithm
h = hmac.new(secret_key, message, hashlib.sha256)
print(h.hexdigest())

# Get the digest of the HMAC
hmac_digest = h.digest()

# Create a second HMAC object using the same secret key and message
h2 = hmac.new(secret_key, message2, hashlib.sha256)
print(h2.hexdigest())
# Compare the digests of the two HMAC objects to authenticate the message
if hmac.compare_digest(h.digest(), h2.digest()):
    print('Authentication successful!')
else:
    print('Authentication failed.')
