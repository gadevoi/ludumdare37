import random
import string
import turtle

alphabet = ["F", "+", "-", "[", "]"]
rules = [("F", "FF-[-F+F+F]+[+F-F-F]")]
d = 10
δ = 22.5

tree = "F[+F][-F[-F]F]F[+F][-F]"
stack = []

turtle.color('black', 'green')
turtle.ht()
turtle.speed("fastest")


def interpret(c):
    if c == "[":
        stack.append((turtle.pos(), turtle.heading()))
    if c == "]":
        pos, heading = stack.pop()
        turtle.setpos(pos)
        turtle.seth(heading)
    if c == "F":
        turtle.fd(d)
    if c == "+":
        turtle.left(δ)
    if c == "-":
        turtle.right(δ)


def grow(tree, n):
    new_tree = tree
    for _ in range(n):
        for old, new in rules:
            new_tree = new_tree[::-1].replace(old[::-1], new[::-1], random.randint(1, 50))[::-1]

    return new_tree


def draw(tree):
    for c in tree:
        interpret(c)


def set(x, y):
    turtle.pu()
    turtle.setpos(x, y)
    turtle.seth(90)
    turtle.pd()


def random_mutation():
    i_gene = random.randrange(0, len(rules))
    i_letter = random.randrange(0, len(rules[i_gene][1]))
    new_rule = rules[i_gene][1][:i_letter]
    new_rule += random.choice(alphabet)
    new_rule += rules[i_gene][1][i_letter+1:]
    rules[i_gene] = rules[i_gene][0], new_rule
    print(new_rule)


i = 0
set(0, 0)
tree = "F[+F][-F[-F]F]F[+F][-F]"
draw(tree)

turtle.done()