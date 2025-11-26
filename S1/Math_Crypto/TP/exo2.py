a=int(input("donner un nombre: "))
b=int(input("donner un nombre: "))

if b==0:
    print("le diviseur né pas 0.")
else:
    if a < 0:
        a = a * -1

    if b < 0:
        b = b * -1
    if a > b:
        c=a%b
    if a < b:
        c=b%a
print("a modelo b est ",a,"[",b,"] est : ",c)
