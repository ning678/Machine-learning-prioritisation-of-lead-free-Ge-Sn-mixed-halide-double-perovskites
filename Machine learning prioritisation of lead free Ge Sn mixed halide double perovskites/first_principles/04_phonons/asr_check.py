"""Impose the acoustic sum rule on a VASP DFPT Gamma-point Hessian, re-diagonalise,
and report how translational each low-lying mode is.

    python asr_check.py vasprun.xml [OUTCAR]

vasprun.xml is enough. If an OUTCAR is also given, the unit conversion is
cross-checked against the frequencies VASP printed.
"""
import re
import sys
import xml.etree.ElementTree as ET

import numpy as np

# VASP writes the vasprun.xml Hessian pre-scaled so that sqrt(-eigenvalue) is
# already in THz; verified to 5e-7 THz against the OUTCAR frequencies.
THZ = 1.0
CM1 = 33.35641  # THz -> cm^-1

root = ET.parse(sys.argv[1]).getroot()
mass_of = {rc.findall("c")[1].text.strip(): float(rc.findall("c")[2].text)
           for rc in root.find(".//array[@name='atomtypes']/set")}
masses = np.array([mass_of[rc.findall("c")[0].text.strip()]
                   for rc in root.find(".//array[@name='atoms']/set")])
nat = len(masses)

# Hessian as written by VASP: mass-weighted and sign-flipped.
hess = np.array([[float(x) for x in v.text.split()]
                 for v in root.find(".//varray[@name='hessian']")])
hess = 0.5 * (hess + hess.T)

# ASR: unweight -> force each 3x3 block row to sum to zero -> reweight.
w = np.sqrt(np.repeat(masses, 3))
phi = (hess * np.outer(w, w)).reshape(nat, 3, nat, 3)
for i in range(nat):
    phi[i, :, i, :] -= phi[i].sum(axis=1)
hess_asr = phi.reshape(3 * nat, 3 * nat) / np.outer(w, w)


def spectrum(matrix):
    val, vec = np.linalg.eigh(-matrix)
    return np.sign(val) * np.sqrt(np.abs(val)) * THZ, vec


if len(sys.argv) > 2:
    printed = np.array([-float(f) if i else float(f) for i, f in
                        re.findall(r"f(/i)?\s*=\s*([\d.]+) THz", open(sys.argv[2]).read())])
    printed = np.sort(printed[-3 * nat:])[::-1]
    assert np.allclose(np.sort(spectrum(hess)[0])[::-1], printed, atol=2e-3), \
        "conversion factor disagrees with the frequencies in OUTCAR"

for label, m in (("raw (as run)", hess), ("ASR-corrected", hess_asr)):
    f, vec = spectrum(m)
    im = f[f < 0]
    print("%-14s n_imag = %2d   max|w_im| = %.4f THz (%.2f cm-1)"
          % (label, len(im), abs(im).max() if len(im) else 0.0,
             abs(im).max() * CM1 if len(im) else 0.0))
    print("               six lowest |w| / THz, with translational weight:")
    for k in np.argsort(np.abs(f))[:6]:
        d = (vec[:, k] / w).reshape(nat, 3)
        t = np.linalg.norm(d.sum(0)) / (np.sqrt(nat) * np.linalg.norm(d))
        print("                 %7.4f%s   %.3f" % (abs(f[k]), "i" if f[k] < 0 else " ", t))

# Values reported in the manuscript (main text, SI residual-mode and soft-mode tables).
f = np.sort(spectrum(hess_asr)[0])
order = np.argsort(np.abs(f))
optical = np.delete(f, order[:3])
print("summary        after ASR: acoustic max |w| = %.2f cm-1, lowest optical = %.4f THz, "
      "imaginary optical modes = %d"
      % (np.abs(f[order[:3]]).max() * CM1, optical.min(), int((optical < 0).sum())))
