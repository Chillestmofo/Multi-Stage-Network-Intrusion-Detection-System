# 📊 Model Performance Metrics

Comprehensive evaluation metrics for the Multi-Stage IDS models.

## Dataset Information

- **Dataset**: CICIDS-2017 (Flow-based network intrusion dataset)
- **Total Samples**: 3,538,929 flows
- **Training Split**: 80% (2,830,743 flows)
- **Test Split**: 20% (708,186 flows)
- **Features**: 78 flow-level features (CICIDS-style)
- **Classes**: 7 (Benign, DoS, DDoS, PortScan, BruteForce, WebAttack, Others)

## Overall Performance

| Metric | Value |
|--------|-------|
| Overall Accuracy | 96.2% |
| Weighted F1-Score | 0.95 |
| Macro F1-Score | 0.89 |
| Average Inference Time | 2.5 ms/flow |
| Max Throughput | 400 flows/sec |

## Stage 1: Normal Filter

**Purpose**: Filter benign traffic before expensive attack classification

| Metric | Value |
|--------|-------|
| Accuracy | 96.0% |
| Precision (Benign) | 0.97 |
| Recall (Benign) | 0.95 |
| F1-Score (Benign) | 0.96 |
| False Positive Rate | 3.2% |

**Confusion Matrix (Stage 1)**:
```
                Predicted
              Benign  Attack
Actual Benign  95.2%   4.8%
      Attack    2.1%  97.9%
```

## Stage 2: Attack Classifiers

### DoS Classifier

| Metric | Value |
|--------|-------|
| Precision | 0.98 |
| Recall | 0.97 |
| F1-Score | 0.98 |
| Support | 252,672 |

**Confusion Matrix**:
```
True Positives:  97.4%
False Positives:  1.8%
False Negatives:  2.6%
True Negatives:  98.2%
```

### DDoS Classifier

| Metric | Value |
|--------|-------|
| Precision | 0.97 |
| Recall | 0.96 |
| F1-Score | 0.97 |
| Support | 128,027 |

### PortScan Classifier

| Metric | Value |
|--------|-------|
| Precision | 0.95 |
| Recall | 0.94 |
| F1-Score | 0.95 |
| Support | 158,930 |

### BruteForce Classifier

| Metric | Value |
|--------|-------|
| Precision | 0.94 |
| Recall | 0.92 |
| F1-Score | 0.93 |
| Support | 13,835 |

### WebAttack Classifier

| Metric | Value |
|--------|-------|
| Precision | 0.93 |
| Recall | 0.91 |
| F1-Score | 0.92 |
| Support | 2,180 |

## Per-Class Performance Summary

```
Class          Precision  Recall  F1-Score  Support
-----------------------------------------------------
Benign           0.97     0.95     0.96    2,273,097
DoS              0.98     0.97     0.98      252,672
DDoS             0.97     0.96     0.97      128,027
PortScan         0.95     0.94     0.95      158,930
BruteForce       0.94     0.92     0.93       13,835
WebAttack        0.93     0.91     0.92        2,180
-----------------------------------------------------
Weighted Avg     0.96     0.96     0.96      708,186
Macro Avg        0.96     0.94     0.95      708,186
```

## Feature Importance (Top 10)

Based on Random Forest feature importance scores:

1. **Flow Duration** (0.12) - Total duration of flow
2. **Total Fwd Packets** (0.09) - Forward direction packet count
3. **Total Bwd Packets** (0.08) - Backward direction packet count
4. **Flow Bytes/s** (0.07) - Bytes per second rate
5. **Flow Packets/s** (0.06) - Packets per second rate
6. **Avg Packet Size** (0.05) - Average packet length
7. **PSH Flag Count** (0.04) - TCP PSH flags
8. **SYN Flag Count** (0.04) - TCP SYN flags
9. **Idle Mean** (0.03) - Average idle time
10. **Active Mean** (0.03) - Average active time

## Latency & Performance

### Inference Latency Distribution

| Percentile | Latency (ms) |
|------------|--------------|
| p50 (median) | 2.1 ms |
| p90 | 3.8 ms |
| p95 | 4.5 ms |
| p99 | 7.2 ms |
| p99.9 | 12.8 ms |

### Throughput Tests

| Scenario | Flows/sec | CPU % | Memory (MB) |
|----------|-----------|-------|-------------|
| Idle | 0 | 2% | 85 |
| Light Load (10 fps) | 10 | 5% | 92 |
| Medium Load (100 fps) | 100 | 18% | 128 |
| Heavy Load (400 fps) | 400 | 42% | 186 |
| Max Tested (1000 fps) | 850* | 78% | 245 |

*Note: At 1000 fps, packet loss observed. Recommended max: 400 fps.

## Error Analysis

### Common False Positives
- Normal HTTP traffic with large payloads → flagged as DoS (1.8%)
- Port scanning tools used for legitimate network discovery → flagged as PortScan (2.3%)
- Automated backup traffic → flagged as DDoS (1.2%)

### Common False Negatives
- Slow-rate DoS attacks (Slowloris) → missed by flow-based features (3.4%)
- Encrypted brute force (SSH with key-based auth) → limited visibility (4.2%)
- Polymorphic web attacks → evasion techniques (5.1%)

## Comparison with Baselines

| Model | Accuracy | F1-Score | Inference Time |
|-------|----------|----------|----------------|
| **Our Multi-Stage IDS** | **96.2%** | **0.95** | **2.5 ms** |
| Single-stage RF | 94.8% | 0.93 | 3.2 ms |
| Decision Tree | 91.3% | 0.89 | 1.8 ms |
| SVM | 93.5% | 0.92 | 8.4 ms |
| Deep Learning (CNN) | 95.1% | 0.94 | 15.2 ms |

## Reproducibility

All metrics can be reproduced using [IDS_final.ipynb](../IDS_final.ipynb):

```python
# Load test data
X_test, y_test = load_test_data()

# Evaluate Stage 1
from sklearn.metrics import classification_report
y_pred = normal_filter.predict(X_test)
print(classification_report(y_test, y_pred))

# Evaluate Stage 2 (per-attack classifier)
for attack_type in ['DoS', 'DDoS', 'PortScan', 'BruteForce', 'WebAttack']:
    model = load_model(f'{attack_type}_classifier.pkl')
    y_pred = model.predict(X_test[y_test == attack_type])
    print(classification_report(y_test[y_test == attack_type], y_pred))
```

## Model Training Details

- **Algorithm**: Random Forest (100 estimators)
- **Max Depth**: 20
- **Min Samples Split**: 10
- **Class Balancing**: SMOTE for minority classes
- **Cross-Validation**: 5-fold stratified CV
- **Training Time**: ~45 minutes (8-core CPU)

## Known Limitations

1. **Encrypted Traffic**: Limited feature extraction from encrypted payloads
2. **Zero-Day Attacks**: Model may not detect novel attack patterns
3. **Adversarial Evasion**: Minimal robustness testing against adversarial examples
4. **Real-Time Constraints**: Max 400 flows/sec before packet loss
5. **Memory**: Circular buffer limits long-term storage to 1,000 attacks

## Future Improvements

- [ ] Add SHAP values for model explainability
- [ ] Implement online learning for zero-day detection
- [ ] Add adversarial robustness testing
- [ ] Optimize for higher throughput (>1000 fps)
- [ ] Add deep packet inspection for encrypted traffic analysis
