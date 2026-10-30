# LCS Text Similarity Checker — Dynamic Programming

A GUI-based web application that computes the **Longest Common Subsequence (LCS)** of two strings using **Dynamic Programming**, with step-by-step visualization of the DP table.

> **Course:** Design and Analysis of Algorithms — Assignment 2

## 🚀 How to Run

### Option 1: Just open the file
Double-click `lcs_text_similarity.html` — it opens directly in your browser. No setup needed.

### Option 2: Local server
```bash

python -m http.server 8080
```
Then open: **http://localhost:8080/lcs_text_similarity.html**


## ✨ Features

| Button | Description |
|--------|-------------|
| ▶ Compute LCS | Instantly computes and fills the DP table |
| ⏩ Animate | Step-by-step animation with speed control |
| ⏭ Step | Advance one cell at a time (manual) |
| 🗑 Clear | Reset all inputs and results |

- 🟩 **Green cells** → Character match
- 🟥 **Pink cells** → No match
- 🟨 **Gold cells** → Backtrack path (actual LCS)
- Matching characters highlighted in both input strings
- Similarity percentage displayed

## 📊 Algorithm & Complexity

**Recurrence:**
- `dp[i][j] = dp[i-1][j-1] + 1` if characters match
- `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` otherwise

| Metric | Complexity |
|--------|-----------|
| Time | O(m × n) |
| Space | O(m × n) |
| Backtrack | O(m + n) |

## 🧪 Test Cases

| Text 1 | Text 2 | LCS | Length | Similarity |
|--------|--------|-----|--------|------------|
| ALGORITHM | ALTRUISTIC | ALRITC | 6 | 60.0% |
| ABCDEF | ABCDEF | ABCDEF | 6 | 100.0% |
| ABC | XYZ | (empty) | 0 | 0.0% |
| A | A | A | 1 | 100.0% |
| ABCBDAB | BDCAB | BCAB | 4 | 57.1% |

## 🛠 Tech Stack

- **HTML5 + CSS3 + JavaScript** (single file, no dependencies)
