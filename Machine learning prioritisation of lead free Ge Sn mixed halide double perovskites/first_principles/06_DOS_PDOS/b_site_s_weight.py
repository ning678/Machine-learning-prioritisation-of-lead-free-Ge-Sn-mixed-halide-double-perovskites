"""B-site s weight near the valence-band maximum from the Fig. 6 DOS/PDOS CSVs.

    python bs_vbm.py Fig6a_...csv Fig6b_...csv ...

For each file: integrated Ge-s, Sn-s, halide-p and total DOS (states/f.u.)
in windows below the VBM (E - E_VBM in [-w, 0]), and the B-s share of the total.
"""
import csv
import sys

import numpy as np


def load(path):
    rows = list(csv.DictReader(open(path, newline='')))
    col = lambda k: np.array([float(r[k]) for r in rows])
    return {k: col(k) for k in rows[0]}


def main(paths, windows=(0.5, 1.0, 2.0)):
    for p in paths:
        d = load(p)
        e = d['Energy_minus_VBM_eV']
        print(f'== {p.split(chr(92))[-1].split("/")[-1]}')
        for w in windows:
            m = (e >= -w) & (e <= 0.0)
            integ = lambda k: np.trapezoid(d[k][m], e[m])
            tot = integ('TDOS_per_fu')
            ges, sns = integ('Ge_s_per_fu'), integ('Sn_s_per_fu')
            xp = integ('Cl_p_per_fu') + integ('Br_p_per_fu')
            print(f'  [-{w:.1f},0] eV: TDOS {tot:.3f}  Ge-s {ges:.3f}  Sn-s {sns:.3f}  '
                  f'B-s share {(ges + sns) / tot * 100:.1f}%  X-p share {xp / tot * 100:.1f}%')
        vb = (e >= -10) & (e <= 0)
        top = (e >= -3) & (e <= 0)
        for k in ('Ge_s_per_fu', 'Sn_s_per_fu'):
            total = np.trapezoid(d[k][vb], e[vb])
            upper = np.trapezoid(d[k][top], e[top])
            centre = np.trapezoid(d[k][vb] * e[vb], e[vb]) / total
            print(f'  {k[:4]} in [-10,0] eV: {total:.3f}; share in top 3 eV {upper / total * 100:.1f}%; '
                  f'weighted centre {centre:.2f} eV')


if __name__ == '__main__':
    main(sys.argv[1:])
