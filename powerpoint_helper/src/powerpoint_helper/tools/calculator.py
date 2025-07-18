from langchain.tools import tool

class CalculatorTools():

    @tool("Make a calculation")
    def calculate(operation):
        try:
            return eval(operation)
        except SyntaxError:
            return "Error: Invalid syntax in the operation."