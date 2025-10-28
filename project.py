import pandas as pd
import numpy as np
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpBinary

def extract(cvs_path): #create a frame for any data
    print("Extracting data from CVS")
    df = pd.read_csv("market_pipe_thickness_loss_dataset.csv")
    print(f"Loaded {len(df)} rows.")
    #print(df.head(10))
    return df
    

def transform(df): #clean the data
    print("Transforming data...")
    df = df.drop_duplicates() #avoid analyzing the same type of material
    df = df.dropna() #remove N/A value
    df = df.reset_index(drop=True)
    return df

def calculated_longevity(df):

    df['Remaining_Thickness_mm'] = df['Thickness_mm'] - df['Thickness_Loss_mm']
    df['Loss_Per_Year_mm'] = df['Thickness_Loss_mm'] / df['Time_Years']
    df['Estimated_Longevity_Years'] = df['Remaining_Thickness_mm'] / df['Loss_Per_Year_mm']
    df = df.reset_index(drop=True)
    print("First 10 rows of Estimated_Longevity_Years:")
    print("\nSample of longevity calculations:")
    print(df[['Material', 'Grade', 'Estimated_Longevity_Years']].sort_values(by='Estimated_Longevity_Years', ascending=False).head(5))
    
    return df
#Use LP to find the optimal type of materials that last the longest and still sastified the requirements


def optimize_materials(df):
    
    prob = LpProblem('select_Best_Materials', LpMaximize)

    #Variables
    x = {i: LpVariable(f"x_{i}", cat=LpBinary) for i in df.index}
    #Objective: 
    prob += lpSum(x[i] * df.loc[i, 'Estimated_Longevity_Years'] for i in df.index)
    #constraint    
    #prob += lpSum(x[i] * df.loc[i, 'Max_Pressure_psi'] for i in df.index) >= 1000, "Max_pressure_psi"
    #prob += lpSum(x[i] * df.loc[i, 'Temperature_C'] for i in df.index) >= 100, "Temperature_C"

    for i in df.index:
        if df.loc[i, 'Max_Pressure_psi'] < 1000 or df.loc[i, 'Temperature_C'] < 120:
            # Prevent selection by forcing x[i] = 0
            prob += x[i] == 0
            
    prob.solve()
    
    selected = [i for i in df.index if x[i].value() == 1]

    print("Selected materials:")
    print(df.loc[selected, ['Material', 'Grade','Max_Pressure_psi','Temperature_C', 'Estimated_Longevity_Years']])
    

    return(df)


def add_cost(df):
    

    df["cost"] = np.random.randint(2000,5000, size= len(df))
                                   
    df.to_csv("market_pipe_thickness_loss_dataset_with_cost.csv", index=False)

    print(df.head())
    return df

def dp_material_selection(df, budget = 18000):
    df = pd.read_csv("market_pipe_thickness_loss_dataset_with_cost.csv")  #update new cvs
    df = transform(df)    #clean new file   
    n = len(df)

    #create a dp table
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]

    for i in range (1,n+1):
        cost = df.loc[i-1, 'cost']
        longevity = df.loc[i-1, 'Estimated_Longevity_Years']

        for w in range (1, budget +1):  
            if cost <= w:
                dp[i][w] = max((dp[i-1][w]), (dp[i-1][w-cost] + longevity))
            else:
                dp[i][w] = dp[i-1][w]
    print(f"Max Longevity within budget {budget}: {dp[n][budget]:.2f}")   

#USAGE
csv_path = "market_pipe_thickness_loss_dataset.csv"
df = extract(csv_path)
df = transform(df)
df = calculated_longevity(df)
df = optimize_materials(df)
df = add_cost(df)
df = dp_material_selection(df, budget = 18000)



#USING DYNAMIC PROGRAMMING
