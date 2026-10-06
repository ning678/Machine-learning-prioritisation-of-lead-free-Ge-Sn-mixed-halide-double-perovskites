# JMCA machine-learning public data package

This directory contains the minimal public data needed to inspect the machine-learning results reported in the JMCA manuscript.

## Contents

- `01_training_data`: final modelling tables for stability classification (1,144 records), direct/indirect classification (884 records), and reference-gap regression (680 records).
- `02_validation`: one strict nested out-of-fold (OOF) prediction per training sample and metrics recomputed from those public OOF files.
- `03_screening`: the auditable candidate funnel, exact training-overlap audit, and 33 retained training-unseen candidates.
- `04_SHAP`: signed deployment-model SHAP values in a common long format.
- `05_reproducibility`: final model settings, feature definitions, provenance, and checksums.

## Validation and deployment

Strict nested OOF evaluation and full-data deployment are different procedures. OOF evaluates the complete model-selection workflow on held-out outer folds. Deployment models were selected/refit on all final training data for prospective screening and SHAP analysis: LGBMClassifier-Top20 for stability, RandomForestClassifier-Top15 for direct/indirect character, and ExtraTreesRegressor-Top20 for the reference gap.

The prospective funnel is 12,513 -> 1,981 -> 1,914 -> 288 -> 35 -> 33. `S_stable` and `S_direct` are uncalibrated ranking scores, not posterior probabilities. `screening_12513.csv` was assembled only by formula-keyed left joins of locked stage outputs; no score was predicted again. Scores for candidates that did not reach a later stage remain missing, not zero.

## Derived columns and SHAP provenance

In `gap_nested_oof.csv`, `residual` is derived as `E_g_ML_oof - E_g_ref`; the reference and prediction values are unchanged. SHAP values were not recomputed. The public SHAP files only add identifiers, join feature values, and convert the locked wide files to long format. The direct SHAP source has no row ID, so its 884 rows are mapped positionally to the verified original row order of `training_884_clean28.csv`; changing that order invalidates the mapping.

The stability training matrix retains its original missing geometry descriptors as empty CSV fields. Median imputation was fitted within each cross-validation training fold, not globally before OOF evaluation.

## Reproducibility boundary

The exact executed code/environment has not yet been fully locked for all three tasks. Current notebooks, model binaries, and guessed package versions are excluded. This package supports numerical inspection of the reported ML results but does not claim complete code-level rerun reproducibility.
