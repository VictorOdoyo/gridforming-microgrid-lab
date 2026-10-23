# Secondary restoration

The secondary-restoration case adds a common integral bias in Hz to the same
primary droop law. Its derivative is minus the active-source mean frequency
deviation times the configured gain. A bounded bias prevents unlimited windup.

Compare against load-step: primary control shares load with a frequency offset;
secondary control moves the droop references until the common frequency recovers.
The model does not include communication delay or cyber-security effects.
