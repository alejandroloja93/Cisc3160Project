import sys
import lexer as clex
import tok as token

class Node:
#asDict() converts an instance into a dictionary
    def asdict(self):
        return {}  # pragma: no cover


class ValueNode(Node):

    node_type = 'value_node'

    def __init__(self, value):
        self.value = value

    def asdict(self):
        return {
            'type': self.node_type,
            'value': self.value
        }
#Following nodes that we will return to the visitor
#All of these nodes will take ValueNode class node
#For Integers
class IntegerNode(ValueNode):
    node_type = 'integer'

    def __init__(self, value):
        self.value = int(value)

#To print out Literals
class LiteralNode(ValueNode):

    node_type = 'literal'
    #def __init__(self, value):
    #    self.value = value
#To print out Variables
class VariableNode(ValueNode):

    node_type = 'variable'
    #def __init__(self, value):
    #    self.value = str(value)

#For binary nodes
class BinaryNode(Node):

    node_type = 'binary'

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def asdict(self):
        result = {
            'type': self.node_type,
            'left': self.left.asdict()
        }

        result['right'] = None
        if self.right:
            result['right'] = self.right.asdict()

        result['operator'] = None
        if self.operator:
            result['operator'] = self.operator.asdict()

        return result
#For negative values
class UnaryNode(Node):

    node_type = 'unary'

    def __init__(self, operator, content):
        self.operator = operator
        self.content = content

    def asdict(self):
        result = {
            'type': self.node_type,
            'operator': self.operator.asdict(),
            'content': self.content.asdict()
        }

        return result

class AssignmentNode(Node):

    node_type = 'assignment'

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value

    def asdict(self):
        return {
            'type': self.node_type,
            'variable': self.variable.value,
            'value': self.value.asdict(),
        }

#Parses integers, symbols, expressions etc...
class cParser:

    def __init__(self):
        self.lexer = clex.Lexer()

    def parse_literal(self):
        t = self.lexer.get_token()
        return LiteralNode(t.value)

    def parse_integer(self):
        t = self.lexer.get_token()
        return IntegerNode(t.value)

    def _parse_variable(self):
        t = self.lexer.get_token()
        return VariableNode(t.value)
#Assignment is able to have a variable as its left member and expression as right
#This is how I am able to add
    def parse_factor(self):
        next_token = self.lexer.peek_token()

        if next_token.type == clex.LITERAL and next_token.value in ['-', '+']:
            operator = self.parse_literal()
            factor = self.parse_factor()
            return UnaryNode(operator, factor)

        if next_token.type == clex.LITERAL and next_token.value == '(':
            self.lexer.discard_type(clex.LITERAL)
            expression = self.parse_expression()
            self.lexer.discard_type(clex.LITERAL)
            return expression


        if next_token.type == clex.NAME:
            t = self.lexer.get_token()
            return VariableNode(t.value)

        return self.parse_integer()
#This is how i am able to multiply or divide
    def parse_term(self):
        left = self.parse_factor()

        next_token = self.lexer.peek_token()

        while next_token.type == clex.LITERAL\
         and next_token.value in ['*', '/']:
            operator = self.parse_literal()
            right = self.parse_integer()

            left = BinaryNode(left, operator, right)

            next_token = self.lexer.peek_token()

        return left
#Takes the operation with the highest precendence
    def parse_expression(self):
        left = self.parse_term()

        next_token = self.lexer.peek_token()

        while next_token.type == clex.LITERAL\
         and next_token.value in ['+', '-']:
            operator = self.parse_literal()
            right = self.parse_term()

            left = BinaryNode(left, operator, right)

            next_token = self.lexer.peek_token()

        return left
#Able to assign variables and discard types
    def parse_assignment(self):
        variable = self._parse_variable()
        self.lexer.discard(token.Token(clex.LITERAL,'='))
        value = self.parse_expression()

        return AssignmentNode(variable, value)
#The line the complier will read and print to the output
    def parse_line(self):
        try:
            self.lexer.stash()
            return self.parse_assignment()
        except clex.TokenError:
            self.lexer.pop()
            return self.parse_expression()
