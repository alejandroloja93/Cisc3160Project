import sys
class Visitor:

    def __init__(self):
        self.variables = {}

    def isvariable(self, name):
        return name in self.variables
#Finds the value of the token
    def valueof(self, name):
        return self.variables[name]['value']
#Finds the type of the token 
    def typeof(self, name):
        return self.variables[name]['type']

    def visit(self, node):
#Checks if node is an Integer
        if node['type'] == 'integer':
            return node['value'], node['type']

        if node['type'] == 'variable':
            return self.valueof(node['value']), self.typeof(node['value'])
#For a unary value
        if node['type'] == 'unary':
            operator = node['operator']['value']
            cvalue, ctype = self.visit(node['content'])

            if operator == '-':
                return - cvalue, ctype

            return cvalue, ctype
#For operations such as addition, subtraction,etc..
        if node['type'] == 'binary':
            lvalue, ltype = self.visit(node['left'])
            rvalue, rtype = self.visit(node['right'])

            operator = node['operator']['value']

            if operator == '+':
                return lvalue + rvalue, rtype
            elif operator == '-':
                return lvalue - rvalue, rtype
            elif operator == '*':
                return lvalue * rvalue, rtype
            elif operator == '/':
                return lvalue // rvalue, rtype

        if node['type'] == 'assignment':
            right_value, right_type = self.visit(node['value'])
            self.variables[node['variable']] = {
                'value': right_value,
                'type': right_type
            }

            return None, None
