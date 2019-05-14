
import sys
import Cparser as cpar
import visitor as cvis


def main():
    p = cpar.cParser()
    v = cvis.Visitor()

    while True:
        try:
            text = input('userinput :> ')
            p.lexer.load(text)

            node = p.parse_line()
            res = v.visit(node.asdict())

            print(res)

        except EOFError:
            print("Bye!")
            break

        if not text:
            continue


if __name__ == '__main__':
    main()
