
class InvalidFormat(Exception):
    pass

class UnknownVariable(Exception):
    pass

class DivisionByZero(Exception):
    pass

class UnsupportedOperator(Exception):
    pass


variables = {}

def get_value(x):
    try:
        return float(x)
    except ValueError:
        if x in variables:
            return variables[x]
        raise UnknownVariable("Unknown variable: " + x)


def calculate(formula):
    parts = formula.split()

    if len(parts) != 3:
        raise InvalidFormat("Enter: operand operator operand")

    a, op, b = parts

    x = get_value(a)
    y = get_value(b)

    if op == "+":
        return x + y
    elif op == "-":
        return x - y
    elif op == "*":
        return x * y
    elif op == "/":
        if y == 0:
            raise DivisionByZero("Cannot divide by zero")
        return x / y
    elif op == "%":
        if y == 0:
            raise DivisionByZero("Cannot use modulo with zero")
        return x % y
    else:
        raise UnsupportedOperator("Unsupported operator: " + op)


while True:
    formula = input("Enter formula (or quit): ")

    if formula.lower() == "quit":
        break

    try:
        # Store result using: variable = operand operator operand
        if "=" in formula:
            name, expression = formula.split("=", 1)
            name = name.strip()

            if not name.isidentifier():
                raise InvalidFormat("Invalid variable name")

            result = calculate(expression.strip())
            variables[name] = result
        else:
            result = calculate(formula)

        print("Result:", result)

    except InvalidFormat as e:
        print("Invalid Format:", e)
    except UnknownVariable as e:
        print("Unknown Variable:", e)
    except DivisionByZero as e:
        print("Division by Zero:", e)
    except UnsupportedOperator as e:
        print("Unsupported Operator:", e)
