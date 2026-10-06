# Gamma-point soft-mode calculations

This directory contains the Gamma-point vibrational calculations and
soft-mode-following structural relaxations used in the manuscript for
Cs2GeSnCl2Br4 and Cs2GeSnCl4Br2.

These data represent Gamma-point soft-mode analyses only. They should
not be interpreted as complete phonon dispersions or as proof of
full-Brillouin-zone dynamical stability.

## Cs2GeSnCl2Br4

The 40-atom parent structure exhibited a largest Gamma-point imaginary
frequency of 3.401681 i THz (113.467880 i cm^-1).

Successive soft-mode-following cycles reduced the largest imaginary
frequency to:

parent      3.401681 i THz
round 1     1.405834 i THz
round 2     0.745194 i THz
final       0.096697 i THz

The final Gamma calculation contains three very small residual imaginary
modes:

0.062800 i THz
0.075110 i THz
0.096697 i THz

The largest residual value corresponds to 3.225467 i cm^-1.

The magnitude of the largest imaginary frequency was reduced by
approximately 97.16% relative to the parent structure.

The final Gamma-check POSCAR is byte-identical to the structure used
for the subsequent final-P1 electronic calculations.

For round 1, the archived Gamma-check POSCAR is not byte-identical to
either saved plus-Q or minus-Q relaxation CONTCAR. It is therefore
retained as the actual Gamma-check input without assigning an exact
plus/minus handoff from byte identity alone.

## Cs2GeSnCl4Br2

The canonical parent Gamma-mode source is the completed VASP calculation
historically stored at:

10_dielectric/01_dfpt_static

Its POSCAR is byte-identical to the parent PBE-static POSCAR.

The largest parent Gamma-point imaginary mode is mode 60:

3.157339 i THz = 105.317482 i cm^-1.

The archived make_mode60_pm.py script reads the parent POSCAR and OUTCAR,
normalises the mode-60 eigenvector, and generates plus-Q and minus-Q
structures with a maximum atomic displacement of 0.05 Angstrom.
The generated structures are byte-identical to the inputs used for the
round-1 plus-Q and minus-Q relaxations.

The subsequent largest Gamma-point imaginary frequencies were:

parent          3.157339 i THz
round 1         2.923960 i THz
round 2         1.001384 i THz
post-ISIF3      1.322188 i THz
final           0.068633 i THz

The final Gamma calculation contains three very small residual imaginary
modes:

0.038212 i THz
0.041437 i THz
0.068633 i THz

The largest residual value corresponds to 2.289351 i cm^-1.

The magnitude of the largest imaginary frequency was reduced by
approximately 97.83% relative to the parent structure.

The final selected structure follows the minus-Q post-ISIF3 branch.
Its Gamma-check POSCAR is byte-identical to the structure used for the
subsequent final-P1 electronic calculations.

## Scope and exclusions

Incomplete historical finite-difference calculations and legacy
full-phonon attempts are not included in this archive.

The archived results should therefore be described as suppression of
Gamma-point soft modes with only very small residual Gamma-point
imaginary modes remaining, rather than as complete removal of imaginary
frequencies or proof of full dynamical stability.

VASP POTCAR files are not redistributed because they are subject to the
VASP licence. PAW dataset identifiers are provided separately in
POTCAR.spec.
