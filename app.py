from math import asin, sqrt
from ket import *
import plotly.express as px
import streamlit as st


class ParamTree:
    def __init__(self, *params):
        assert (len(params)).bit_count() == 1

        total = sum(params)
        if total != 0:
            params = [p/total for p in params]

        left_params = params[:len(params)//2]
        right_params = params[len(params)//2:]

        self.value = 2*asin(sqrt(sum(right_params)))

        if len(params) > 2:
            self.left = ParamTree(*left_params)
            self.right = ParamTree(*right_params)
        else:
            self.left = None
            self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def __repr__(self) -> str:
        return f'{self.value} {self.left} {self.right}' if not self.is_leaf() else f'{self.value}'


def prepare(q: quant, params: ParamTree):
    head, tail = q[0], q[1:]

    RY(params.value, head)

    if params.is_leaf():
        return
    with control(head, on_state=0):
        prepare(tail, params.left)
    with control(head):
        prepare(tail, params.right)


st.sidebar.write("# Number of Qubits")

num_qubits = st.sidebar.slider("Number of qubits", 1, 10, 3)

st.sidebar.write("# Quantum State")

parameters = [st.sidebar.slider(
    f"|{i:0{num_qubits}b}⟩", 0, 100, 50) for i in range((1 << num_qubits))]

q = quant(num_qubits)
params = ParamTree(*parameters)

prepare(q, params)

d = dump(q)

df = {
    'State': [f'|{s:0{num_qubits}b}⟩' for s in d.states],
    'Probability': d.probabilities,
}

fig = px.bar(df, x='State', y='Probability')
fig.update_layout(yaxis_range=[0, 1])

st.plotly_chart(fig, use_container_width=True)
