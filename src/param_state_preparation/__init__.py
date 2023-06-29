from __future__ import annotations
# MIT License
# Copyright (c) 2023 Evandro Chagas Ribeiro da Rosa
from ket import quant, control, RY
from math import asin, sqrt


class ParamTree:
    def __init__(self, params):
        assert (len(params)).bit_count() == 1

        total = sum(params)
        if total != 0:
            params = [p/total for p in params]

        left_params = params[:len(params)//2]
        right_params = params[len(params)//2:]

        self.value = 2*asin(sqrt(sum(right_params)))

        if len(params) > 2:
            self.left = ParamTree(left_params)
            self.right = ParamTree(right_params)
        else:
            self.left = None
            self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def __repr__(self) -> str:
        return f'{self.value} {self.left} {self.right}' if not self.is_leaf() else f'{self.value}'


def prepare(q: quant, params: ParamTree | list[float | int]):
    if not isinstance(params, ParamTree):
        params = ParamTree(params)

    head, tail = q[0], q[1:]

    RY(params.value, head)

    if params.is_leaf():
        return
    with control(head, on_state=0):
        prepare(tail, params.left)
    with control(head):
        prepare(tail, params.right)
