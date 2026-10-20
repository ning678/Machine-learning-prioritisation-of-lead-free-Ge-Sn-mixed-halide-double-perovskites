
# Canonical structures and local octahedral geometry

This directory contains the canonical parent and soft-mode-derived final-P1 structures of Cs2GeSnCl2Br4 and Cs2GeSnCl4Br2. These structures were used to calculate the local octahedral geometry parameters reported in Table 5 of the manuscript.

## 1. Structural models

| Material | Structure | POSCAR file | Atoms | Volume per formula unit (Å³) |
|---|---|---|---:|---:|
| Cs2GeSnCl2Br4 | Parent | `Cs2GeSnCl2Br4_parent40_structural_POSCAR` | 40 | 363.04 |
| Cs2GeSnCl2Br4 | Final P1 | `Cs2GeSnCl2Br4_final_P1_POSCAR` | 40 | 383.98 |
| Cs2GeSnCl4Br2 | Parent | `Cs2GeSnCl4Br2_parent_POSCAR` | 20 | 346.21 |
| Cs2GeSnCl4Br2 | Final P1 | `Cs2GeSnCl4Br2_final_P1_POSCAR` | 20 | 370.10 |

The additional file `Cs2GeSnCl2Br4_parent20_downstream_POSCAR` is an equivalent 20-atom representation of the 40-atom parent structure used in downstream electronic-structure calculations.

## 2. Structure provenance

The four structures used for Table 5 were obtained from the following VASP calculation directories.

**Cs2GeSnCl2Br4 parent:**

`02_SOFTMODE_HISTORY/00_tight_start/10_pbe_relax_tight_333/Cs2GeSnCl2Br4_parent_PBE_relaxed/01_input/POSCAR`

**Cs2GeSnCl2Br4 final P1:**

`03_FINAL_P1/00_structure/POSCAR`

**Cs2GeSnCl4Br2 parent:**

`15_phonon/00_parent_reference/00_prepare_mode60_round1/POSCAR_parent`

**Cs2GeSnCl4Br2 final P1:**

`19_finalP1_electronic/01_FINAL_postISIF3_canonical/01_pbe_static_666/POSCAR`

All four archived POSCAR files were verified against their original calculation inputs using SHA-256 checksums.

## 3. Local octahedral geometry analysis

The script `local_geometry.py` calculates local structural descriptors for Ge- and Sn-centred octahedra using the six nearest halide neighbours under periodic boundary conditions.

The calculated parameters include:

- Ge-X and Sn-X bond-length ranges.
- Three shortest and three longest B-X bonds, where B = Ge or Sn.
- Ge and Sn off-centre displacements.
- Bond-length distortion index.
- Octahedral bond-angle variance.
- Ge-X-Sn bridging-angle ranges.

The off-centre displacement is defined as the distance between a B-site cation and the centroid of its six coordinating halide atoms.

The bond-length distortion index is calculated as

\[
\Delta_d=\frac{1}{6}\sum_{i=1}^{6}
\left(\frac{d_i-\bar d}{\bar d}\right)^2
\]

where \(d_i\) represents an individual B-X bond length and \(\bar d\) is the mean bond length.

The bond-angle variance is calculated as

\[
\sigma^2=\frac{1}{11}\sum_{i=1}^{12}
(\theta_i-90^\circ)^2
\]

where the sum runs over the twelve cis X-B-X angles.

## 4. Reproduction instructions

Requirements:

- Python 3
- NumPy

Run the following command from this directory:

```bash
python3 local_geometry.py \
  Cs2GeSnCl2Br4_parent40_structural_POSCAR \
  Cs2GeSnCl2Br4_final_P1_POSCAR \
  Cs2GeSnCl4Br2_parent_POSCAR \
  Cs2GeSnCl4Br2_final_P1_POSCAR
```

The reference output is provided in:

`local_geometry_Table5_FINAL.txt`

The reference output contains historical server-side POSCAR names. These files are byte-identical to the corresponding canonical POSCAR files in this directory.

## 5. Verified local structural parameters

| Parameter | Cl2Br4 parent | Cl2Br4 P1 | Cl4Br2 parent | Cl4Br2 P1 |
|---|---:|---:|---:|---:|
| Ge off-centre displacement (Å) | 0.000 | 0.335 | 0.000 | 0.342 |
| Sn off-centre displacement (Å) | 0.000 | 0.279 | 0.000 | 0.268 |
| Ge distortion index (×10⁻³) | 0.70 | 12.19 | 0.63 | 15.68 |
| Sn distortion index (×10⁻³) | 0.55 | 8.69 | 0.51 | 10.69 |
| Ge bond-angle variance (deg²) | 0.0 | 16.1 | 0.0 | 13.0 |
| Sn bond-angle variance (deg²) | 0.0 | 11.5 | 0.0 | 6.7 |
| Ge-X-Sn angles (degrees) | 180.0 | 152.9-172.8 | 180.0 | 150.8-172.9 |

The parent structures exhibit negligible B-site off-centre displacement and approximately linear Ge-X-Sn bridging bonds.

Following soft-mode-derived structural relaxation, both P1 structures exhibit substantial Ge/Sn off-centre displacements, bond-length splitting, and deviations from linear bridging geometry.

These geometric descriptors quantify the structural changes but do not, by themselves, uniquely establish the microscopic driving mechanism or electronic consequences of the distortion.

## 6. Reproducibility limitations

The archived structures and analysis script permit independent reproduction of the reported local geometric descriptors without rerunning VASP.

The results are specific to the supplied ordered structures and their relaxed configurations.
