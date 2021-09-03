import sys
import turtle


def rewrite(n, axiom, productions):
    """Produce the final list of commands after all replacements.

    Start by setting the axiom as the final string. With every iteration,
    replace each symbol with the string that is mapped to them in the
    productions dictionary.

    If the symbol is a constant that cannot be replaced, add it to the string
    as it is (this is the case for '+' and '-').

    For example: given an axiom F-F-F-F and a production F->FF-F, the first
    iteration would replace each 'F' in the axiom with the string 'FF-F',
    resulting in this new string: F->FF-F-F->FF-F-F->FF-F-F->FF-F. The second
    iteration would replace each 'F' in that new string with the string 'FF-F',
    and so on...
    """
    final_string = axiom
    for _ in range(n):
        s = ""  # String to be built
        for symbol in final_string:
            if symbol in productions:  # Replace
                s += productions[symbol]
            else:  # Constant
                s += symbol
        final_string = s
    return final_string


def draw(distance, angle, commands_list):
    """Execute the commands represented by each symbol in the list."""
    stack = []
    for command in commands_list:
        if command in ["F", "l", "r"]:  # l is F_l, r is F_r
            # Move forward a step of length 'distance'
            turtle.forward(distance)

        elif command == "f":
            # Move forward a step of length 'distance' without drawing a line
            turtle.penup()
            turtle.forward(distance)
            turtle.pendown()

        elif command == "+":
            turtle.left(angle)

        elif command == "-":
            turtle.right(angle)

        elif command == "L" or command == "R":
            pass

        elif command == "[":
            # Push the current state of the turtle (position and orientation)
            # onto a stack
            stack.append((turtle.pos(), turtle.heading()))

        elif command == "]":
            # Pop the last state in the stack and make it the current state
            new_position, new_orientation = stack.pop()
            turtle.penup()
            turtle.goto(new_position)
            turtle.setheading(new_orientation)
            turtle.pendown()


def main():
    # Get parameters from input file
    try:
        filename = sys.argv[1]
    except IndexError:
        raise SystemExit(f"Missing input file!\nUsage: {sys.argv[0]} <input_file>")

    with open(filename) as f:
        parameters = list(s.rstrip("\n") for s in f.readlines())

    n, d, delta = int(parameters[0]), int(parameters[1]), float(parameters[2])
    axiom = parameters[3]

    # Store the list of productions/rewriting rules in a dictionary
    productions = {}
    for p in parameters[4:]:
        k, v = p.split("->")
        productions[k] = v

    # Turtle settings
    turtle.Screen().screensize(4000, 3000)
    turtle.Screen().setup(1200, 900)
    turtle.pen(shown=False)
    turtle.left(90)  # Set initial orientation to the positive y-axis

    final_string = rewrite(n, axiom, productions)

    draw(d, delta, final_string)

    # Save output in a file
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file=filename.replace(".txt", ".eps"))
    turtle.done()


if __name__ == "__main__":
    main()
