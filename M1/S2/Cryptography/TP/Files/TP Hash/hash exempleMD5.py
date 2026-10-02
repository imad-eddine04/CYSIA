import hashlib

# =====================================================
# 1️ Hachage d'une chaîne avec SHA-256
# =====================================================

msg = "Hello, world!"
sha256_hash = hashlib.sha256(msg.encode()).hexdigest()

print("SHA-256('Hello, world!') :")
print(sha256_hash)
print()

# =====================================================
# 2️ Hachage MD5 de deux fichiers en collision
# =====================================================

s1 = bytes.fromhex(
    "d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5b"
    "d8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70"
)

s2 = bytes.fromhex(
    "d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f89"
    "55ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5b"
    "d8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0"
    "e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70"
)

print("MD5(s1) =", hashlib.md5(s1).hexdigest())
print("MD5(s2) =", hashlib.md5(s2).hexdigest())
print("s1 == s2 ?", s1 == s2)
print("hs1 == hs2 ?", hashlib.md5(s1).hexdigest() == hashlib.md5(s2).hexdigest())