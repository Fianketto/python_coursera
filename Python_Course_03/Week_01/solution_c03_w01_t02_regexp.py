def calculate(data, findall):
    reg = r"([abc])([+-]?=)([abc]?)([+-]?\d*)"
    matches = findall(reg)  # Если придумать хорошую регулярку, будет просто
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        if s == "=":
            data[v1] = data.get(v2, 0) + int(n or 0)
        elif s[0] == "+":
            data[v1] = data.get(v1, 0) + data.get(v2, 0) + int(n or 0)
        elif s[0] == "-":
            data[v1] = data.get(v1, 0) - data.get(v2, 0) - int(n or 0)
        print(v1, s, v2, n)
    return data
