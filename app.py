from ket import quant, dump, quantum_code_last
import plotly.express as px
import streamlit as st
from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate, XGate
from param_state_preparation import prepare

st.set_page_config(
    page_title="Arbitrary Quantum State Preparation",
    page_icon="https://quantumket.org/_static/ket.svg",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.sidebar.write("# Number of Qubits")

num_qubits = st.sidebar.slider("Number of qubits", 1, 10, 3)

st.sidebar.write("# Quantum State")

parameters = [st.sidebar.slider(
    f"|{i:0{num_qubits}b}⟩", 0, 100, 50) for i in range((1 << num_qubits))]


"# Arbitrary Quantum State Preparation"

":arrow_left: Open the sidebar to change the number of qubits and the states probability."

q = quant(num_qubits)
prepare(q, parameters)

d = dump(q)

df = {
    'State': [f'|{s:0{num_qubits}b}⟩' for s in d.states],
    'Probability': d.probabilities,
}

fig = px.bar(df, x='State', y='Probability')
fig.update_layout(yaxis_range=[0, 1])

st.plotly_chart(fig, use_container_width=True)

qc = QuantumCircuit(num_qubits)

for instruction in quantum_code_last()[0]['instructions']:
    if 'Gate' in instruction:
        gate = instruction['Gate']
        target = gate['target']
        controls = gate['control']
        if isinstance(gate['gate'], dict):
            gate = RYGate(gate["gate"]["RY"])
        else:
            gate = XGate()

        if len(controls) != 0:
            gate = gate.control(len(controls))

        qc.append(gate, [*controls, target])

st.pyplot(qc.draw(output='mpl', style={"backgroundcolor": "#F4F8FF"}))

"---"

"Made with"
"[![ket](https://quantumket.org/_static/ket.svg)](https://quantumket.org)"
