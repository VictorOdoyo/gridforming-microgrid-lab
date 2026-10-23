# Load sharing under a step

Run the load-step case with two identical voltage sources behind equal impedances.
At 2 seconds, load admittance increases by 50 percent. This is an impedance-load
step: actual power also depends on bus voltage.

Symmetry requires equal complex power from both sources at every sample.
The settled common deviation obeys df = mp * (Pref - P) for each source.
Primary control alone leaves a steady frequency offset. Source terminal power
excludes copper losses inside each source impedance.

The regression checks equality of source injections and network KCL.
