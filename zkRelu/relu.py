import subprocess 
import json
import os
import numpy as np
import math
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils.removeNegatives import removeNegatives
from utils.convert_3D_To_1D import convert_3d_to_1d

def relu(arr):
  return np.maximum(0, arr)

def zkRelu(arguments, dir_path=''):

    witness = []
    labels = []
    data = []

    # print(arguments)

    arr = relu(arguments)

    moded_arr = convert_3d_to_1d(arr)
    modified_arr, positive_min = removeNegatives(moded_arr)
    mod_arr = [item for item in modified_arr]
    str_mod_arr = [str(item) for item in mod_arr]
    sys.path.pop()

    curr_path = dir_path + '/zkRelu'
    os.chdir(curr_path)


    with open('size.zok', 'w') as f:
        f.write('const u32 size = {};\n'.format(int(len(modified_arr))))

    with open('input.json', 'w') as f:
        json.dump([str_mod_arr,str(int(positive_min))], f)

    subprocess.run(["zokrates", "compile", "-i", "relu.zok"])
    subprocess.run(["zokrates", "setup", "--proving-scheme", "gm17"])
    subprocess.run(["powershell.exe", "Get-Content input.json |", "zokrates", "compute-witness", "--abi", "--stdin"], stdout=sys.stdout)
        
    subprocess.run(["zokrates", "generate-proof", "--proving-scheme", "gm17"])
    with open("proof.json", 'r') as proof_file:
        proof = json.load(proof_file)


    os.chdir(dir_path)

    return proof, arr

