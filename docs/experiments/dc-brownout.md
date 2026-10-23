# Energy-limited operation

With battery contactors open, the load draws only from DC capacitor energy.
The analytically predicted brownout time is:

    t = (Uinitial - 0.5 C Vminimum²) / Pload

The DC driver stops at the first control tick below minimum voltage. It reports
the termination reason and never silently claims the requested duration was served.
A regression compares this sampled detection time against the analytical result.

Opening the contactor routes existing converter-inductor energy to the modeled
dump resistor. Battery current becomes zero while inductor current decays.
