# Threshold Strategy

Fraud detection should not rely on the default 0.50 classification threshold.

The system uses a configurable threshold because fraud detection usually prioritizes recall while controlling false positives.

Recommended optimization target:

- Maximize recall for fraud transactions
- Keep false positives within operational review capacity
- Compare thresholds using PR-AUC, precision, recall, F1, and confusion matrix
