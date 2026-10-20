"""Local octahedral geometry of Cs2GeSnX6 structures (manuscript Table 5).

    python local_geometry.py POSCAR [POSCAR ...]

For each Ge and Sn: the six nearest halides (minimum image), the three
shortest and three longest B-X bonds, the off-centre displacement (B to
centroid of its six halides), the bond-length distortion index
Delta_d = 1/6 sum((d_i - d_mean)/d_mean)^2 and the bond-angle variance
sigma^2 = 1/11 sum(theta_i - 90)^2 over the twelve cis angles.
Ge-X-Sn angles are taken over halides shared by one Ge and one Sn.
Only numpy is needed.
"""
import itertools
import sys

import numpy as np


def read_poscar(path):
    lines = open(path).read().split('\n')
    scale = float(lines[1].split()[0])
    lat = np.array([[float(x) for x in lines[i].split()[:3]] for i in (2, 3, 4)]) * scale
    species = lines[5].split()
    counts = [int(x) for x in lines[6].split()]
    i = 7
    if lines[i].strip()[0] in 'Ss':
        i += 1
    direct = lines[i].strip()[0] in 'Dd'
    n = sum(counts)
    pos = np.array([[float(x) for x in lines[i + 1 + k].split()[:3]] for k in range(n)])
    cart = pos @ lat if direct else pos
    sym = [sp for sp, c in zip(species, counts) for _ in range(c)]
    return lat, cart, sym


def octahedra(lat, cart, sym):
    shifts = np.array(list(itertools.product((-1, 0, 1), repeat=3))) @ lat
    halides = [k for k, s in enumerate(sym) if s in ('Cl', 'Br', 'I')]
    out = []
    for b in [k for k, s in enumerate(sym) if s in ('Ge', 'Sn')]:
        cand = []
        for x in halides:
            v = cart[x] + shifts - cart[b]
            d = np.linalg.norm(v, axis=1)
            j = d.argmin()
            cand.append((d[j], x, v[j]))
        cand.sort(key=lambda t: t[0])
        out.append((b, cand[:6]))
    return out


def summarise(path):
    lat, cart, sym = read_poscar(path)
    octs = octahedra(lat, cart, sym)
    print(f'== {path}')
    print(f'  V per f.u. {abs(np.linalg.det(lat)) / sym.count("Ge"):.2f} A^3')
    shared = {}
    for B in ('Ge', 'Sn'):
        short, long_, off, dd, bav = [], [], [], [], []
        for b, nb in octs:
            if sym[b] != B:
                continue
            d = np.array(sorted(t[0] for t in nb))
            vs = np.array([t[2] for t in nb])
            short += list(d[:3])
            long_ += list(d[3:])
            off.append(np.linalg.norm(vs.mean(axis=0)))
            dd.append(np.mean(((d - d.mean()) / d.mean()) ** 2))
            u = vs / np.linalg.norm(vs, axis=1)[:, None]
            ang = np.degrees(np.arccos(np.clip((u @ u.T)[np.triu_indices(6, 1)], -1, 1)))
            bav.append(np.sum((np.sort(ang)[:12] - 90) ** 2) / 11)
        print(f'  {B}-X all {min(short):.3f}-{max(long_):.3f}  short three {min(short):.3f}-{max(short):.3f}  '
              f'long three {min(long_):.3f}-{max(long_):.3f} A')
        print(f'  {B}: off-centre {np.mean(off):.3f} A  Delta_d {np.mean(dd) * 1e3:.2f}e-3  '
              f'sigma^2 {np.mean(bav):.1f} deg^2')
    for b, nb in octs:
        for _, x, v in nb:
            shared.setdefault(x, []).append(v)
    ang = [np.degrees(np.arccos(np.clip(np.dot(v[0], v[1]) / np.linalg.norm(v[0]) / np.linalg.norm(v[1]), -1, 1)))
           for v in shared.values() if len(v) == 2]
    print(f'  Ge-X-Sn {min(ang):.1f}-{max(ang):.1f} deg (n={len(ang)})')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        summarise(p)
