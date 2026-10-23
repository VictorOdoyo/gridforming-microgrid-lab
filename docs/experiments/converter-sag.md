# DC sag and inner-loop recovery

The sampled LC experiment regulates a 325 V peak dq reference. An artificial DC
supply sag from 700 V to 450 V reduces the circular SVPWM voltage ceiling from
about 404 V to 260 V. The commanded AC voltage therefore saturates.

The test checks the physical modulation limit at every tick, reduced output during
the sag, and voltage recovery after the link returns to 700 V. Both cascaded PI
loops include tracking anti-windup. This experiment imposes the DC sag externally;
the hybrid model instead calculates its DC voltage from stored energy.

Current and voltage loops are sampled; the continuous design bandwidth alone does
not guarantee the settling time. Load-step tests include the actual saturation
and recovery transient before evaluating final tracking error.
