# convert chars to hex , in 0-F

t = "DEADBEEF"
a = "0123456789ABCDEF"
# TODO convert me to asm
def hex_convert(s,l=0):
    if l==0:
        l = len(s)
    num = 0 
    for i in s[0:l]:
        print(i,":",end="")
        val = ord(i)
        print(val)
        if val >= 65:
            if val <= 70:
                val = val - 55
                print(val)
                num = num << 4
                num = num | val
        elif val >= 48 : # starts at zero
            if val <= 56: # ends at nine
                val = val - 48 
                print(val)
                num = num << 4
                num = num | val
    print(num)

print('--- allchar ---')
hex_convert(a)
print('--- moo ---')
hex_convert('00FF')
