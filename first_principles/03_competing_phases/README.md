# Finite-set competing-phase calculations

This directory contains the PBE static calculations used for the
finite-set competing-phase comparison of Cs2GeSnCl2Br4 and
Cs2GeSnCl4Br2.

The explicitly tested phase set comprises:
- binaries: CsCl, CsBr, GeCl2, GeBr2, SnCl2 and SnBr2
- ternaries: CsGeCl3, CsGeBr3, CsSnCl3 and CsSnBr3
- auxiliary calculated phase: GeCl4

All archived static calculations used:
- VASP 6.3.2
- ENCUT = 500 eV

Individual k-point meshes are retained in each KPOINTS file.

The lowest balanced product combination identified within this tested
phase set for Cs2GeSnCl2Br4 is:

(2/3) CsGeCl3 + (1/3) CsGeBr3 + CsSnBr3

with an energy of -33.19618497 eV per target formula unit.

Relative to this product set, the parent and soft-mode-derived P1
structures lie 12.323126 and 2.629617 meV/atom higher, respectively.

For Cs2GeSnCl4Br2, the lowest tested balanced product combination is:

CsGeCl3 + (1/3) CsSnCl3 + (2/3) CsSnBr3

with an energy of -34.31840958 eV per target formula unit.

Relative to this product set, the parent and soft-mode-derived P1
structures lie 15.022214 and 1.858199 meV/atom higher, respectively.

These values are finite-set competing-phase offsets and should not be
interpreted as complete convex-hull energies.

GeCl4 was calculated as an auxiliary competing phase but does not enter
either lowest-energy tested decomposition pathway.

VASP POTCAR files are not redistributed.
