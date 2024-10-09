import sys
import pandas as pd
import numpy as np
def growth_factor(pred,total):
    temp_pred ,temp_total = 0 , 0
    for i in range(len(total)):
        temp_total += total[i]
        temp_pred += pred[i]
    return temp_pred / temp_total

def Detroit(mat, growth, a):
    total_row = [0.0 for _ in range(a)]
    total_col = [0.0 for _ in range(a)]
    pred_row = [0.0 for _ in range(a)]
    pred_col = [0.0 for _ in range(a)]
    # Calculate total_row and total_col
    for i in range(a):
        for j in range(a):
            total_row[i] += mat[i][j]
            total_col[j] += mat[i][j]  # Corrected to mat[i][j] for column sums

    # Calculate pred_row and pred_col based on growth factors
    for i in range(a):
        pred_row[i] = total_row[i] * growth[i]
        pred_col[i] = total_col[i] * growth[i]

    # Generate initial DataFrame
    generate2(mat, total_row, growth, pred_row, total_col, pred_col)
    # Start calculating the new matrix and updating growth factors
    calculate_new_matrix(mat, growth, pred_row, pred_col)

def calculate_new_matrix(mat, growth, pred_row, pred_column):
    previous_growth = np.array(growth)
    iteration_count = 0
    a = len(growth)

    # Loop until convergence criteria is met
    while True:
        iteration_count += 1
        
        # Initialize the new matrix
        new_mat = np.zeros_like(mat, dtype=float)
        total_old_row = np.sum(mat,axis=1)
        f_value = growth_factor(pred_row,np.sum(mat,axis=1))
        # Update the new matrix based on the growth factors
        for i in range(a):
            for j in range(a):
                new_mat[i][j] = mat[i][j] * (previous_growth[i] * previous_growth[j]) / f_value

        # Calculate total_row and total_column
        total_row = np.sum(new_mat, axis=1)
        total_column = np.sum(new_mat, axis=0)

        # Normalize total_row with pred_row and total_column with pred_column
        GF_Revised_row = pred_row / total_row
        GF_Revised_col = pred_column / total_column
        print(f_value)
        # Check for convergence
        if all(0.97 <= value <= 1.03 for value in GF_Revised_row):
            print("Convergence achieved after iterations:", iteration_count)
            break

        # Generate the DataFrame and prepare for the next iteration
        generate2(new_mat, total_row, GF_Revised_row, pred_row, total_column, pred_column)
        previous_growth = GF_Revised_row.copy()
        mat = new_mat  # Update mat for next iteration

    return new_mat, total_row, total_column, growth

def generate2(new_mat, total_row, GF_Revised_row, pred_row, total_column, pred_column):
    # Prepare the data dictionary for DataFrame creation
    data = {
        '1': [new_mat[i][0] for i in range(len(new_mat))],
        '2': [new_mat[i][1] for i in range(len(new_mat))],
        '3': [new_mat[i][2] for i in range(len(new_mat))],
        '4': [new_mat[i][3] for i in range(len(new_mat))],
        'Oi_base': total_row,
        'G-f': GF_Revised_row,
        'Oi_horizon': pred_row
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Replace None with 0 for total_column
    total_col = [x if x is not None else 0 for x in total_column]

    # Add additional rows for totals and growth factors
    df.loc['Dj_base'] = [total_column[i] if i < len(total_column) else "" for i in range(df.shape[1])]
    df.loc['G.F'] = [GF_Revised_row[i] if i < len(GF_Revised_row) else "" for i in range(df.shape[1])]
    df.loc['Dj_horizon'] = [pred_column[i] if i < len(pred_column) else "" for i in range(df.shape[1])]

    # Set the index for the DataFrame
    df.index = [1, 2, 3,4, 'Dj_base', 'G.F', 'Dj_horizon']

    # Round all numeric columns to 3 decimal places
    df = df.round(3)

    # Display the DataFrame
    print("\nTij_012:")
    print(df)



file_path = 'Assignment_2.xlsx'
print("You have entered Question 3")
df = pd.read_excel(file_path, sheet_name='Detroit',header=None)
print(df)
a = int(input("Enter the size of matrix:"))
Tij_012 = df.iloc[:a, :a].values.tolist()

print(Tij_012)
Oih_012 = df.values[:a,a+1].tolist()
print(Oih_012)
Detroit(Tij_012,Oih_012,a)
    