#!/usr/bin/env python3
"""Recompute canonical SLME for 4 structures from the public PBE optical data.

Run from any working directory:
    python3 first_principles/09_slme/scripts/recompute_slme.py

This script has no external Python dependencies. The results are derived from
canonical optical data and canonical non-SOC PBE/HSE06 gaps; they are not
copied from or fitted to earlier manuscript SLME values.
"""
import bisect
import csv
import hashlib
import math
from pathlib import Path

SLME_DIR = Path(__file__).resolve().parents[1]
OPTICAL_DIR = SLME_DIR.parent / '07_optical' / 'plotting_data'
SOLAR = SLME_DIR / 'solar_spectrum' / 'ASTM_G173_AM1.5G.csv'
RESULT = SLME_DIR / 'results' / 'slme_canonical_results.csv'

CASES = [
    ('Cs2GeSnCl2Br4', 'parent', 0.694182, 1.168815),
    ('Cs2GeSnCl2Br4', 'final_P1', 1.488056, 2.116285),
    ('Cs2GeSnCl4Br2', 'parent', 0.713850, 1.205662),
    ('Cs2GeSnCl4Br2', 'final_P1', 1.620450, 2.271259),
]

EXPECTED_SHA256 = {
    'ASTM_G173_AM1.5G.csv': '01f52e67a2309338a1bba35380e2189fc636cb7bfc32f4b83b236ce770f92b95',
    'Cs2GeSnCl2Br4_parent_optical_full.csv': '03d792e397b2d2a0d52b3c2c572adf8d5028d74bf2c5b7eca756a51a22ceca1a',
    'Cs2GeSnCl2Br4_P1_optical_full.csv': 'd60cd69249e68c01606aa4774f708d610689b4a8d397b8e9b6a5721dba48b01e',
    'Cs2GeSnCl4Br2_parent_optical_full.csv': '2c07df4822583fb952b41d7c9843834a1b6ad9495fbf00793eb7a22cd14f151c',
    'Cs2GeSnCl4Br2_P1_optical_full.csv': '6d354935ff787c2c69e673fe71367db9ddbd28373ff55b2a66d697a819c00fc0',
}

q = 1.602176634e-19
h = 6.62607015e-34
c = 2.99792458e8
kB = 1.380649e-23
T = 300.0
F_R = 1.0
THICKNESSES_UM = (0.5, 1.0, 2.0)


def sha256(path):
    with path.open('rb') as stream:
        dig = hashlib.sha256()
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            dig.update(block)
        return dig.hexdigest()


def require_expected_input(path):
    got = sha256(path)
    expected = EXPECTED_SHA256[path.name]
    if got != expected:
        raise RuntimeError(
            f'Input checksum mismatch for {path}.\n'
            f'  expected: {expected}\n  actual:   {got}\n'
            'Do not overwrite the published canonical result with changed input.')
    return got


def read_csv(path, xcol, ycol):
    with path.open(newline='', encoding='utf-8-sig') as f:
        rd = csv.DictReader(f)
        if not {xcol, ycol}.issubset(rd.fieldnames or []):
            raise ValueError(f'{path}: missing required columns')
        arr = [(float(r[xcol]), float(r[ycol])) for r in rd]
    if len(arr) < 2 or any(arr[i][0] >= arr[i+1][0] for i in range(len(arr)-1)):
        raise ValueError(f'{path}: invalid or non-increasing grid')
    if any(not (math.isfinite(x) and math.isfinite(y)) for x, y in arr):
        raise ValueError(f'{path}: non-finite data')
    return [x for x, _ in arr], [y for _, y in arr]


def trapz(x, y):
    return sum((x[i+1] - x[i]) * (y[i+1] + y[i]) * 0.5
               for i in range(len(x)-1))


def linear(x, xp, yp):
    if x < xp[0] or x > xp[-1]:
        return 0.0
    j = bisect.bisect_left(xp, x)
    if j == 0:
        return yp[0]
    if j == len(xp):
        return yp[-1]
    t = (x - xp[j-1]) / (xp[j] - xp[j-1])
    return yp[j-1] + t * (yp[j] - yp[j-1])


def blackbody(e_eV):
    if e_eV <= 0:
        return 0.0
    e_j = e_eV * q
    x = e_j / (kB * T)
    if x > 700:
        return 0.0
    return (2 * math.pi * e_j**2 / (h**3 * c**2)) * q / math.expm1(x)


def compute_case(comp, phase, pbe, hse, wl, irr, pin):
    optical_name = f'{comp}_{"parent" if phase == "parent" else "P1"}_optical_full.csv'
    optical_path = OPTICAL_DIR / optical_name
    file_sha = require_expected_input(optical_path)
    E, alpha = read_csv(optical_path, 'Energy_eV', 'alpha_from_epsavg_cm-1')
    if len(E) != 3000:
        raise ValueError(f'{optical_path}: expected 3000 optical grid points')
    shift = hse - pbe
    shifted = [x + shift for x in E]

    def alpha_at(e):
        return 0.0 if e < hse else max(0.0, linear(e, shifted, alpha))

    bb_energies = [e for e in shifted if e >= hse]
    bb_alphas = [alpha_at(e) for e in bb_energies]
    bb_flux = [blackbody(e) for e in bb_energies]
    sun_energies = [h*c/(q * nm * 1e-9) for nm in wl]
    sun_photon_flux = [flux * (nm * 1e-9)/(h*c) for nm, flux in zip(wl, irr)]

    output = []
    for thickness in THICKNESSES_UM:
        length_cm = thickness * 1e-4
        jsc = q * trapz(wl, [flux * (1 - math.exp(-2 * alpha_at(e) * length_cm))
                               for flux, e in zip(sun_photon_flux, sun_energies)])
        j0 = q * trapz(bb_energies,
                      [flux * (1 - math.exp(-2 * a * length_cm))
                       for flux, a in zip(bb_flux, bb_alphas)]) / F_R
        if jsc <= 0 or j0 <= 0:
            raise ValueError(f'Non-positive Jsc/J0: {comp} {phase} {thickness}')
        voc = (kB * T / q) * math.log1p(jsc / j0)
        vmax = 1.05 * voc
        max_power = max(v * (jsc - j0 * math.expm1(q*v/(kB*T)))
                        for v in (vmax*i/20000 for i in range(20001)))
        slme = 100 * max_power / pin
        ff = 100 * max_power / (jsc * voc)
        output.append([comp, phase, thickness, pbe, hse, shift, len(E), pin,
                       slme, jsc * 0.1, voc, ff, j0, optical_name, file_sha])
    return output


def main():
    require_expected_input(SOLAR)
    wl, irr = read_csv(SOLAR, 'Wavelength_nm', 'AM1.5G_W_m-2_nm-1')
    pin = trapz(wl, irr)
    if len(wl) != 2002 or not (999 < pin < 1002):
        raise ValueError('Unexpected ASTM solar spectrum or input power')
    print(f'Solar: {SOLAR}\nP_in={pin:.9f} W/m^2, N_solar={len(wl)}')
    results = []
    for args in CASES:
        r = compute_case(*args, wl, irr, pin)
        results.extend(r)
        print(f'\n{args[0]} {args[1]}:')
        for entry in r:
            print(f'  {entry[2]:.1f} um: {entry[8]:.8f}%'
                  f'  Jsc={entry[9]:.6f} mA/cm2, Voc={entry[10]:.6f} V')
    RESULT.parent.mkdir(parents=True,exist_ok=True)
    with RESULT.open('w',newline='') as f:
        wr = csv.writer(f)
        wr.writerow(['Composition','Structure','Thickness_um','Eg_PBE_eV',
                    'Eg_HSE06_eV','scissors_shift_eV','optical_grid_points',
                    'Pin_W_m2','SLME_percent','Jsc_mA_cm2','Voc_V',
                    'FF_percent','J0_A_m2','optical_file','optical_SHA256'])
        wr.writerows(results)
    print(f'\nSaved {len(results)} rows to {RESULT}')


if __name__ == '__main__':
    main()
