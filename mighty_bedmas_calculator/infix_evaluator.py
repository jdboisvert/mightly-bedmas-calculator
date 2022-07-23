from collections import deque
from decimal import Decimal
from multiprocessing.sharedctypes import Value

from mighty_bedmas_calculator.operator import get_weight, is_operator

def evaluate(infix_expression: str) -> str:
    postfix_expression = __convert_infix_to_postfix(infix_expression)
    result = __evaluate_postfix_expression(postfix_expression)
    
    return result

def __convert_infix_to_postfix(infix_expression: str):
    last_character = infix_expression[-1]
    if is_operator(last_character) and last_character != ")":
        raise ValueError("Expression cannot end with an operator.")
    
    operators_stack = deque()
    postfix_queue = deque()
    
    previous_value = ""
        
    for value in infix_expression:
        if value == " ":
            # Skip white space 
            continue
        
        value_is_numeric = value.isdecimal()
        value_is_an_operator = is_operator(value)
        
        if not value_is_numeric and not value_is_an_operator:
            raise ValueError(f"{value} in expression is not valid")
        
        if value_is_numeric:
            if previous_value.isdecimal():
                # TODO validate
                raise ValueError("Previous value was numeric therefore a binary expression")
            
            if previous_value == ")":
                # Check if it is (2+2)4 which means an implied multiplication (2+2)*4
                __apply_precedence_logic(postfix_queue, operators_stack, "*")
            
            postfix_queue.append(value)
                
        elif value == "(":
            if previous_value:
                if previous_value == ")" or previous_value.isdecimal():
                    __apply_precedence_logic(postfix_queue, operators_stack, "*")
                    
            if previous_value in ["+", "-"]:
              # Means the -1 or +1 is implied on bracket
              postfix_queue.append("1")
              
            operators_stack.append(value)
                                
        elif value == ")":
            if not operators_stack:
                raise ValueError("Attempted to close a bracket but there is no pairing open bracket since there are no other operators")
            
            while operators_stack and operators_stack[-1] != "(":
                # Pop everything off stack until opening bracket is found
                operator_from_stack = operators_stack.pop()
                postfix_queue.append(operator_from_stack)
                
            if not operators_stack:
                raise ValueError("Attempted to close a bracket but there is no pairing open bracket")
            
            # Remove open bracket "("
            operators_stack.pop()
            
        
        elif value_is_an_operator:
            if previous_value and not previous_value.isdecimal() and previous_value != ")":
                # If the previous result is blank or not a number then non binary operation.
                # This does not include ')' since (2+2)*5 is valid.
                raise ValueError("Non binary operation.")
                                
            __apply_precedence_logic(postfix_queue, operators_stack, value)      
                
        previous_value = value
    
    
    if "(" in operators_stack or "(" in postfix_queue:
        raise ValueError("Equation is missing a closing bracket.")
    
    while operators_stack:
        operator_from_stack = operators_stack.pop()
        postfix_queue.append(operator_from_stack)
    
    return "".join(postfix_queue) # expecting 23+4^ from (2+3)^4"
    
def __apply_precedence_logic(postfix_queue: deque, operators_stack: deque, operator: str) -> None:
    if not operators_stack:
        operators_stack.append(operator)
        return 
    
    if get_weight(operator) > get_weight(operators_stack[-1]):
        operators_stack.append(operator)
        return 
    
    while operators_stack and (get_weight(operator) <= get_weight(operators_stack[-1])) and operators_stack[-1] != "(":
        operator_from_stack = operators_stack.pop()
        postfix_queue.append(operator_from_stack)
        
    
    operators_stack.append(operator)
    
    
def __evaluate_postfix_expression(postfix_expression: str) -> str:
        # Deque<Double> operands = new ArrayDeque<>();
        operands_stack = deque()
        
        for value in postfix_expression:
            __perform_evaluation_step(operands_stack, value)
            
        if len(operands_stack) != 1:
            raise ValueError("Result contains more than one value")
        
        return operands_stack.pop()
    
    
def __perform_evaluation_step(operands_stack: deque, value: str) -> None:
        if not value.isdecimal():
            # An operator 
            right_operand = operands_stack.pop()
            left_operand = operands_stack.pop()
            
            result = __evaluate_operands(left_operand, right_operand, operator=value)
            operands_stack.append(result)
            return
        
        operands_stack.append(value)
        
        
def __evaluate_operands(left_operand: str, right_operand: str, operator: str) -> str:
        if right_operand == "0" and operator == "/":
            raise ValueError("Attempting to divide by 0")
        
        left_operand_decimal = Decimal(left_operand)
        right_operand_decimal = Decimal(right_operand)
        
        if operator == "+":
            return str(left_operand_decimal + right_operand_decimal)
        
        if operator == "-":
            return str(left_operand_decimal - right_operand_decimal)
        
        if operator == "*":
            return str(left_operand_decimal * right_operand_decimal)
        
        if operator == "/":
            return str(left_operand_decimal / right_operand_decimal)
        
        if operator == "^":
            return str(left_operand_decimal ** right_operand_decimal)





    
