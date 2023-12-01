# QODA
Quantum Outlier Detection Algorithm (QODA)

The Quantum Outlier Detection Algorithm (QODA) is a hybrid quantum-classical method for solving the Outlier Detection problem. It is inspired by the classical Angle Based Outlier Detection (ABOD) algorithm, which, given a dataset record $p$, computes the angles between each other pair of dataset records $a$ and $b$ ($\hat{apb}$). Then, ABOD computes the variance of these angles. If the variance is low, $p$ is highly likely an outlier. QODA mimics the behavior of ABOD, but instead of computing the variance of the angles, it computes the variance of the differences of the components, where the records are properly normalized with the *Inverse Stereographic Projection (ISP)*. This heuristic is supported by theoretical analysis.

QODA uses [QVAR](https://github.com/AlessandroPoggiali/QVAR) to compute the variance within a quantum circuit, where the initial state contains all the differences between the components of every record. 

## Quickstart

To run a simple demostration of the QODA, follow these steps:
* Make sure you have Qiskit installed on your computer
* Install the QVAR package `pip install -i https://test.pypi.org/simple/ QVAR` (the PyPI version is not available yet)
* Clone this repo with `git clone https://github.com/AlessandroPoggiali/QODA.git`
* Navigate to the HQFS directory and run the command `python3 test.py`

The `test.py` file contains code that will run QODA on a very simple dataset.
