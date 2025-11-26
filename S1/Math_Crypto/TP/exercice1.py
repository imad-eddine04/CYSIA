def pgcd(a, b):

    if b == 0:
        return (a, 1, 0)
    else:
        d, x1, y1 = pgcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (d, x, y)

def sol_par(a, b, c):
    d, x, y = pgcd(a, b)
    if c % d != 0:
        print("Pas de solution entière car c n’est pas multiple du pgcd(a, b).")
        return None
    x0 = x * (c // d)
    y0 = y * (c // d)
    return (x0, y0)

a = int(input("Entrez a : "))
b = int(input("Entrez b : "))
c = int(input("Entrez c : "))

sol = sol_par(a, b, c)
if sol:
    print(f"Une solution particulière est : x0 = {sol[0]}, y0 = {sol[1]}")

