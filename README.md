# Oil and Gas Material Longevity Optimization

## Project Overview
This project analyzes material performance data in the oil and gas industry to **estimate pipe longevity**, **filter optimal materials**, and **optimize cost-efficiency** using a combination of **data analysis**, **linear programming (LP)**, and **dynamic programming (DP)**.

It is designed to help engineers or data scientists **select materials that maximize pipeline lifespan** under given environmental and operational constraints.

---

## Features
1. **Data Extraction & Cleaning**
   - Loads and processes raw material datasets
   - Removes duplicates and missing values for clean analysis.

2. **Longevity Calculation**
   - Computes:
     - Remaining pipe thickness
     - Annual thickness loss
     - Estimated total longevity (years)
   - Displays top-performing materials.

3. **Linear Programming Optimization**
   - Uses `PuLP` to select materials that **last the longest** while meeting required **pressure** and **temperature** thresholds.
   - Binary decision variables determine whether a material should be selected.

4. **Dynamic Programming for Budget Optimization**
   - Adds random cost values for each material.
   - Solves a **cost-longevity tradeoff** problem under a defined budget (similar to a Knapsack problem).
   - Determines the **maximum total longevity achievable within the budget**.



## Key Libraries
- `pandas` – Data manipulation and cleaning  
- `numpy` – Numerical operations  
- `pulp` – Linear optimization (LP model)


## Expected Output

- Displays top 5 materials with highest estimated longevity.
- Prints selected materials that satisfy engineering constraints.
- Shows the maximum achievable longevity within the given budget.

## Future improvement
- Build a web dashboard for interactive material analysis.

## Author
My Phan 
Passionate about applying AI and optimization to real-world industrial problems.