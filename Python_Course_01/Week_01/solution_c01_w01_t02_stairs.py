import sys

stair_count = int(sys.argv[1])
my_string = ""
for i in range(stair_count):
    my_string += " " * (stair_count - i - 1) + "#" * (i + 1) + "\n"

print(my_string)
