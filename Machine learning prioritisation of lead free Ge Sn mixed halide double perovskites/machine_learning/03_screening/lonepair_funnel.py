"""Share of screened A2BB'X6 compositions whose B sites carry an ns2 lone-pair
cation (Ge2+, Sn2+, Pb2+, In+, Tl+, As3+, Sb3+, Bi3+), at each screening stage.

    python lonepair_funnel.py screening_12513.csv

Oxidation states follow the B-site pools of SI Table S1; a composition counts
only if every charge-balanced assignment of its B/B' pair contains an ns2 ion
("always"), and is reported separately if only some assignments do ("ambiguous").
"""
import csv
import re
import sys

POOL = {
    1: set('Li Na K Rb Cs Cu Ag Au Tl In'.split()),
    2: set('Be Mg Ca Sr Ba Zn Cd Hg Ge Sn Pb Mn Fe Co Ni Cu Eu Yb'.split()),
    3: set('Al Ga In Tl Sc Y La Ce Pr Nd Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Bi Sb As Fe Cr Mn Co Ni Rh Ir'.split()),
}
NS2 = {('Ge', 2), ('Sn', 2), ('Pb', 2), ('In', 1), ('Tl', 1), ('As', 3), ('Sb', 3), ('Bi', 3)}
HALIDES = {'Cl', 'Br', 'I'}


def b_pair(formula):
    tok = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
    metals = [e for e, _ in tok if e not in HALIDES]
    if len(metals) == 2:            # B = A element, e.g. Cs2CsBiCl6 written as Cs3BiCl6
        return metals[0], metals[1]
    return metals[1], metals[2]


def lone_pair(formula):
    b, bp = b_pair(formula)
    hits = [((b, o1), (bp, o2)) for o1, o2 in ((1, 3), (3, 1), (2, 2))
            if b in POOL[o1] and bp in POOL[o2]]
    flags = [any(x in NS2 for x in h) for h in hits]
    if not hits:
        return 'unassigned'
    return 'always' if all(flags) else ('ambiguous' if any(flags) else 'none')


def main(path):
    rows = list(csv.DictReader(open(path, newline='')))
    true = lambda r, k: r[k].strip().lower() in ('true', '1')
    stages = [
        ('descriptor-ready', lambda r: True),
        ('stable', lambda r: true(r, 'pass_stability')),
        ('+ geometry', lambda r: true(r, 'pass_stability') and true(r, 'pass_geometry')),
        ('+ direct', lambda r: true(r, 'pass_stability') and true(r, 'pass_geometry') and true(r, 'pass_direct')),
        ('+ gap window', lambda r: true(r, 'pass_stability') and true(r, 'pass_geometry')
         and true(r, 'pass_direct') and true(r, 'pass_gap_window')),
        ('retained', lambda r: true(r, 'final_retained')),
    ]
    for name, keep in stages:
        sel = [lone_pair(r['formula']) for r in rows if keep(r)]
        n = len(sel)
        a, m = sel.count('always'), sel.count('ambiguous')
        print(f'{name:17s} n={n:6d}  ns2 always {a:5d} ({100 * a / n:5.1f}%)  ambiguous {m:4d}  '
              f'unassigned {sel.count("unassigned")}')
    for r in rows:
        if true(r, 'final_retained'):
            print(f'  {r["formula"]:16s} {lone_pair(r["formula"])}')


if __name__ == '__main__':
    main(sys.argv[1])
