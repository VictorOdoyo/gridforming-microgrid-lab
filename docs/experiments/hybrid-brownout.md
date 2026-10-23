# Coupled battery outage

A battery contactor trip removes chemical supply without erasing inductor energy.
The dump path dissipates residual DC/DC inductor energy. The capacitor continues
to supply the inverter until the gate supervisor detects low DC voltage.

Blocking the average bridge sets its AC voltage command to zero; LC stored energy
then dissipates into its resistor and passive load. Gate blocking remains latched.
This is an illustrative averaged freewheel/isolation model, not a detailed diode,
fault-current, or gate-driver implementation.

The regression checks source disconnection, positive remaining DC energy, AC
voltage decay, and whole-system chemical-to-load energy balance.
