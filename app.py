from math import pi
from ket import *
import plotly.express as px
import streamlit as st


class ParamTree:
    def __init__(self, *params):
        assert (len(params)+1).bit_count() == 1

        self.value = params[0]
        params = params[1:]

        if len(params) > 1:
            left_list = params[:len(params)//2]
            right_list = params[len(params)//2:]
            self.left = ParamTree(*left_list)
            self.right = ParamTree(*right_list)
        else:
            self.left = None
            self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def __repr__(self) -> str:
        return f'{self.value} {self.left} {self.right}' if not self.is_leaf() else f'{self.value}'


def preparer(q: quant, params: ParamTree):
    head, tail = q[0], q[1:]

    RX(params.value, head)

    if params.is_leaf():
        return
    with control(head, on_state=0):
        preparer(tail, params.left)
    with control(head):
        preparer(tail, params.right)


st.sidebar.write("# Number of Qubits")

num_qubits = st.sidebar.slider("Number of qubits", 1, 10, 3)

st.sidebar.write("# Parameters")

parameters = [st.sidebar.slider(
    f"Parameter {i}", 0.0, pi, pi/2) for i in range((1 << num_qubits)-1)]

q = quant(num_qubits)
params = ParamTree(*parameters)

preparer(q, params)

d = dump(q)

df = {
    'State': [f'|{s:0{num_qubits}b}>' for s in d.states],
    'Probability': d.probabilities,
}

fig = px.bar(df, x='State', y='Probability')
fig.update_layout(yaxis_range=[0, 1])

st.plotly_chart(fig, use_container_width=True)
