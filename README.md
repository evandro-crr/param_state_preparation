# Arbitrary State Preparation

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://statepreparation.streamlit.app)

Algorithm for arbitrary quantum state preparation implemented in [Ket](https://quantumket.org).

## Interactive Demo

<https://statepreparation.streamlit.app>

## Install

```shell
pip install git+https://github.com/evandro-crr/param_state_preparation.git
```

## Example

```py
from ket import *
from param_state_preparation import prepare

num_qubits = 3
parameters = [2**i for i in range(2**num_qubits)]

q = quant(num_qubits)
prepare(q, parameters)

d = dump(q)
print(d.show())
```
