import sys
import pandas as pd
import numpy as np
def growth_factor(pred,total):  ## to calculate growth factor (Oi_horizon / Oi_current) ==> horizon is temp_pred nd Oi_current is temp_total
    temp_pred ,temp_total = 0 , 0
    for i in range(len(total)):
        temp_total += total[i]
        temp_pred += pred[i]
    return temp_pred / temp_total
def Uniform(mat,pred,a): 
    total = [0.0 for i in range(len(mat))] #total row sum
    uniform_growth_factor = 0.0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            total[i] += mat[i][j]
    uniform_growth_factor = growth_factor(pred,total)
    for i in range(len(mat)):
        temp = 0
        for j in range(len(mat[0])):
            mat[i][j] *= uniform_growth_factor # for calculating new matrix for multiplied growth factors
            temp += mat[i][j]
        total[i] = temp
    data = {
    '1': [mat[i][0] for i in range(len(mat))] ,
    '2': [mat[i][1] for i in range(len(mat))] ,
    '3': [mat[i][2] for i in range(len(mat))] ,
    'Σ': total,
    }

# Create DataFrame
    df = pd.DataFrame(data)

# Set the index for the DataFrame to include serial numbers
    df.index = [1, 2, 3,]

# Display the DataFrame as a table
    print("\nTij_012:")
    print(df)



file_path = 'Assignment_2.xlsx'
print("You have entered Question 1",)
df = pd.read_excel(file_path, sheet_name='Uniform',header=None) #taking excel data 
print(df)
a = int(input("Enter the size of matrix:"))
Tij_012 = df.iloc[:a, :a].values.tolist() #GIven Matrix

print(Tij_012)
Oih_012 = df.values[:a,a+1].tolist() #Given Oi_horizon
print(Oih_012)
Uniform(Tij_012,Oih_012,a)

    