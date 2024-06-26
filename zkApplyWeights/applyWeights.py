import subprocess
import json
import sys
import numpy as np
import math
import os

# dot_product = np.dot(matrix1, matrix2)
# result = dot_product + bias_b
# print(result)

def get_matrix_dimensions(matrix):
    rows = len(matrix)
    if rows > 0:
        columns = len(matrix[0])
    else:
        columns = 0
    # columns = len(matrix[0]) if rows > 0 else 0
    return rows, columns

def removeNgv(mat):
    mat[mat < 0] = 0
    return mat

def zkApplyWeights(matrix1,matrix2,bias_b, dir_path = ''):

    curr_path = dir_path + '/zkApplyWeights'
    os.chdir(curr_path)

    
    matrix1 = matrix1.astype(np.int64)
    matrix2 = matrix2.astype(np.int64)
    bias_b = bias_b.astype(np.int64)
    
    # max1 = np.maximum(matrix1)
    # max2 = np.maximum(matrix2)

    # matrix1 //= max1
    # matrix2 //= max2

    # matrix1 = matrix1 * math.pow(10,4)
    # matrix2 = matrix2 * math.pow(10,4)
    
    rows1, columns1 = get_matrix_dimensions(matrix1)
    rows2, columns2 = get_matrix_dimensions(matrix2)
        
    with open('size.zok', 'w') as f:
        f.write('const u32 M1 = {};\n'.format(int(rows1)))
        f.write('const u32 N1 = {};\n'.format(int(columns1)))
        f.write('const u32 M2 = {};\n'.format(int(rows2)))
        f.write('const u32 N2 = {};\n'.format(int(columns2)))
        f.write('const u32 bc = {};\n'.format(int(len(bias_b))))
        
    # matrix_1 = list(map(lambda row: [str(int(element*math.pow(10,8))) for element in row], matrix1))
    # matrix_2 = list(map(lambda row: [str(int(element*math.pow(10,8))) for element in row], matrix2))
    

    removeNgv(matrix1)
    removeNgv(matrix2)
    removeNgv(bias_b)
    
    dot_product = np.dot(matrix1, matrix2)
    bias_b = bias_b.reshape(-1, 1)
    print(dot_product.shape, bias_b.shape)
    result = dot_product + bias_b
    
    print(result)

    # bias = bias_b[0] * math.pow(10, 4)
    bias = bias_b.astype(int).astype(str).tolist()

    # bias = [str(int(item) * math.pow(10,4)) for item in bias_b[0]]  # Convert the first element of bias_b to string and store in a list
    


    # result = list(map(lambda row: [str(element*math.pow(10,8)) for element in row], result))
    
    with open('input.json', 'w') as f:
        json.dump([matrix1.astype(np.int64).astype(str).tolist(), matrix2.astype(np.int64).astype(str).tolist(), bias, result.astype(np.int64).astype(str).tolist()], f)

    # print("Result of dot product of matrices with bias:")

    subprocess.run(["zokrates", "compile", "-i", "applyWeights.zok"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin","--verbose"], stdout=sys.stdout)
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])

    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)
        
    os.chdir(dir_path)
        
    return result, proof
    

# subprocess.run(["zokrates", "verify"])
# matrix1 = np.array([["1",  "2",  "-33"]], dtype=int)
# matrix2 = np.array([["7",  "8"], ["9",  "10"], ["11",  "-12"]], dtype=int)
# bias_b = np.array(["1", "3"], dtype=int)
