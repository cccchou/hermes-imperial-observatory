# ML Interview: GRPO + SDAR Formula Reference

> Condensed from paper deep-dive session. Use as quick-review before interviews.

## GRPO (Group Relative Policy Optimization)

**Motivation**: PPO needs a Critic network (same size as policy). For 671B models, that's infeasible. GRPO drops the Critic entirely — uses in-group statistics instead.

### Core Formula Chain (4 steps)

```
Step 1: Sample G responses per prompt
  {y₁, ..., y_G} ~ π_θ_old(·|x), get rewards r₁...r_G

Step 2: Group-normalized advantage (replaces Critic)
  A_i = (r_i - μ_group) / σ_group

Step 3: Importance sampling ratio
  ρ_i = π_θ(y_i|x) / π_θ_old(y_i|x)

Step 4: Clipped objective + KL penalty
  L = -(1/G) Σ_i [ min(ρ_i·A_i, clip(ρ_i, 1-ε, 1+ε)·A_i) - β·D_KL(π_θ || π_ref) ]
```

### KL Estimator (k3, Schulman)

```
D_KL ≈ exp(log π_ref - log π_θ) - (log π_ref - log π_θ) - 1
```

Properties: always non-negative, gradient-unbiased.

### Hyperparameters
- ε = 0.2 (clip range, same as PPO)
- β = 0.001~0.01 (KL penalty strength)
- G = 4~16 (group size)

### Interview Narrative
> "GRPO solves PPO's dual-network problem for large models. Instead of training a Critic, it samples G responses per prompt and uses Z-score normalization of in-group rewards as the advantage signal. The update formula is identical to PPO's clipped surrogate, plus a KL penalty estimated via the k3 estimator."

---

## SDAR — Self-Distilled Agentic RL

### Problem: RL reward is trajectory-level (sparse)
Agent takes 10+ steps, only final outcome is rewarded. Intermediate steps get no signal.

### OPSD (On-Policy Self-Distillation) — the precursor
- Teacher branch = **same model π_θ** + privileged context c⁺
- Student = π_θ without c⁺
- Token-level supervision: Δ_t = log π_T(y_t|c⁺) - log π_θ(y_t|no c⁺)

### Why OPSD fails on multi-turn agents
1. **Multi-turn instability**: Student drifts → teacher signals become unreliable → KL explodes
2. **Asymmetric trust**: Teacher rejection (Δ_t < 0) may be from bad skill retrieval, not bad action

### SDAR's fix: Sigmoid-gated auxiliary loss

```
L = L_GRPO + λ·L_SDAR

L_SDAR = Σ_t g_t · (log π_T(y_t|c⁺) - log π_θ(y_t))

g_t = σ(β·Δ_t)  ← sigmoid gate, detached
  Δ_t > 0 → g_t ≈ 1 (strong distillation)
  Δ_t < 0 → g_t → 0 (soft attenuation)
```

### Key insight: Teacher is NOT a separate model
Teacher = π_θ(x, c⁺, y_<t), same weights, just extra privileged context.
Privileged context c⁺ = retrieved skills (sub-goal decompositions, action templates), reference answers, or other training-only info.

### Results (Qwen2.5/3)
- ALFWorld: +9.4%, Search-QA: +7.0%, WebShop: +10.2%
- Standalone OPSD collapses (near-zero on Search-QA)
- Naive GRPO+OPSD degrades severely (32.0 vs 46.1 on Qwen3-1.7B)

### MAPGD connection (interview talking point)
> "MAPGD's beam search over prompt edit paths is test-time optimization. SDAR's teacher branch distills search into the policy — the teacher shows 'what I'd do if I knew the answer' via privileged context, and the sigmoid gate selectively trusts that signal. Both address the same fundamental problem: multiple signal sources with asymmetric reliability."
