import sys
import pandas as pd
import numpy as np
def growth_factor(pred,total):
    temp_pred ,temp_total = 0 , 0
    for i in range(len(total)):
        temp_total += total[i]
        temp_pred += pred[i]
    return temp_pred / temp_total
def Uniform(mat,growth,a):
    Oi_horizon = [0.0 for i in range(len(mat))]
    total = [0.0 for i in range(len(mat))]
    growth_factor = 0.0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            total[i] += mat[i][j]
        Oi_horizon[i] = total[i] * growth[i]

    generate_Row(mat, total,growth, Oi_horizon)
    calculate_new_matrix(mat,growth,Oi_horizon)
def calculate_new_matrix(mat, growth,Oi_horizon):
    previous_growth = np.array(growth)
    iteration_count = 0
    a = len(growth)

    # Loop until convergence criteria is met
    while True:
        iteration_count += 1
        
        # Initialize the new matrix
        new_mat = np.zeros_like(mat, dtype=float)
        # Update the new matrix based on the growth factors
        if iteration_count % 2:
            for i in range(a):
                for j in range(a):
                    new_mat[i][j] = mat[i][j] * previous_growth[i]
            total_column = np.sum(new_mat, axis=0)

        # Normalize total_row with pred_row and total_column with pred_column
        
            GF_Revised = Oi_horizon / total_column
            # Check for convergence
            if all(0.97 <= value <= 1.03 for value in GF_Revised):
                print("Convergence achieved after iterations:", iteration_count)
                break

            # Generate the DataFrame and prepare for the next iteration
            generate_Column(new_mat, total_column, Oi_horizon,GF_Revised)

        else:
            for j in range(a):
                for i in range(a):
                    new_mat[i][j] = mat[i][j] * previous_growth[j]
            total_row = np.sum(new_mat, axis=1)

        # Normalize total_row with pred_row and total_column with pred_column
        
            GF_Revised = Oi_horizon / total_row
            # Check for convergence
            if all( value == 1.0 for value in GF_Revised):
                print("Convergence achieved after iterations:", iteration_count)
                break

            # Generate the DataFrame and prepare for the next iteration
            generate_Row(new_mat, total_row, GF_Revised,Oi_horizon)
        previous_growth = GF_Revised.copy()
        mat = new_mat  # Update mat for next iteration

    return new_mat, total_row, total_column, growth

def generate_Row(new_mat, total_row, GF_Revised_row, pred_row):
    # Prepare the data dictionary for DataFrame creation
    data = {
        '1': [new_mat[i][0] for i in range(len(new_mat))],
        '2': [new_mat[i][1] for i in range(len(new_mat))],
        '3': [new_mat[i][2] for i in range(len(new_mat))],
        '4': [new_mat[i][3] for i in range(len(new_mat))],
        'Oi_current': total_row,
        'Oi_Horizon': pred_row,
        'Growth': GF_Revised_row
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Set the index for the DataFrame
    df.index = [1, 2, 3,4,]

    # Round all numeric columns to 3 decimal places
    df = df.round(3)

    # Display the DataFrame
    print("\nTij_012:")
    print(df)


def generate_Column(new_mat, total_column, Oi_horizon, GF_Revised):
    # Prepare the data dictionary for DataFrame creation
    data = {
        '1': [new_mat[i][0] for i in range(len(new_mat))],
        '2': [new_mat[i][1] for i in range(len(new_mat))],
        '3': [new_mat[i][2] for i in range(len(new_mat))],
        '4': [new_mat[i][3] for i in range(len(new_mat))],
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Replace None with 0 for total_column
    total_col = [x if x is not None else 0 for x in total_column]

    # Add additional rows for totals and growth factors
    df.loc['Dj_Current'] = [total_column[i] if i < len(total_column) else "" for i in range(df.shape[1])]
    df.loc['Dj_horizon'] = [Oi_horizon[i] if i < len(Oi_horizon) else "" for i in range(df.shape[1])]
    df.loc['G.F'] = [GF_Revised[i] if i < len(GF_Revised) else "" for i in range(df.shape[1])]

    # Set the index for the DataFrame
    df.index = [1, 2, 3,4, 'Dj_current', 'Dj_Horizon', 'GF']

    # Round all numeric columns to 3 decimal places
    df = df.round(3)

    # Display the DataFrame
    print("\nTij_012:")
    print(df)



file_path = 'Assignment_2.xlsx'
print("You have entered Question 5")
df = pd.read_excel(file_path, sheet_name='Furness',header=None)
print(df)
a = int(input("Enter the size of matrix:"))
Tij_012 = df.iloc[:a, :a].values.tolist()

print(Tij_012)
Oih_012 = df.values[:a,a+1].tolist()
print(Oih_012)
Uniform(Tij_012,Oih_012,a)
    