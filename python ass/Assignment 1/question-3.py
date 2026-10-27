
import re

definitions = {
    "a": "10 + 5",
    "b": "a * 2",
    "c": "(b + 4) * 2"
}

memo = {}
visiting = set()


def evaluate(name):
    # Return cached value
    if name in memo:
        return memo[name]

   
    if name in visiting:
        raise ValueError("CYCLE")

    if name not in definitions:
        raise ValueError("INVALID")

    visiting.add(name)

    try:
        value = parse_expression(definitions[name])
        memo[name] = value
        return value
    finally:
        visiting.remove(name)


def parse_expression(expr):
    tokens = re.findall(r'\d+|[a-zA-Z_]\w*|[()+*-]|\S', expr)
    tokens = [t for t in tokens if not t.isspace()]
    pos = 0

    def factor():
        nonlocal pos

        if pos >= len(tokens):
            raise ValueError("INVALID")

        token = tokens[pos]
        pos += 1

        if token.isdigit():
            return int(token)

        if token == '(':
            value = expression()
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("INVALID")
            pos += 1
            return value

        if re.fullmatch(r'[a-zA-Z_]\w*', token):
            return evaluate(token)

        raise ValueError("INVALID")

    def term():
        nonlocal pos
        value = factor()

        while pos < len(tokens) and tokens[pos] == '*':
            pos += 1
            value *= factor()

        return value

    def expression():
        nonlocal pos
        value = term()

        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            right = term()

            if op == '+':
                value += right
            else:
                value -= right

        return value

   
    if ''.join(tokens) == '' or any(
        not re.fullmatch(r'\d+|[a-zA-Z_]\w*|[()+*-]', t)
        for t in tokens
    ):
        raise ValueError("INVALID")

    result = expression()

    if pos != len(tokens):
        raise ValueError("INVALID")

    return result

for variable in definitions:
    try:
        print(variable, "=", evaluate(variable))
    except ValueError as e:
        print(e)
        break
