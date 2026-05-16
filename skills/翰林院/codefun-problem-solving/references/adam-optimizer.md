# Adam & AdamW Optimizer Reference

## Adam

### Intuition
SGD + Momentum + Adaptive Learning Rate = Adam

### Core Update (3 steps)
```
t = t + 1                          # global step counter

m = β₁·m + (1-β₁)·g               # 1st moment (EMA of gradient → direction)
v = β₂·v + (1-β₂)·g²              # 2nd moment (EMA of squared gradient → scale)

m̂ = m / (1-β₁ᵗ)                   # bias correction (cold-start compensation)
v̂ = v / (1-β₂ᵗ)

θ = θ - lr · m̂ / (√v̂ + ε)          # parameter update
```

### Key Parameters
| Param | Default | Intuition |
|-------|---------|-----------|
| β₁ | 0.9 | Momentum decay. Higher = more inertia |
| β₂ | 0.999 | Adaptive scale decay. Higher = slower to react to gradient changes |
| ε | 1e-8 | Numerical stability. Changing this rarely matters |
| lr | 0.001 | Base learning rate |

### Bias Correction
Without correction: m and v start at 0, so early steps are underestimated.
`m̂ = m / (1-β₁ᵗ)` compensates — as t grows, denominator → 1, correction fades.

### vs SGD
| | SGD | Adam |
|---|-----|------|
| Direction | Current gradient only | EMA-smoothed (m) |
| Step size | Uniform lr | Adaptive per-parameter (√v̂) |
| Tuning | lr-sensitive | β₁,β₂ usually fine at defaults |

---

## AdamW

### Problem with Adam + L2
Adam's L2 regularization adds `2λθ` to the gradient. This gradient then goes through the m/v adaptive mechanism — **regularization strength gets distorted by the adaptive learning rate**. Sparse features (large effective lr) get over-regularized; frequent features (small effective lr) get under-regularized.

### AdamW Fix: Decoupled Weight Decay
Separate the weight decay from the gradient path:

```python
# AdamW update (decoupled)
θ = θ - lr * m̂ / (√v̂ + ε)    # normal Adam step
θ = θ - lr * λ * θ            # independent weight decay (NOT through gradient)
```

### Why It Matters
- λ and lr become independently tunable
- Better generalization, especially for large models
- SOTA default for transformers and modern architectures

### Interview Answer
Q: "Why AdamW over Adam?"  
A: **Decoupling.** Adam's L2 gets distorted by adaptive learning rates. AdamW applies weight decay directly to parameters, bypassing the gradient statistics.
