# Regenerative DC operation

The coupled DC plant uses signed inductor current. Negative inverter DC demand
injects energy into the capacitor; the voltage regulator requests negative battery
current, and the bidirectional converter transfers energy back into the pack.

The regression supplies 30 kW for 0.3 s. It checks increasing SOC, negative final
battery current, positive dissipative heat, and independent chemical/storage/load
energy closure. Charging uses unit coulomb efficiency in this physical energy
audit; empirical coulomb efficiency is available separately in electrochem.py.

This is an averaged converter experiment with held duty commands. It does not
model switching ripple, dead-time, or electrochemical aging.
