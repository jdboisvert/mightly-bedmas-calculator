from enum import IntEnum


class OperatorWeight(IntEnum):    
    BRACKET_WEIGHT = 4
    EXPONENT_WEIGHT = 3
    DIVISION_MULTIPLICATION_WEIGHT = 2
    ADDITION_SUBTRACTION_WEIGHT = 1

