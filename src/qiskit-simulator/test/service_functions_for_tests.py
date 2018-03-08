#!/usr/bin/python3

'''
This file contains auciliary functions, to be called from test scripts.
Its purpose is to avoid duplication.
'''

import os
import argparse
import random
import numpy
import qiskit.backends._qiskit_cpp_simulator as qsim


def default_executable():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../out/qiskit_simulator'))


def parse(description):

    parser = argparse.ArgumentParser(description = description,
                                     formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--seed', type = int, dest = 'seed',
                        help = 'random seed')

    parser.add_argument('--executable', type = str, dest = 'executable',
                        help = 'qiskit simulator executable',
                        default = default_executable())
                        
    args = parser.parse_known_args()[0]

    if args.seed is not None:
        random.seed(a = args.seed)
        numpy.random.seed(args.seed)

    return parser


def run_simulator(qobj, executable):
    
    result = qsim.run(qobj, executable = executable)

    if result['success'] == True:
        print('Successful execution. Execution time: ' + str(result['time_taken']))
    else:
        print('Execution failed. Details:')
        print(result)

    return result
