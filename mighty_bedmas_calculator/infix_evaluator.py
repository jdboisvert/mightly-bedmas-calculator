from collections import deque
from multiprocessing.sharedctypes import Value

from mighty_bedmas_calculator.operator import get_weight, is_operator

def evaluate(infix_expression: str) -> str:
    postfix_expression = __convert_infix_to_postfix(infix_expression)
    return postfix_expression

def __convert_infix_to_postfix(infix_expression: str):
    if is_operator(infix_expression[-1]):
        raise ValueError("Equestion cannot end with an operator.")
    
    operators_stack = deque()
    postfix_queue = deque()
    
    previous_value = ""
        
    for value in infix_expression:
        if value == " ":
            # Skip white space 
            continue
        
        value_is_numeric = value.isdecimal()
        
        if not value_is_numeric and not is_operator(value):
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
            
            while operators_stack and not operators_stack[0] == "(":
                # Pop everything off stack until opening bracket is found
                operator_from_stack = operators_stack.pop()
                postfix_queue.append(operator_from_stack)
                
            if not operators_stack:
                raise ValueError("Attempted to close a bracket but there is no pairing open bracket")
            
            # Remove open bracket "("
            operators_stack.pop()
                    
        if not previous_value.isdecimal() and previous_value != ")":
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
    
    return "".join(postfix_queue)
    
def __apply_precedence_logic(postfix_queue: deque, operators_stack: deque, operator: str) -> None:
    if not operators_stack:
        operators_stack.append(operator)
        return 
    
    if get_weight(operator) > get_weight(operators_stack[0]):
        operators_stack.append(operator)
        return 
    
    while operators_stack and (get_weight(operator) <= get_weight(operators_stack[0])) and operators_stack[0] != "(":
        operator_from_stack = operators_stack.pop()
        postfix_queue.append(operator_from_stack)
        
    
    operator_from_stack.append(operator)


    
