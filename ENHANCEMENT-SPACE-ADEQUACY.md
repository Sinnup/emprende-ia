# Enhancement: Space Adequacy Factor for Viability Score

**Type**: Optional MVP Enhancement  
**Complexity**: Simple (5 minutes)  
**Impact**: Better viability scoring for space-type mismatches  
**Testing**: 2 minutes  

---

## 🎯 What This Does

**Current**: Space only affects COST (higher rent for bigger space)  
**After Enhancement**: Space affects VIABILITY SCORE

**Example**:
- 30m² restaurant (too small) → Budget score penalized 20%
- 500m² restaurant (too large) → Budget score penalized 30%
- 100m² restaurant (optimal) → No penalty

---

## 📝 Exact Code Changes

### File: `app.py`

**Location**: Line ~210-220 (inside `calculate()` function)

**Current Code**:
```python
if budget >= fy:          bs, bst = m["budget"]["scoring"]["sufficient"],   "Suficiente"
elif budget >= fy * 0.8:  bs, bst = m["budget"]["scoring"]["marginal"],     "Marginal"
else:                      bs, bst = m["budget"]["scoring"]["insufficient"], "Insuficiente"
```

**Replace With**:
```python
# Calculate budget score
if budget >= fy:          bs, bst = m["budget"]["scoring"]["sufficient"],   "Suficiente"
elif budget >= fy * 0.8:  bs, bst = m["budget"]["scoring"]["marginal"],     "Marginal"
else:                      bs, bst = m["budget"]["scoring"]["insufficient"], "Insuficiente"

# ENHANCEMENT: Apply space adequacy penalty to budget score
# Penalize if space is too small or too large for business type
space_penalty = 1.0
if sqm < 50:              space_penalty = 0.80   # Too small: -20%
elif sqm > 300:           space_penalty = 0.70   # Too large: -30%

bs = round(bs * space_penalty)  # Apply penalty to budget score
```

---

## 🔍 Detailed Implementation

### Step 1: Locate the Code

In `app.py`, find the `calculate()` function around line 184.

Look for this section (around line 208-212):
```python
if budget >= fy:          bs, bst = m["budget"]["scoring"]["sufficient"],   "Suficiente"
elif budget >= fy * 0.8:  bs, bst = m["budget"]["scoring"]["marginal"],     "Marginal"
else:                      bs, bst = m["budget"]["scoring"]["insufficient"], "Insuficiente"
```

### Step 2: Add After This Section

Right after the budget score calculation, add:

```python
# ENHANCEMENT: Space Adequacy Penalty
# Penalize budget score if space is inadequate for business type
space_penalty = 1.0

# Small space penalty (can't accommodate enough customers/operations)
if sqm < 50:
    space_penalty = 0.80  # 20% penalty for very small spaces
elif sqm < 60:
    space_penalty = 0.85  # 15% penalty for small spaces

# Large space penalty (high overhead costs)
if sqm > 300:
    space_penalty = 0.70  # 30% penalty for very large spaces
elif sqm > 200:
    space_penalty = 0.80  # 20% penalty for large spaces

# Apply penalty to budget score
bs = round(bs * space_penalty)
```

### Step 3: No Other Changes Needed

The rest of the calculation stays the same. The function will:
1. Calculate initial budget score (bs)
2. Apply space penalty (NEW)
3. Continue with competition, location, security, growth, legal factors
4. Return final viability score

---

## 📊 Space Penalty Values

| Space (m²) | Penalty | Effect | Reason |
|------------|---------|--------|--------|
| <50 | -20% | Too small | Can't accommodate operations/customers |
| 50-60 | -15% | Small | Limited capacity |
| 60-200 | 0% | Optimal | No penalty |
| 200-300 | -20% | Large | High overhead costs |
| >300 | -30% | Too large | Unsustainable overhead |

---

## 🧪 Testing the Enhancement

### Test Case 1: Small Space (Too Small)
**Input**: Restaurant, Cuauhtémoc, $500k, **30m²**
**Expected**: Budget score reduced by 20%
**Before**: Budget factor might be 75/100
**After**: Budget factor = 75 × 0.80 = **60/100**

### Test Case 2: Large Space (Optimal)
**Input**: Restaurant, Cuauhtémoc, $500k, **100m²**
**Expected**: No penalty
**Before**: Budget factor = 75/100
**After**: Budget factor = 75 × 1.0 = **75/100** (same)

### Test Case 3: Very Large Space
**Input**: Restaurant, Cuauhtémoc, $500k, **400m²**
**Expected**: Budget score reduced by 30%
**Before**: Budget factor = 75/100
**After**: Budget factor = 75 × 0.70 = **52/100**

---

## 📋 Verification Checklist

After making changes:

1. Open `app.py` in text editor
2. Find the code section mentioned above
3. Add the space penalty code after budget score calculation
4. Save file
5. Run: `streamlit run app.py`
6. Test the 3 cases above
7. Verify scores change as expected
8. ✅ Enhancement complete

---

## 💡 Why This Works

**Current Model**: Budget factor = "Do you have enough capital?"
- Looks at: Total costs for year 1
- Space affects: Rent cost (larger space = higher rent)
- Gap: Doesn't account for whether space is APPROPRIATE

**Enhanced Model**: Budget factor = "Do you have enough capital FOR THIS SPACE?"
- Adds: Space adequacy check
- Logic: Small/large spaces = harder to operate = riskier = lower score
- Result: More realistic viability assessment

---

## 🔄 If Issues Occur

**Issue**: Code won't run / Syntax error
→ Check indentation matches surrounding code
→ Ensure quotes and parentheses are balanced

**Issue**: Score doesn't change
→ Verify space_penalty is being applied to `bs`
→ Check if sqm values are outside penalty ranges (60-200 = no penalty)

**Issue**: Viability score changes too much
→ Adjust penalty percentages (0.80 = 20%, 0.70 = 30%)
→ Use smaller penalties if needed (0.90 = 10%, 0.85 = 15%)

---

## 📈 Impact on Final Score

The space penalty affects **only the Budget Factor** (15% weight):

```
Final Score = (Budget × 0.15) + (Competition × 0.20) + (Location × 0.20) 
            + (Security × 0.15) + (Growth × 0.15) + (Legal × 0.15)

With Space Penalty:
Final Score = (Budget_with_penalty × 0.15) + (other factors × 0.85)
```

**Maximum impact**: 15% of total score (if budget factor is heavily penalized)
**Minimum impact**: 0% (if space is optimal)

---

## ✅ Completion

Once tested and working:

1. Commit changes:
   ```bash
   git add app.py
   git commit -m "enhance: add space adequacy penalty to budget factor"
   ```

2. Run demo video with enhancement active

3. Submit with improved viability scoring

---

**Time to implement**: 5 minutes  
**Time to test**: 2 minutes  
**Total**: 7 minutes  
**Risk level**: Very low (isolated change, easy to revert)  

