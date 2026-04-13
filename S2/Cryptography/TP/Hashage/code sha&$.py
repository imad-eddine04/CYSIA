
import struct

def sha0_compress(h, m):
    w = [0] * 80
    for i in range(16):
        w[i] = struct.unpack('>I', m[i*4:i*4+4])[0]
    for i in range(16, 80):
        w[i] = (w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]) << 1
    a, b, c, d, e = h
    for i in range(80):
        if i < 20:
            f = (b & c) | ((~b) & d)
            k = 0x5A827999
        elif i < 40:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif i < 60:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6
        a, b, c, d, e = ((a << 5) & 0xffffffff) + f + e + k + w[i], a, (b << 30) & 0xffffffff, c, d
    return [(h[i] + x) & 0xffffffff for i, x in enumerate([a, b, c, d, e])]

def sha1_compress(h, m):
    w = [0] * 80
    for i in range(16):
        w[i] = struct.unpack('>I', m[i*4:i*4+4])[0]
    for i in range(16, 80):
        w[i] = (w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]) << 1
    a, b, c, d, e = h
    for i in range(80):
        if i < 20:
            f = (b & c) | ((~b) & d)
            k = 0x5A827999
        elif i < 40:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif i < 60:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6
        a, b, c, d, e = ((a << 5) & 0xffffffff) + f + e + k + w[i], b, ((c << 30) & 0xffffffff) + a, d, e
    return [(h[i] + x) & 0xffffffff for i, x in enumerate([a, b, c, d, e])]

# SHA0 collision example
h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
m0 = b'\x65\xc2\x4f\x5c\x0c\x0f\x89\xf6\xd4\x78\xde\x77\xef\x25\x52\x45\x83\xae\x3a\x4d\xb8\x2f\x13\xf4\xd8\x50\x1d\xf1\xbe\x57\xe7\xea\xec\x55\x7a\x48\x50\x3b\x77\x2e\x71\x50\x9e\x21\x95\x0b\x30\x6c\x8a\xb3\xb6\x93\x69\xfa\xbc\x8d\x9e\xe3\xca\x6b\x5c\x1f\xca\x35\x7a'
h0 = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
h1 = sha0_compress(h0, m0)
h2 =sha1_compress(h0,m0)
print(h1)
print(h2)
