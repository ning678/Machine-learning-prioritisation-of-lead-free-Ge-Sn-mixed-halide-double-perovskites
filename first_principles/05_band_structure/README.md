# Electronic band gaps and band-structure calculations

This directory contains the first-principles electronic-structure
calculations used for the parent and soft-mode-derived P1 structures of
Cs2GeSnCl2Br4 and Cs2GeSnCl4Br2.

## Canonical band-gap calculations

The file canonical_band_gaps.csv contains the canonical band gaps
obtained directly from completed static or full-Brillouin-zone
calculations.

All sixteen parent/final-P1 and
PBE/PBE+SOC/HSE06/HSE06+SOC combinations show direct Gamma-Gamma gaps.

Canonical gaps (eV):

Cs2GeSnCl2Br4 parent:
- PBE:       0.694182
- PBE+SOC:   0.505782
- HSE06:     1.168815
- HSE06+SOC: 0.973401

Cs2GeSnCl2Br4 final P1:
- PBE:       1.488056
- PBE+SOC:   1.411790
- HSE06:     2.116285
- HSE06+SOC: 2.037146

Cs2GeSnCl4Br2 parent:
- PBE:       0.713850
- PBE+SOC:   0.602169
- HSE06:     1.205662
- HSE06+SOC: 1.096830

Cs2GeSnCl4Br2 final P1:
- PBE:       1.620450
- PBE+SOC:   1.581880
- HSE06:     2.271259
- HSE06+SOC: 2.232990

For the 40-atom Cs2GeSnCl2Br4 final-P1 structure, the canonical HSE06
gap was taken from the 2x2x2 calculation (2.116285 eV). A 3x3x3
calculation gives 2.106816 eV; the corresponding k-mesh comparison is
archived in ../09_convergence/Cs2GeSnCl2Br4_final_HSE06_kmesh.csv.

## Line-band calculations

Completed line-band calculations are archived only where they were
actually performed.

Available dispersion calculations are:
- Cs2GeSnCl2Br4 parent: PBE and HSE06
- Cs2GeSnCl2Br4 final P1: PBE
- Cs2GeSnCl4Br2 parent: PBE and HSE06
- Cs2GeSnCl4Br2 final P1: PBE

For Cs2GeSnCl2Br4 parent HSE06, the dispersion was evaluated using
three completed zero-weight k-path segments following the converged
HSE06 SCF calculation.

SOC band gaps and final-P1 HSE06 gaps for which no line-band
calculation was performed were obtained from static or
full-Brillouin-zone calculations. They should not be interpreted as
line-band dispersions.

The POSCAR files used in band calculations may be equivalent
reorientations or primitive representations of the corresponding
canonical structures and therefore need not be byte-identical to the
canonical static POSCAR files.

## Scope

Historical failed, obsolete and pre-ISIF3 calculations are excluded
from this archive.

VASP POTCAR, WAVECAR and CHGCAR files are not redistributed.
PAW dataset identifiers are provided separately in POTCAR.spec.
