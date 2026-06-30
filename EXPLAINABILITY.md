# 🔍 Model Explainability with SHAP

This document demonstrates how to interpret IDS model predictions using SHAP (SHapley Additive exPlanations).

## What is SHAP?

SHAP values explain individual predictions by quantifying the contribution of each feature to the model's decision.

- **Positive SHAP value** → feature pushes prediction toward attack classification
- **Negative SHAP value** → feature pushes prediction toward benign classification
- **Magnitude** → importance of the feature for this specific prediction

## Installation

```bash
pip install shap matplotlib
```

## Basic Usage

### 1. Load Model and Data

```python
import joblib
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt

# Load trained model
model = joblib.load('backend/models/dos_classifier.pkl')

# Load feature names
with open('backend/artifacts/feature_order.json', 'r') as f:
    feature_names = json.load(f)

# Load test data
X_test = pd.read_csv('test_data.csv')  # Your test dataset
```

### 2. Generate SHAP Values

```python
# Create SHAP explainer for tree-based models
explainer = shap.TreeExplainer(model)

# Calculate SHAP values for test set (use subset for speed)
shap_values = explainer.shap_values(X_test[:1000])

# For binary classification, shap_values[1] = attack class
attack_shap = shap_values[1]
```

### 3. Visualize Feature Importance

#### Summary Plot (Global Importance)

```python
# Shows most important features across all predictions
shap.summary_plot(attack_shap, X_test[:1000], feature_names=feature_names)
plt.savefig('shap_summary.png', dpi=300, bbox_inches='tight')
plt.show()
```

**Example Output**:
```
Feature Importance (DoS Attacks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Flow Duration         ████████████████ 0.28
Total Fwd Packets     ████████████ 0.19
Flow Bytes/s          ██████████ 0.15
PSH Flag Count        ████████ 0.12
Total Bwd Packets     ██████ 0.09
...
```

#### Force Plot (Single Prediction)

```python
# Explain why a specific flow was classified as attack
idx = 42  # Index of flow to explain

shap.force_plot(
    explainer.expected_value[1],
    attack_shap[idx],
    X_test.iloc[idx],
    feature_names=feature_names,
    matplotlib=True
)
plt.savefig('shap_force_plot.png', dpi=300, bbox_inches='tight')
```

**Interpretation**:
- Red bars → features increasing attack probability
- Blue bars → features decreasing attack probability
- Base value → model's default prediction
- Output value → final prediction score

### 4. Feature Importance Bar Chart

```python
# Get mean absolute SHAP values
feature_importance = np.abs(attack_shap).mean(axis=0)

# Create DataFrame
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

# Plot top 15 features
plt.figure(figsize=(10, 8))
plt.barh(importance_df['feature'][:15], importance_df['importance'][:15])
plt.xlabel('Mean |SHAP Value|')
plt.title('Top 15 Features for DoS Detection')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance_shap.png', dpi=300)
plt.show()
```

## Example: Explaining DoS Detection

```python
# Sample DoS flow features
dos_sample = {
    'Flow Duration': 45000,        # Very long flow (45s)
    'Total Fwd Packets': 8500,     # Extremely high packet count
    'Total Bwd Packets': 12,       # Very few responses
    'Flow Bytes/s': 125000,        # High byte rate
    'PSH Flag Count': 0,           # No PSH flags (unusual)
    'SYN Flag Count': 1,
    'Avg Packet Size': 1024,
    'Flow Packets/s': 189,         # High packet rate
    # ... other 70 features
}

# Convert to DataFrame
X_sample = pd.DataFrame([dos_sample])

# Predict
prediction = model.predict_proba(X_sample)[0][1]
print(f"DoS Probability: {prediction:.2%}")

# Explain
shap_values_sample = explainer.shap_values(X_sample)
shap.force_plot(
    explainer.expected_value[1],
    shap_values_sample[1][0],
    X_sample.iloc[0],
    matplotlib=True
)
```

**Output Interpretation**:
```
DoS Probability: 99.2%

Top Contributing Features:
✓ Flow Duration (+0.18) - Abnormally long connection
✓ Total Fwd Packets (+0.15) - Massive packet count
✓ Flow Bytes/s (+0.12) - High bandwidth consumption
✓ Total Bwd Packets (-0.08) - Very few responses (suspicious)
✓ PSH Flag Count (+0.06) - No PSH flags (anomalous)
```

## Integration with Dashboard

### Backend Endpoint

Add to `backend/app/api/predict.py`:

```python
import shap
import numpy as np

@router.post("/explain")
def explain_prediction(flow_features: dict):
    """
    Returns SHAP explanation for a prediction
    """
    # Load model and explainer
    model = load_model('dos_classifier')
    explainer = shap.TreeExplainer(model)
    
    # Convert features to array
    X = feature_mapper.map_features(flow_features)
    
    # Get SHAP values
    shap_values = explainer.shap_values(X)
    attack_shap = shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]
    
    # Get top 5 features
    feature_indices = np.argsort(np.abs(attack_shap))[-5:][::-1]
    
    explanations = []
    for idx in feature_indices:
        explanations.append({
            'feature': feature_names[idx],
            'value': float(X[0][idx]),
            'shap_value': float(attack_shap[idx]),
            'impact': 'increases' if attack_shap[idx] > 0 else 'decreases'
        })
    
    return {
        'explanations': explanations,
        'base_value': float(explainer.expected_value[1]),
        'prediction': float(model.predict_proba(X)[0][1])
    }
```

### Frontend Display

Add to detection table in `App.jsx`:

```jsx
const [explanation, setExplanation] = useState(null);

const explainDetection = async (detection) => {
  const response = await fetch(`${API_BASE}/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(detection.features)
  });
  const data = await response.json();
  setExplanation(data);
};

// In table row
<td>
  <button onClick={() => explainDetection(d)}>
    Explain
  </button>
</td>

// Modal/popup
{explanation && (
  <div className="explanation-modal">
    <h3>Why was this classified as {explanation.attack_type}?</h3>
    <ul>
      {explanation.explanations.map(e => (
        <li key={e.feature}>
          <strong>{e.feature}</strong>: {e.value}
          <br />
          <span style={{color: e.shap_value > 0 ? 'red' : 'green'}}>
            {e.impact} attack probability by {Math.abs(e.shap_value).toFixed(3)}
          </span>
        </li>
      ))}
    </ul>
  </div>
)}
```

## Pre-Generated SHAP Visualizations

For demo purposes, generate static SHAP plots:

```python
# Script: backend/scripts/generate_shap_plots.py

import joblib
import shap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load models
attack_types = ['dos', 'ddos', 'portscan', 'bruteforce', 'webattack']

for attack in attack_types:
    model = joblib.load(f'backend/models/{attack}_classifier.pkl')
    X_test = pd.read_csv(f'test_data_{attack}.csv')[:500]
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # Summary plot
    shap.summary_plot(
        shap_values[1], 
        X_test, 
        show=False,
        max_display=10
    )
    plt.savefig(f'frontend/public/shap_{attack}_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Feature importance
    feature_importance = np.abs(shap_values[1]).mean(axis=0)
    importance_df = pd.DataFrame({
        'feature': X_test.columns,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)[:10]
    
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['feature'], importance_df['importance'])
    plt.xlabel('Mean |SHAP Value|')
    plt.title(f'{attack.upper()} Detection - Feature Importance')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f'frontend/public/shap_{attack}_importance.png', dpi=300, bbox_inches='tight')
    plt.close()

print("SHAP visualizations generated!")
```

## Key Insights from SHAP Analysis

### DoS Attacks
- **Flow Duration** (+) - Long-running connections
- **Total Fwd Packets** (+) - High volume of outgoing packets
- **Flow Bytes/s** (+) - Bandwidth saturation

### Port Scanning
- **SYN Flag Count** (+) - Multiple SYN packets
- **Unique Dest Ports** (+) - Scanning many ports
- **Flow Duration** (-) - Very short connections

### Brute Force
- **Flow IAT Mean** (-) - Rapid successive attempts
- **Dst Port** (+) - Targeting SSH/FTP ports (22, 21)
- **Failed Connection Count** (+) - Multiple failures

## Best Practices

1. **Use TreeExplainer for RF models** - Much faster than KernelExplainer
2. **Sample for speed** - SHAP on 1000 samples instead of full dataset
3. **Cache explanations** - Pre-compute for common attack patterns
4. **Simplify for users** - Show top 3-5 features only
5. **Validate consistency** - SHAP should align with feature importance

## Resources

- [SHAP Documentation](https://shap.readthedocs.io/)
- [SHAP GitHub](https://github.com/slundberg/shap)
- [Interpreting ML Models](https://christophm.github.io/interpretable-ml-book/)
