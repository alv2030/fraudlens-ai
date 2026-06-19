# Model Card

## Model purpose

Classify transaction fraud risk for analyst triage in a portfolio demo environment.

## Intended use

- Demonstrate ML pipeline design.
- Demonstrate fraud scoring API design.
- Demonstrate explainable alert triage.

## Not intended for

- Real payment approval/decline decisions.
- PCI-regulated production environments.
- Consumer credit or eligibility decisions.

## Metrics

Use PR-AUC, ROC-AUC, precision, recall, F1, and confusion matrix.

## Known limitations

- Synthetic data distribution may not represent real fraud.
- Fraud labels in real environments are delayed and noisy.
- Model requires drift monitoring and retraining in production.
