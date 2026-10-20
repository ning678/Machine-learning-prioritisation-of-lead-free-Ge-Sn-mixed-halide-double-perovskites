
# Gamma-point soft-mode calculations and ASR analysis

This directory contains Gamma-point vibrational calculations, soft-mode-following structural relaxation results, and acoustic sum rule (ASR) post-processing data for Cs2GeSnCl2Br4 and Cs2GeSnCl4Br2.

The calculations are restricted to the Gamma point. They do not constitute full phonon-dispersion calculations or establish dynamical stability throughout the Brillouin zone.

## 1. Cs2GeSnCl2Br4: soft-mode evolution

The 40-atom parent structure exhibits a largest Gamma-point imaginary frequency of 3.401681 i THz (113.467880 i cm^-1).

The soft-mode-following sequence reduces the largest imaginary frequency as follows:

| Structural stage | Largest imaginary frequency (i THz) |
|---|---:|
| Parent | 3.401681 |
| Round 1 | 1.405834 |
| Round 2 | 0.745194 |
| Final P1 | 0.096697 |

The final P1 structure contains three small residual imaginary modes before ASR correction:

- 0.062800 i THz
- 0.075110 i THz
- 0.096697 i THz

The largest imaginary-frequency magnitude decreases by approximately 97.16% relative to the parent structure.

The final Gamma-point phonon calculation was performed on the same atomic structure as that used for the final-P1 electronic calculations, as verified by byte-identical POSCAR files.

For the historical round-1 calculation, the archived Gamma-check POSCAR was not byte-identical to either saved plus-Q or minus-Q relaxation CONTCAR. Therefore, no exact plus/minus handoff is assigned for that stage solely on the basis of file identity.

## 2. Cs2GeSnCl4Br2: soft-mode evolution

The 20-atom parent structure exhibits a largest Gamma-point imaginary frequency of 3.157339 i THz (105.317482 i cm^-1).

The canonical parent Gamma calculation was historically stored in:

`10_dielectric/01_dfpt_static`

The parent Gamma calculation used a structure byte-identical to the parent PBE-static POSCAR.

The soft-mode-following evolution is summarised below:

| Structural stage | Largest imaginary frequency (i THz) |
|---|---:|
| Parent | 3.157339 |
| Round 1 | 2.923960 |
| Round 2 | 1.001384 |
| Post-ISIF3 intermediate | 1.322188 |
| Final post-ISIF3 P1 | 0.068633 |

A historical mode-following script, `make_mode60_pm.py`, generated plus-Q and minus-Q structures from the parent mode-60 eigenvector using a maximum atomic displacement of 0.05 Å. The generated structures were verified against the round-1 relaxation inputs. This historical generator script is not included in the present public repository.

The final selected structure was obtained from the minus-Q post-ISIF3 branch.

The final Gamma calculation contains three residual imaginary modes before ASR correction:

- 0.038212 i THz
- 0.041437 i THz
- 0.068633 i THz

The largest imaginary-frequency magnitude decreases by approximately 97.83% relative to the parent structure.

The final Gamma-check POSCAR is byte-identical to the canonical final-P1 electronic-structure POSCAR.

## 3. Acoustic sum rule analysis

The final P1 structures of both materials exhibit three small residual imaginary modes in the raw Gamma-point calculations.

To investigate their character, the script `asr_check.py` performs acoustic sum rule post-processing on the VASP DFPT Gamma-point Hessian.

The procedure includes:

1. Reading the mass-weighted Gamma-point Hessian and atomic masses from `vasprun.xml`.
2. Constructing the corresponding unweighted force-constant matrix.
3. Applying an on-site-block correction to enforce the acoustic sum rule.
4. Reconstructing the mass-weighted Hessian and diagonalising it.
5. Evaluating the translational character of the low-frequency eigenmodes.

The detailed numerical implementation is provided in `asr_check.py`.

### 3.1. Archived input and output files

**Cs2GeSnCl2Br4:**

```text
Cs2GeSnCl2Br4_final_gamma/
├── vasprun.xml
└── asr_finalP1_result.txt
```

The XML contains a 120 × 120 Gamma-point Hessian for the 40-atom final P1 structure.

**Cs2GeSnCl4Br2:**

```text
Cs2GeSnCl4Br2_final_gamma/
├── vasprun.xml
└── asr_finalP1_result.txt
```

The XML contains a 60 × 60 Gamma-point Hessian for the 20-atom final P1 structure.

Both Gamma-check structures were verified to be byte-identical to their respective canonical final-P1 POSCAR files archived in `../01_structures/`.

### 3.2. Reproduction instructions

Requirements:

- Python 3
- NumPy

From the current `04_phonons` directory, run:

```bash
python3 asr_check.py \
  Cs2GeSnCl2Br4_final_gamma/vasprun.xml
```

For Cs2GeSnCl4Br2:

```bash
python3 asr_check.py \
  Cs2GeSnCl4Br2_final_gamma/vasprun.xml
```

The original VASP OUTCAR can optionally be supplied as a second argument:

```bash
python3 asr_check.py vasprun.xml OUTCAR
```

When OUTCAR is supplied, the raw Hessian-derived frequencies are compared with the frequencies printed by VASP.

The original OUTCAR files are not included in this public repository. Their frequency consistency was checked using the original completed VASP calculations.

The archived `vasprun.xml` files are sufficient to reproduce the reported ASR post-processing results.

## 4. Verified ASR results

| Quantity | Cs2GeSnCl2Br4 | Cs2GeSnCl4Br2 |
|---|---:|---:|
| Number of atoms | 40 | 20 |
| Number of Gamma modes | 120 | 60 |
| Raw imaginary modes | 3 | 3 |
| Largest raw imaginary frequency (i THz) | 0.096697 | 0.068633 |
| Maximum residual acoustic frequency after ASR (cm^-1) | 0.72 | 0.09 |
| Lowest optical frequency after ASR (THz) | 0.3791 | 0.5288 |
| Imaginary optical modes after ASR | 0 | 0 |

### 4.1. Translational weights

The three residual imaginary modes before ASR correction have the following translational weights:

| Material | Mode 1 | Mode 2 | Mode 3 |
|---|---:|---:|---:|
| Cs2GeSnCl2Br4 | 0.998 | 0.994 | 0.990 |
| Cs2GeSnCl4Br2 | 0.999 | 0.999 | 0.999 |

These values indicate a predominantly translational character of the three residual low-frequency modes.

Following ASR correction, the three lowest-frequency modes in each material have translational weights reported as 1.000.

### 4.2. Residual acoustic frequencies after ASR

For Cs2GeSnCl2Br4, the three residual acoustic frequencies are approximately:

```text
0.0000 i THz
0.0100 i THz
0.0216 i THz
```

For Cs2GeSnCl4Br2:

```text
0.0000 i THz
0.0024 i THz
0.0027 i THz
```

These values represent small residual negative acoustic-mode eigenvalues after the applied ASR procedure.

The largest residual acoustic-frequency magnitudes correspond to 0.72 and 0.09 cm^-1, respectively.

The lowest positive optical frequencies after ASR are:

- Cs2GeSnCl2Br4: 0.3791 THz.
- Cs2GeSnCl4Br2: 0.5288 THz.

No imaginary optical modes were identified at the Gamma point after the reported ASR processing.

## 5. Interpretation and limitations

The results support the interpretation that the three small residual imaginary Gamma-point modes of the final P1 structures are predominantly acoustic translational modes.

However, ASR correction does not make every reported frequency exactly positive or zero. Small residual imaginary acoustic frequencies remain in both materials.

Consequently, the appropriate conclusion is:

**No imaginary optical modes were identified at the Gamma point after ASR post-processing for either final P1 structure.**

This conclusion must not be interpreted as:

- Complete elimination of all imaginary frequencies.
- Proof of full-Brillouin-zone dynamical stability.
- Evidence that all possible lattice instabilities have been excluded.

Full phonon-dispersion calculations would be required to assess vibrational stability across the Brillouin zone.

## 6. Data provenance and exclusions

The original soft-mode evolution is summarised in:

- `gamma_frequency_summary.csv`
- `soft_mode_relaxation_energies.csv`

The final-P1 ASR calculations are documented by:

- `asr_check.py`
- `Cs2GeSnCl2Br4_final_gamma/vasprun.xml`
- `Cs2GeSnCl2Br4_final_gamma/asr_finalP1_result.txt`
- `Cs2GeSnCl4Br2_final_gamma/vasprun.xml`
- `Cs2GeSnCl4Br2_final_gamma/asr_finalP1_result.txt`

Incomplete historical finite-difference calculations and legacy full-phonon attempts are excluded from this archive.

VASP POTCAR files are not redistributed because of VASP licence restrictions. PAW dataset identifiers are provided in `POTCAR.spec`.
