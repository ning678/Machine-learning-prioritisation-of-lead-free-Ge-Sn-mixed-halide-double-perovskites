# PBE optical calculations and Fig. 7 plotting data

This directory contains the canonical PBE non-SOC LOPTICS calculations
and processed optical data used for Fig. 7 of the manuscript.

Four structures are included:
- Cs2GeSnCl2Br4 parent
- Cs2GeSnCl2Br4 soft-mode-derived P1
- Cs2GeSnCl4Br2 parent
- Cs2GeSnCl4Br2 soft-mode-derived P1

All canonical optical calculations used:
- VASP
- PBE
- non-SOC
- LOPTICS = .TRUE.
- ENCUT = 500 eV
- NEDOS = 3000
- CSHIFT = 0.10 eV

The k-point meshes and NBANDS values differ between calculations and
are listed in optical_sources.csv.

The dielectric data used for Fig. 7 were extracted from the
density-density dielectric-function block in vasprun.xml.

The dielectric tensor was averaged as:

epsilon_avg = (epsilon_xx + epsilon_yy + epsilon_zz) / 3

The optical constants n, k, absorption coefficient alpha, and
reflectivity R were subsequently derived from the averaged dielectric
function. The exact processing procedure is retained in
scripts/build_and_audit_fig7.py.

Both full-range and 0-6 eV plotting CSV files are provided.

These spectra are PBE non-SOC optical calculations. HSE06 gap
corrections used later for SLME are not applied to the Fig. 7 spectra.

VASP POTCAR files are not redistributed. PAW dataset identifiers are
listed in POTCAR.spec.
