# 📚 AWS Certified Machine Learning - Associate: Study Guide
## Module 1.7: Train / Validation / Test & Data Splitting Strategies

Mastering how to partition datasets is a foundational requirement for both real-world machine learning engineering and passing the AWS Certified Machine Learning – Associate exam. Improper data splitting leads to severe issues like **data leakage**, **overfitting**, and **production failure**.

---

## 1. The Three Pillars of Dataset Partitioning

To build robust machine learning models, your dataset must be partitioned into three independent subsets:

1. **Training Set ($70\\% - 80\\%$):** 
   - **Purpose:** Used by the algorithm to learn patterns, adjust weights, and fit model parameters.
2. **Validation Set ($10\\% - 15\\%$):** 
   - **Purpose:** Used during development to **tune hyperparameters** (e.g., learning rate, tree depth, number of epochs) and select the best-performing model architecture. The model never directly learns from these samples.
3. **Test Set ($10\\% - 15\\%$):** 
   - **Purpose:** An isolated dataset kept completely unseen during training and tuning. It provides an **unbiased evaluation** of how the model will perform in the real world.
   - ⚠️ *Rule of Thumb:* The test set should only be evaluated **once** at the very end of your experimentation pipeline.

---

## 2. Core Splitting Strategies & Sampling Techniques

### Random Split
* **Definition:** Randomly shuffles and splits the dataset into subsets according to defined ratios (e.g., 80/20).
* **When to use:** When observations are **I.I.D. (Independent and Identically Distributed)** — meaning row $N$ has no spatial or temporal correlation with row $N+1$.

### Shuffle
* **Definition:** Reordering the rows of a dataset randomly.
* **Why it matters:** Eliminates ordering biases (e.g., if a dataset was originally sorted by class labels or signup dates).
* **Critical Warning:** **Never** shuffle time-series or sequential data.

### Stratification (Stratified Split / K-Fold)
* **Definition:** Ensures that the proportion of target classes in each split (train, validation, test) mirrors the exact distribution of the original dataset.
* **When to use:** Essential for **imbalanced classification problems** (e.g., fraud detection, anomaly detection where positive cases make up $<1\\%$ of data) to prevent splits from missing minority classes entirely.

### K-Fold Cross-Validation
* **Definition:** The training dataset is split into $K$ equal parts (folds). The model is trained $K$ times, using $K-1$ folds for training and $1$ fold for validation in rotation. The final performance metric is averaged across all rounds.
* **Why use it:** Maximizes data utilization when working with small datasets without risking biased validation metrics.

---

## 3. Critical Exam Concept: When NOT to Use Random Split

### The Danger of Temporal Data Leakage
When working with time-dependent data (e.g., **retail sales forecasts, energy consumption, stock prices, web traffic logs**):
* **The Mistake:** Applying a random shuffle or standard random split.
* **The Consequence:** Future data (e.g., December sales) ends up in the training set, while past data (e.g., January sales) ends up in the test set. The model "learns the future to predict the past."
* **Production Failure:** High accuracy in laboratory tests, but catastrophic failure in production because the model cannot predict unseen future events.

### Proper Approach for Time-Series
1. **Temporal Split (Chronological):** Train on historical past data $\rightarrow$ Validate/Test on future data.
2. **Rolling / Expanding Window Cross-Validation:** Incrementally expanding the training window over time. *(Note: AWS native services like Amazon Forecast handle chronological splitting automatically).*

---

## 4. Quick Reference Matrix for the AWS Exam

| Scenario / Data Type | Recommended Strategy | Key Risk / Consideration |
| :--- | :--- | :--- |
| **Independent tabular records** | Random Split (+ Shuffle if needed) | Check for sorting bias in source files. |
| **Imbalanced classification** | Stratified Train-Test / Stratified K-Fold | Prevents empty minority classes in test/validation sets. |
| **Small datasets / limited samples** | K-Fold Cross-Validation | Maximizes data efficiency for hyperparameter tuning. |
| **Time-series / Sales / Logs** | Chronological / Temporal Split | **Never** use random split; prevents temporal data leakage. |

---

*Prepared for the AWS Certified Machine Learning – Associate Certification Journey.*