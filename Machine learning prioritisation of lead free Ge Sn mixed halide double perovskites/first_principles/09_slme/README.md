# Canonical spectroscopic limited maximum efficiency (SLME)

This directory contains the **recomputed**, machine-readable SLME results for the ordered parent (`I4/mmm`) and soft-mode-derived final-P1 structures of Cs2GeSnCl2Br4 and Cs2GeSnCl4Br2. All four structures are treated with the **same** numerical protocol and a single processed ASTM G173-03 AM1.5G solar spectrum. These values supersede preliminary parent/final-soft comparison sheets assembled from mixed historical optical inputs. The values in this archive are calculated outputs, not values pasted from a manuscript table.

## Files

- `scripts/recompute_slme.py`: reproducible Python 3 post-processing script; no third-party packages required. File paths are relative to this repository.
- `solar_spectrum/ASTM_G173_AM1.5G.csv`: 2,002-point global-tilt AM1.5G spectrum in `W m^-2 nm^-1`.
- `results/slme_canonical_results.csv`: twelve independently recomputed efficiency records, including `Jsc`, `Voc`, fill factor and the underlying HSE06 scissors shifts.

The four **3000-point optical input files are already stored** in `../07_optical/plotting_data/` and are not duplicated here:

| Structure | PBE absorption-spectrum input |
|---|---|
| Cs2GeSnCl2Br4 parent | `Cs2GeSnCl2Br4_parent_optical_full.csv` |
| Cs2GeSnCl2Br4 final P1 | `Cs2GeSnCl2Br4_P1_optical_full.csv` |
| Cs2GeSnCl4Br2 parent | `Cs2GeSnCl4Br2_parent_optical_full.csv` |
| Cs2GeSnCl4Br2 final P1 | `Cs2GeSnCl4Br2_P1_optical_full.csv` |

Only the `alpha_from_epsavg_cm-1` column is used. This coefficient is derived from the complex dielectric tensor averaged as `(eps_xx + eps_yy + eps_zz)/3` **before** calculating the optical constants. Fig. 7 spectra are unshifted PBE/non-SOC data; HSE06 scissors shifts are applied **only within SLME post-processing**.

## Electronic gaps and shifts

The gaps below correspond to the canonical, non-SOC band-gap calculations archived in `../05_band_structure/canonical_band_gaps.csv`.

| Composition | Structure | PBE gap (eV) | HSE06 gap (eV) | Scissors shift (eV) |
|---|---|---:|---:|---:|
| Cs2GeSnCl2Br4 | Parent | 0.694182 | 1.168815 | 0.474633 |
| Cs2GeSnCl2Br4 | Final P1 | 1.488056 | 2.116285 | 0.628229 |
| Cs2GeSnCl4Br2 | Parent | 0.713850 | 1.205662 | 0.491812 |
| Cs2GeSnCl4Br2 | Final P1 | 1.620450 | 2.271259 | 0.650809 |

The PBE absorption coefficient is shifted rigidly on the energy axis by the corresponding HSE06-minus-PBE gap difference. The spectral shape is otherwise retained. Absorption is explicitly set to zero below the HSE06 gap.

## Numerical protocol

- Solar reference: processed ASTM G173-03 AM1.5G global-tilt spectrum, 280-4000 nm (2,002 tabulated points).
- Numerically integrated incident power: **1000.370655573 W m^-2**.
- Temperature: **300 K**.
- Radiative fraction: **f_r = 1** for these direct-gap cases.
- Absorptivity: **a(E,L) = 1 - exp[-2 alpha(E) L]**, with `alpha` converted from cm^-1 by applying thickness in cm.
- Absorber thicknesses: **0.5, 1.0, and 2.0 micrometres**.
- Short-circuit current: numerical integration of solar photon flux multiplied by absorptivity.
- Radiative saturation current: numerical integration of the 300 K black-body photon flux multiplied by absorptivity over the shifted optical-energy grid.
- Numerical integration: trapezoidal rule; linear interpolation to the solar photon-energy grid.
- Maximum-power point: grid search at 20,001 voltage points from `0` to `1.05 Voc`.
- Efficiency: `100 * Pmax / Pin`.

This is the stated independent-particle, non-SOC PBE optical + non-SOC HSE06 scissors **materials-level radiative-limit** approximation. It is not a full HSE06+SOC optical calculation and is not a full photovoltaic device simulation.

## Canonical results

| Composition | Structure | SLME at 0.5 um (%) | SLME at 1.0 um (%) | SLME at 2.0 um (%) |
|---|---|---:|---:|---:|
| Cs2GeSnCl2Br4 | Parent | 32.56 | 33.89 | 34.05 |
| Cs2GeSnCl2Br4 | Final P1 | 19.51 | 20.36 | 20.51 |
| Cs2GeSnCl4Br2 | Parent | 30.17 | 32.54 | 33.39 |
| Cs2GeSnCl4Br2 | Final P1 | 16.26 | 16.95 | 17.04 |

The efficiency losses (final P1 minus parent) are approximately -13.05 to -13.54 percentage points for Cs2GeSnCl2Br4 and -13.92 to -16.34 percentage points for Cs2GeSnCl4Br2. The composition ordering remains unchanged at all three thicknesses.

## How to reproduce

Keep this directory under `first_principles/` alongside the existing `07_optical` folder. From the outer repository data directory (the directory containing `first_principles/`), run:

```bash
python3 first_principles/09_slme/scripts/recompute_slme.py
```

The script resolves paths from its own location and therefore does not depend on a user's HPC username or server installation. It checks the SHA-256 hashes of all four optical input CSVs and the solar spectrum **before** writing output. The output is `first_principles/09_slme/results/slme_canonical_results.csv`.

The validated solar input SHA-256 is:

`01f52e67a2309338a1bba35380e2189fc636cb7bfc32f4b83b236ce770f92b95`

Input optical SHA-256 hashes are recorded in the script and in the result CSV (`optical_SHA256`). The script can be rerun without the VASP executables or proprietary PAW potentials, using the deposited PBE optical spectra.

## Provenance and interpretation

The four standard optical CSV files were regenerated from completed VASP `vasprun.xml` density-density dielectric-function data and audited separately under `../07_optical/`. The canonical band gaps are taken from completed electronic calculations, not inferred from the SLME outputs.

Historical SLME results used different intermediate optical data and/or gap values. Consequently, they should **not** be interchanged with these canonical results or used as independent support for the values in this directory. This archive retains one common post-processing method for all four structures. Interpret the calculated efficiencies as idealised absorber-level estimates; no device-level recombination, transport or interface loss model is included.
