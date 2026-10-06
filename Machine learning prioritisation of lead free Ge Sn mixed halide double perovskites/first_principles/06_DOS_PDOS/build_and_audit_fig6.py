from pathlib import Path
import csv
import hashlib
import numpy as np

ROOT = Path("/home/qnxu/Ms/Fig6_dos_data")
OUT  = ROOT / "JMCA_final"
OUT.mkdir(parents=True, exist_ok=True)

cases = [
    {
        "panel":"a",
        "name":"Cs2GeSnCl2Br4_parent",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl2Br4/VASP/04_C20_EQUIV_PARENT/05_dos_999"),
        "species":["Cs","Ge","Sn","Cl","Br"],
        "counts":[4,2,2,4,8],
        "Z":2,
        "VBM":1.761658,
        "old":ROOT/"Cs2GeSnCl2Br4_parent_dos_pdos.csv",
    },
    {
        "panel":"b",
        "name":"Cs2GeSnCl2Br4_P1",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl2Br4/VASP/03_FINAL_P1/01_electronic/05_pbe_dos_999"),
        "species":["Cs","Ge","Sn","Cl","Br"],
        "counts":[8,4,4,8,16],
        "Z":4,
        "VBM":1.002609,
        "old":ROOT/"Cs2GeSnCl2Br4_P1_dos_pdos.csv",
    },
    {
        "panel":"c",
        "name":"Cs2GeSnCl4Br2_parent",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl4Br2/VASP/05_pbe_dos/01_dos_888"),
        "species":["Cs","Ge","Sn","Cl","Br"],
        "counts":[4,2,2,8,4],
        "Z":2,
        "VBM":1.927202,
        "old":ROOT/"Cs2GeSnCl4Br2_parent_dos_pdos.csv",
    },
    {
        "panel":"d",
        "name":"Cs2GeSnCl4Br2_P1",
        "src":Path("/home/qnxu/Ms/Cs2GeSnCl4Br2/VASP/19_finalP1_electronic/01_FINAL_postISIF3_canonical/07_dos_pdos/01_pbe_dos_999"),
        "species":["Cs","Ge","Sn","Cl","Br"],
        "counts":[4,2,2,8,4],
        "Z":2,
        "VBM":0.984933,
        "old":ROOT/"Cs2GeSnCl4Br2_distorted_dos_pdos.csv",
    },
]

def sha256(fn):
    h = hashlib.sha256()
    with fn.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def read_doscar(fn, species, counts):
    lines = fn.read_text(errors="ignore").splitlines()

    hdr = lines[5].split()
    nedos = int(hdr[2])

    total = np.array([
        [float(x) for x in line.split()]
        for line in lines[6:6+nedos]
    ])

    E = total[:,0]
    TDOS = total[:,1]

    atom_species = []
    for sp,n in zip(species,counts):
        atom_species += [sp]*n

    pdos = {
        sp:{
            "s":np.zeros(nedos),
            "p":np.zeros(nedos),
            "d":np.zeros(nedos)
        }
        for sp in species
    }

    pos = 6 + nedos

    for iatom,sp in enumerate(atom_species):
        # one DOS header per atom
        pos += 1

        block = np.array([
            [float(x) for x in lines[pos+j].split()]
            for j in range(nedos)
        ])
        pos += nedos

        # LORBIT=11, non-spin:
        # E s py pz px dxy dyz dz2 dxz dx2-y2
        pdos[sp]["s"] += block[:,1]
        pdos[sp]["p"] += block[:,2] + block[:,3] + block[:,4]

        if block.shape[1] >= 10:
            pdos[sp]["d"] += block[:,5:10].sum(axis=1)

    return E,TDOS,pdos,nedos

columns = [
    "Energy_eV",
    "Energy_minus_VBM_eV",
    "TDOS_per_fu",
    "Cs_s_per_fu","Cs_p_per_fu","Cs_d_per_fu",
    "Ge_s_per_fu","Ge_p_per_fu","Ge_d_per_fu",
    "Sn_s_per_fu","Sn_p_per_fu","Sn_d_per_fu",
    "Cl_s_per_fu","Cl_p_per_fu","Cl_d_per_fu",
    "Br_s_per_fu","Br_p_per_fu","Br_d_per_fu",
]

report = []

for c in cases:

    doscar = c["src"]/"DOSCAR"

    E,T,p,nedos = read_doscar(
        doscar,c["species"],c["counts"]
    )

    Z = c["Z"]
    Erel = E-c["VBM"]
    T = T/Z

    for sp in p:
        for orb in p[sp]:
            p[sp][orb] /= Z

    data = np.column_stack([
        E,
        Erel,
        T,
        p["Cs"]["s"],p["Cs"]["p"],p["Cs"]["d"],
        p["Ge"]["s"],p["Ge"]["p"],p["Ge"]["d"],
        p["Sn"]["s"],p["Sn"]["p"],p["Sn"]["d"],
        p["Cl"]["s"],p["Cl"]["p"],p["Cl"]["d"],
        p["Br"]["s"],p["Br"]["p"],p["Br"]["d"],
    ])

    out = OUT/f"Fig6{c['panel']}_{c['name']}_DOS_PDOS.csv"

    with out.open("w",newline="") as f:
        w=csv.writer(f)
        w.writerow(columns)
        w.writerows(data)

    report.append("")
    report.append("="*80)
    report.append(c["name"])
    report.append(f"source = {doscar}")
    report.append(f"source_sha256 = {sha256(doscar)}")
    report.append(f"NEDOS = {nedos}")
    report.append(f"N_atoms = {sum(c['counts'])}")
    report.append(f"Z = {Z}")
    report.append(f"VBM = {c['VBM']:.9f}")
    report.append(f"output = {out}")
    report.append(f"energy_strictly_increasing = {np.all(np.diff(E)>0)}")
    report.append(f"finite = {np.isfinite(data).all()}")

    # ---------------------------------------------------------
    # Compare with historical CSV
    # ---------------------------------------------------------
    if c["old"].exists():
        old = np.genfromtxt(
            c["old"],
            delimiter=",",
            names=True,
            dtype=float
        )

        report.append(f"historical_csv = {c['old']}")

        if len(old) != len(data):
            report.append(
                f"OLD_COMPARE = DIFFERENT ROW COUNT "
                f"{len(old)} vs {len(data)}"
            )
        else:
            report.append("OLD_COMPARE = same row count")

            for j,col in enumerate(columns):
                if col in old.dtype.names:
                    diff = np.max(
                        np.abs(old[col]-data[:,j])
                    )
                    report.append(
                        f"max_abs_diff {col} = {diff:.12e}"
                    )
    else:
        report.append("historical_csv = NOT FOUND")

(OUT/"Fig6_rebuild_audit.txt").write_text(
    "\n".join(report),
    encoding="utf-8"
)

(OUT/"README.txt").write_text(
"""Fig.6 locked plotting data

Source:
Four audited VASP DOSCAR files.

Processing:
- non-spin LORBIT=11 projected DOS;
- all atoms of each element are summed;
- p = px + py + pz;
- d = sum of five d projections;
- TDOS and every PDOS channel are divided by Z,
  the number of formula units per computational cell;
- energies are aligned to the corresponding SCF VBM;
- no smoothing;
- no interpolation;
- no filtering;
- no resampling.

Z:
a = 2
b = 4
c = 2
d = 2

VBM / eV:
a = 1.761658
b = 1.002609
c = 1.927202
d = 0.984933

Final plotted DOS unit:
states eV^-1 f.u.^-1
""",
encoding="utf-8"
)

print("\n".join(report))
print()
print("FINAL DATA DIRECTORY =",OUT)
