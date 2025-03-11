#!/usr/bin/env python3
import operator

ops = {
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '-=': operator.isub,
    '+=': operator.iadd,
    '*=': operator.imul,
    '/=': operator.itruediv,
    '=': None,
}
