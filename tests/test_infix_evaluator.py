#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `infix_evaluator` package."""

from mighty_bedmas_calculator.infix_evaluator import evaluate


def test_evaluate_addition():
    assert evaluate("2+2")  == "4"
    assert evaluate("(2+5)")   == "7"
    assert evaluate("(22+5)")   == "27"
    assert evaluate("(-1+5)")   == "4"
    
def test_evaluate_subtraction():
    assert evaluate("2-2")  == "0"
    assert evaluate("(2-5)")   == "-3"
    assert evaluate("22-5")   == "17"
    assert evaluate("(-1-5)")   == "-6"
    
def test_evaluate_multiplcation():
    assert evaluate("2*2")  == "4"
    assert evaluate("(2*5)")   == "10"
    assert evaluate("2(22+5)")   == "54"
    assert evaluate("(-1*5)")   == "-5"
    
def test_evaluate_division():
    assert evaluate("2/2")  == "1"
    assert evaluate("(10/5)")   == "2"
    assert evaluate("(-1/5)")   == "-0.2"
    
def test_evaluate_exponent():
    assert evaluate("2^2")  == "4"
    assert evaluate("(10^5)")   == "100000"
    assert evaluate("(-1^5)")   == "-1"
    
def test_evaluate_brackets():
    assert evaluate("(2*2)(2*2)")  == "16"
    assert evaluate("3(2*2)(2*2)")  == "48"
    assert evaluate("-5(2*2)(2*2)")  == "-80"
    assert evaluate("-5(2*2)(2*2)3")  == "-240"
    assert evaluate("-5*(2*2)(2*2)*3")  == "-240"