import numpy as np
import pandas as pd

def topsis(input_file_name, weights, impacts, output_file_name):
    # Reading the dataset
    my_data_set = pd.read_csv(str(input_file_name))
    # Fetching weights and impacts and converting them into a list of numbers.
    weights = [float(w) for w in weights.split(',')]
    impacts = impacts.split(',')
    if not set(impacts).issubset({'+', '-'}):
        raise ValueError("Impacts must be either + or -.")
    # Checking if the weights and impacts are equal to number of columns - 1 as one column is for FundName
    assert len(weights) == len(impacts) == len(my_data_set.columns) - 1
    # Atleast 3 columns must be there as a condition mentioned in the question
    if len(my_data_set.columns) < 3:
        raise ValueError("Input file must contain three or more columns.")
    if not my_data_set.iloc[:, 1:].apply(lambda col: pd.to_numeric(col, errors='coerce').notna().all()).all():
        raise ValueError("Columns from 2nd to last must contain numeric values only.")
    # Creating normalized matrix
    data_values = my_data_set.iloc[:, 1:].values
    normalized_matrix = np.zeros_like(data_values, dtype=float) 
    column_norms = np.linalg.norm(data_values, axis=0)
    for i in range(data_values.shape[0]):  
        for j in range(data_values.shape[1]):  
            normalized_matrix[i, j] = data_values[i, j] / column_norms[j]
    # Creating the weighted matrix
    weighted_matrix = normalized_matrix * weights
    # Finding the ideal best and worst value
    ideal_best = np.zeros(weighted_matrix.shape[1])
    ideal_worst = np.zeros(weighted_matrix.shape[1])
    for j in range(weighted_matrix.shape[1]):
        if impacts[j] == '+':
            ideal_best[j] = np.max(weighted_matrix[:, j])
            ideal_worst[j] = np.min(weighted_matrix[:, j])
        elif impacts[j] == '-':
            ideal_best[j] = np.min(weighted_matrix[:, j])
            ideal_worst[j] = np.max(weighted_matrix[:, j])
        else:
            raise ValueError("Impacts must be either + or -.")
    # Finding the euclidean distance
    best_dist = np.linalg.norm(weighted_matrix - ideal_best, axis=1)
    worst_dist = np.linalg.norm(weighted_matrix - ideal_worst, axis=1)
    # Calculating the topsis score
    topsis_score = worst_dist / (best_dist + worst_dist)
    my_data_set['TOPSIS Score'] = topsis_score
    my_data_set['Rank'] = my_data_set['TOPSIS Score'].rank(ascending=False)
    # my_data_set.to_csv(output_file_name, index=False)
    # print("TOPSIS Score and Rank Updated and saved to the output file = ",output_file_name)
    return my_data_set