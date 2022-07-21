# -*- coding: utf-8 -*-

"""Odyssey Settings: Manage Odyssey settings without manually editing JSON.."""

__author__ = """Jeffrey Boisvert"""
__email__ = "info.jeffreyboisvert@gmail.com"

from . import infix_evaluator
from . import operator

# any functions from backend you want to expose should be
# imported above and added to the list below.
__all__ = [
    "infix_evaluator",
    "operator"
]