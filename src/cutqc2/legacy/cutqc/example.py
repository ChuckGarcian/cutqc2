import os, math, logging
from cutqc.main import CutQC
from helper_functions.benchmarks import generate_circ

def supremacy():  
  num_qubits=6
  circuit = generate_circ(
      num_qubits=num_qubits,
      depth=1,
      circuit_type="supremacy",
      reg_name="q",
      connected_only=True,
      seed=None,
  )
  
  import math
  
  cutter_constraints = {
          "max_subcircuit_width":  math.ceil(circuit.num_qubits / 4 * 3),
          "max_subcircuit_cuts": 10,
          "subcircuit_size_imbalance": 2,
          "max_cuts": 10,
          "num_subcircuits": [3]
      } 
  return circuit, cutter_constraints

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="example.log",
        filemode="w",
    )

    circuit, cutter_constraints = supremacy ()
    cutqc = CutQC(
        circuit=circuit,
        cutter_constraints=cutter_constraints,
        verbose=True,
    )
    cutqc.cut()
    cutqc.evaluate(num_shots_fn=None)
    cutqc.build(mem_limit=32, recursion_depth=1)
    cutqc.verify()
    logging.info(f"Cut: {cutqc.num_recursions} recursions.")
    logging.info(cutqc.approximation_bins)
