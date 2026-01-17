# CEC-WAM LOCKED CORE FORMULAS
Status: IMMUTABLE
Version: 1.0

## 1. PSI MASS
PSI_mass = Σ(incoming_assets) − Σ(outgoing_assets)

## 2. BLACK HOLE FLOW RATE
BH_flow = (PSI_mass × Φ) / T

Where:
Φ (phi) = 1.618033988
T = time normalization constant (default: 21600 seconds)

## 3. DARK ENERGY INDEX
DE_index = 1 − (usable_capacity / total_capacity)

Stable range:
0.985 ≤ DE_index ≤ 1.005

## 4. R-RATIO EFFICIENCY
R_ratio = PSI_mass / BH_flow

Target band:
9.5 ≤ R_ratio ≤ 11.2

## 5. CAPACITY THRESHOLD
System must export when:
used_capacity ≥ 0.85

Hard stop at:
used_capacity ≥ 0.92

## 6. EXPORT RULE (NON-DESTRUCTIVE)
Export oldest data first.
Verify checksum.
Only delete after successful write.

These formulas MUST NOT be auto-edited.
