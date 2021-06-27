import sys

digit_string = sys.argv[1]
s = 0
for d in digit_string:
    s += int(d)

print(s)
