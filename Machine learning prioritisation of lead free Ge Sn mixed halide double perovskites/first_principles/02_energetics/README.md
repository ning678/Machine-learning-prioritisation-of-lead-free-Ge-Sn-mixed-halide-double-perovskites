# Target and elemental-reference PBE energies

This directory contains the self-consistent PBE calculations used for
the parent-to-soft-mode-derived P1 energetic comparison and for the
formation-energy calculations.

## Target static calculations

The target static calculations used:
- VASP 6.3.2
- ENCUT = 500 eV
- Gamma-centred 6x6x6 k-point meshes

Cell representations:
- Cs2GeSnCl2Br4 parent: 20 atoms, Z = 2
- Cs2GeSnCl2Br4 P1: 40 atoms, Z = 4
- Cs2GeSnCl4Br2 parent: 20 atoms, Z = 2
- Cs2GeSnCl4Br2 P1: 20 atoms, Z = 2

Reported target energies are normalised per formula unit when structures
with different cell sizes are compared.

The parent-to-P1 energy lowerings are:
- Cs2GeSnCl2Br4: -96.93509 meV/f.u.
- Cs2GeSnCl4Br2: -131.64015 meV/f.u.

## Elemental references

Formation energies were referenced to:
- bcc Cs
- diamond Ge
- beta-Sn
- isolated Cl2 molecule
- isolated Br2 molecule

All elemental-reference calculations used ENCUT = 500 eV.
The individual KPOINTS, smearing settings and irreducible k-point counts
are retained in the archived calculation directories and summarised in
elemental_reference_energies.csv.

The final VASP TOTEN values were used as the energy convention for the
formation energies reported in the manuscript. The corresponding
energy(sigma->0) values are also retained in
elemental_reference_energies.csv for transparency.

The resulting formation energies are:
- Cs2GeSnCl2Br4 parent: -1.31529759 eV/atom
- Cs2GeSnCl2Br4 P1: -1.32499109 eV/atom
- Cs2GeSnCl4Br2 parent: -1.36638589 eV/atom
- Cs2GeSnCl4Br2 P1: -1.37954990 eV/atom

VASP POTCAR files are not redistributed because they are subject to the
VASP licence. The PAW dataset identifiers are provided in POTCAR.spec
and in elemental_reference_energies.csv.
