import pandas as pd
import numpy as np
import argparse
## Revision: 0
# Dynamically acquire column names: all_columns = df.columns.tolist() obtains all column headers.
# Adjust data range: df.loc[1:, all_columns] loads data starting from the second row (index=1) for all columns.
# Process empty columns: dropna(axis=1, how='all') removes entirely empty columns to ensure data validity.
def read_data(data_path):
    # Excel ingestion: Read source data
    df = pd.read_excel(data_path, sheet_name="Sheet1")
    # Data slicing: Load columns from row 2 (index=1) onward
    df = df.iloc[0:,1:].dropna(axis=1, how='all').dropna(axis=0, how='all')# 移除全空的列
    print(f"The number of data rows read: {len(df)}")
    # Array conversion: Transform to NumPy ndarray
    arr_data = df.values
    return arr_data

def generate_x0(num_indices):
    x0s = []
    # Combination generation: Recursively produce all binary (0/1) permutations
    def generate_combinations(current, remaining):
        if remaining == 0:
            x0s.append(current.copy())
            return
        for value in (0, 1):
            current.append(value)
            generate_combinations(current, remaining - 1)
            current.pop()

    generate_combinations([], num_indices)
    return np.array(x0s).reshape(-1, num_indices)

#   the absolute difference
def diff_x0_x(x0,x):
    num = x.shape[0]
    diff = np.abs(x0-x)
    return diff
#   the correlation coefficient
def get_coeff(diff,r):
    min_j = diff.min(axis=0)
    min_i = min_j.min()
    max_j = diff.max(axis=0)
    max_i = max_j.max()
    print(max_i)
    coeff = (min_i + r * max_i) / (diff + r * max_i)
    return coeff
#   the weighted grey relational grades
def get_r(coeff,weight):
    r = np.sum(coeff * weight,axis=1)
    return r
#   Tri-level probabilistic classification:
#   Category_1 (1): values ≤ (mean - 0.5246 * s)
#   Intermediate (0.5): values between (mean - 0.5246 * s) and (mean + 0.5246 * s)
#   Category_2 (0): values ≥ (mean + 0.5246 * s)
def split(r):
    mean = np.mean(r)
    s = np.std(r)
    left = mean - 0.5246 * s
    right = mean + 0.5246 * s
    r[r<left] = 0
    r[r>right] = 2
    return r
# Calculate prediction accuracy
def get_acc(rs,targets):
    rs = rs.tolist()
    targets = targets.tolist()
    correct = 0
    wrong = 0
    mid = 0
    for r,t in zip(rs,targets):
        if r == t:
            correct += 1
        elif r != t and (r != 0 or r != 2) :
            mid += 1
        else:
            wrong += 1
    acc = (1 * correct + 0.5 * mid + 0 * wrong) / len(rs)
    return acc

#def main(data_path, save_path, weight_path, num_indices, r):
def main(data_path, save_path, weight_path, num_indices, r, Category_1, Category_2):
    # Load weight vector from file
    weight = np.loadtxt(weight_path)
    #target = np.array([2] * 78 + [0] * 78)
    target = np.array([2] * Category_1 + [0] * Category_2)
    arr_data = read_data(data_path)
    # Validate row count equals sum of Category_1 and Category_2 samples
    total_samples = Category_1 + Category_2
    if arr_data.shape[0] != total_samples:
        raise ValueError(f"Data_sample_count ({arr_data.shape[0]}) ≠ Category_1 ({Category_1}) + Category_2 ({Category_2})")

    x0s = generate_x0(num_indices)
    accs = []
    for x0 in x0s:
        diff = diff_x0_x(x0, arr_data)
        coeff = get_coeff(diff, r)
        r_values = get_r(coeff, weight)
        r_values = split(r_values)
        acc = get_acc(r_values, target)
        accs.append(acc)
    with open(save_path, 'w') as f:
        for index, acc in enumerate(accs):
            f.write(str(x0s[index]) + ':' + str(acc) + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gray Relational Analysis Automation')
    parser.add_argument('data_path', type=str, help='Path to the input data file')
    parser.add_argument('save_path', type=str, help='Path to save the results')
    parser.add_argument('weight_path', type=str, help='Path to the weight file')
    parser.add_argument('--num_indices', type=int, default=13, help='Number of indices for generate_x0 function')
    parser.add_argument('--r', type=float, default=0.5, help='Value of r for get_coeff function')
    parser.add_argument('--Category_1', type=int, required=True, help='Number of Category_1 samples')
    parser.add_argument('--Category_2', type=int, required=True, help='Number of Category_2 samples')
    args = parser.parse_args()

    main(args.data_path, args.save_path, args.weight_path, args.num_indices, args.r, args.Category_1, args.Category_2)
