Fig.7 JMCA-final optical data provenance

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
