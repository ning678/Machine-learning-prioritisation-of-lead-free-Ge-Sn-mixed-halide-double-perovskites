from pathlib import Path
import csv
import hashlib
import math
import re
import xml.etree.ElementTree as ET
import numpy as np

ROOT = Path("/home/qnxu/Ms/Fig7_optical_data")
OUT  = ROOT / "JMCA_final"
OUT.mkdir(parents=True, exist_ok=True)

HC_eV_cm = 1.239841984e-4  # h*c in eV cm

cases = [
    {
        "panel":"parent_Cl2Br4",
        "name":"Cs2GeSnCl2Br4_parent",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl2Br4/VASP/04_C20_EQUIV_PARENT/06_optics_666"),
        "old_full":ROOT/"Cs2GeSnCl2Br4_parent_optical_full.csv",
        "old_06":ROOT/"Cs2GeSnCl2Br4_parent_optical_0_6eV.csv",
    },
    {
        "panel":"P1_Cl2Br4",
        "name":"Cs2GeSnCl2Br4_P1",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl2Br4/VASP/03_FINAL_P1/02_optical/03_pbe_optical_555"),
        "old_full":ROOT/"Cs2GeSnCl2Br4_P1_optical_full.csv",
        "old_06":ROOT/"Cs2GeSnCl2Br4_P1_optical_0_6eV.csv",
    },
    {
        "panel":"parent_Cl4Br2",
        "name":"Cs2GeSnCl4Br2_parent",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl4Br2/VASP/09_optical/01_pbe_optical_888"),
        "old_full":ROOT/"Cs2GeSnCl4Br2_parent_optical_full.csv",
        "old_06":ROOT/"Cs2GeSnCl4Br2_parent_optical_0_6eV.csv",
    },
    {
        "panel":"P1_Cl4Br2",
        "name":"Cs2GeSnCl4Br2_P1",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl4Br2/VASP/19_finalP1_electronic/01_FINAL_postISIF3_canonical/08_pbe_optical_666"),
        "old_full":ROOT/"Cs2GeSnCl4Br2_distorted_optical_full.csv",
        "old_06":ROOT/"Cs2GeSnCl4Br2_distorted_optical_0_6eV.csv",
    },
]

def sha256(fn):
    h = hashlib.sha256()
    with fn.open("rb") as f:
        for b in iter(lambda: f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def read_density_density(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    blocks = []
    for elem in root.iter():
        tag = elem.tag.split("}")[-1]
        if tag == "dielectricfunction" and elem.attrib.get("comment") == "density-density":
            blocks.append(elem)

    if len(blocks) != 1:
        raise RuntimeError(
            f"{xmlfile}: expected exactly one density-density block, got {len(blocks)}"
        )

    block = blocks[0]

    def get_rows(partname):
        target = None
        for child in block.iter():
            if child.tag.split("}")[-1] == partname:
                target = child
                break

        if target is None:
            raise RuntimeError(f"{xmlfile}: missing {partname}")

        rows = []
        for r in target.iter():
            if r.tag.split("}")[-1] == "r":
                rows.append([float(x) for x in r.text.split()])

        return np.asarray(rows, dtype=float)

    imag = get_rows("imag")
    real = get_rows("real")

    if imag.shape != real.shape:
        raise RuntimeError(
            f"{xmlfile}: real/imag shapes differ {real.shape} {imag.shape}"
        )

    if imag.shape[1] < 7:
        raise RuntimeError(
            f"{xmlfile}: expected 7 dielectric columns, got {imag.shape[1]}"
        )

    if not np.allclose(real[:,0], imag[:,0]):
        raise RuntimeError(f"{xmlfile}: real/imag energy grids differ")

    return real, imag

def optical_from_eps(e1, e2, E):
    mod = np.sqrt(e1*e1 + e2*e2)

    n2 = np.maximum((mod + e1)/2.0, 0.0)
    k2 = np.maximum((mod - e1)/2.0, 0.0)

    n = np.sqrt(n2)
    k = np.sqrt(k2)

    alpha = 4.0*np.pi*k*E/HC_eV_cm  # cm^-1

    denom = (n + 1.0)**2 + k**2
    R = ((n - 1.0)**2 + k**2) / denom

    return n, k, alpha, R

def read_csv_header(fn):
    if not fn.exists():
        return None
    with fn.open(errors="ignore") as f:
        return next(csv.reader(f), None)

report = []

for c in cases:
    xml = c["src"] / "vasprun.xml"

    real, imag = read_density_density(xml)

    E = real[:,0]

    # VASP column convention:
    # E xx yy zz xy yz zx
    e1xx,e1yy,e1zz = real[:,1],real[:,2],real[:,3]
    e2xx,e2yy,e2zz = imag[:,1],imag[:,2],imag[:,3]

    # ----------------------------------------------------
    # Method A: average epsilon tensor trace first
    # ----------------------------------------------------
    e1avg = (e1xx + e1yy + e1zz)/3.0
    e2avg = (e2xx + e2yy + e2zz)/3.0

    n_avg, k_avg, alpha_avg, R_avg = optical_from_eps(
        e1avg, e2avg, E
    )

    # ----------------------------------------------------
    # Method B: derive directionally, then average
    # only for audit/comparison
    # ----------------------------------------------------
    nx,kx,ax,Rx = optical_from_eps(e1xx,e2xx,E)
    ny,ky,ay,Ry = optical_from_eps(e1yy,e2yy,E)
    nz,kz,az,Rz = optical_from_eps(e1zz,e2zz,E)

    n_diravg = (nx+ny+nz)/3.0
    k_diravg = (kx+ky+kz)/3.0
    alpha_diravg = (ax+ay+az)/3.0
    R_diravg = (Rx+Ry+Rz)/3.0

    data = np.column_stack([
        E,
        e1xx,e1yy,e1zz,e1avg,
        e2xx,e2yy,e2zz,e2avg,
        n_avg,k_avg,alpha_avg,R_avg,
        n_diravg,k_diravg,alpha_diravg,R_diravg,
    ])

    cols = [
        "Energy_eV",
        "eps1_xx","eps1_yy","eps1_zz","eps1_avg",
        "eps2_xx","eps2_yy","eps2_zz","eps2_avg",
        "n_from_epsavg",
        "k_from_epsavg",
        "alpha_from_epsavg_cm-1",
        "R_from_epsavg",
        "n_directional_avg",
        "k_directional_avg",
        "alpha_directional_avg_cm-1",
        "R_directional_avg",
    ]

    fullout = OUT / f"{c['name']}_optical_full.csv"
    out06   = OUT / f"{c['name']}_optical_0_6eV.csv"

    with fullout.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(data)

    mask = (E >= 0.0) & (E <= 6.0)

    with out06.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(data[mask])

    report += [
        "",
        "="*90,
        c["name"],
        f"source = {xml}",
        f"source_sha256 = {sha256(xml)}",
        "dielectric_block = density-density",
        f"points_full = {len(E)}",
        f"points_0_6eV = {mask.sum()}",
        f"E_min = {E.min():.10f}",
        f"E_max = {E.max():.10f}",
        f"strictly_increasing = {bool(np.all(np.diff(E)>0))}",
        f"finite = {bool(np.isfinite(data).all())}",
        f"eps1_avg_E0 = {e1avg[0]:.10f}",
        f"eps2_avg_E0 = {e2avg[0]:.10f}",
        f"n_E0 = {n_avg[0]:.10f}",
        f"k_E0 = {k_avg[0]:.10f}",
        f"alpha_E0_cm-1 = {alpha_avg[0]:.10f}",
        f"R_E0 = {R_avg[0]:.10f}",
        "",
        "HISTORICAL FULL CSV HEADER:",
        str(read_csv_header(c["old_full"])),
        "",
        "HISTORICAL 0-6 eV CSV HEADER:",
        str(read_csv_header(c["old_06"])),
        f"new_full = {fullout}",
        f"new_0_6 = {out06}",
    ]

(OUT/"Fig7_rebuild_audit.txt").write_text(
    "\n".join(report),
    encoding="utf-8"
)

(OUT/"README_Fig7.txt").write_text(
"""Fig.7 JMCA-final optical data provenance

Source:
VASP vasprun.xml, dielectricfunction comment="density-density".

Dielectric tensor averaging:
eps1_avg = (eps1_xx + eps1_yy + eps1_zz)/3
eps2_avg = (eps2_xx + eps2_yy + eps2_zz)/3

Final plotted optical constants are derived from eps1_avg and eps2_avg:

|eps| = sqrt(eps1_avg^2 + eps2_avg^2)

n = sqrt[(|eps| + eps1_avg)/2]

k = sqrt[(|eps| - eps1_avg)/2]

alpha = 4*pi*k*E/(h*c), in cm^-1
with h*c = 1.239841984e-4 eV cm

R = [ (n-1)^2 + k^2 ] / [ (n+1)^2 + k^2 ]

No smoothing.
No interpolation.
No resampling.
No HSE06 scissors correction.

The directional-average optical constants are retained in the CSV
only for audit purposes. The publication plots should use the
'_from_epsavg' columns.

Fig.7 should use only the two final P1 structures:
Cs2GeSnCl2Br4_P1
Cs2GeSnCl4Br2_P1

Parent optical data are retained for SLME/provenance comparisons.
""",
encoding="utf-8"
)

print("\n".join(report))
print()
print("FINAL DATA DIRECTORY =", OUT)
