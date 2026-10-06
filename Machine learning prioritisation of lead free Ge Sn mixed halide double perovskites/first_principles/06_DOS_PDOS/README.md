# PBE DOS and PDOS data

This directory contains the PBE density-of-states calculations and the
machine-readable plotting data used for Fig. 6 of the manuscript.

## Source calculations

Cs2GeSnCl2Br4 parent:
- 20 atoms, Z = 2
- Gamma-centred 9x9x9 k-point mesh
- NEDOS = 3000

Cs2GeSnCl2Br4 soft-mode-derived P1:
- 40 atoms, Z = 4
- Gamma-centred 9x9x9 k-point mesh
- NEDOS = 3000

Cs2GeSnCl4Br2 parent:
- 20 atoms, Z = 2
- Gamma-centred 8x8x8 k-point mesh
- NEDOS = 5000

Cs2GeSnCl4Br2 soft-mode-derived P1:
- 20 atoms, Z = 2
- Gamma-centred 9x9x9 k-point mesh
- NEDOS = 3000

All four calculations used:
- PBE
- ENCUT = 500 eV
- LORBIT = 11

## Plotting convention

For Fig. 6, the energy axis is referenced to the valence-band maximum:

E_plot = E - E_VBM.

Total and projected densities of states are normalised per formula unit,
in units of states/eV/formula_unit.

The plotting CSV files were regenerated directly from the archived
DOSCAR files using build_and_audit_fig6.py.

Fig6_rebuild_audit.txt records the source DOSCAR SHA256 hashes and the
numerical comparison against the historical plotting CSV files.

No interpolation, smoothing or resampling was introduced during this
rebuild.

VASP POTCAR files are not redistributed because they are subject to the
VASP licence. PAW dataset identifiers are provided in POTCAR.spec.
