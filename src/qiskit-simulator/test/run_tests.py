#!/usr/bin/python3

'''
This script runs all the tests in the test folder of the qiskit simulator.

There are two types of tests: random and static.

Random tests are written in Python.
The script run_tests runs each random test.
If the user specifies a reference executable,
then run_tests runs the random tests with both the main and the reference executables,
and compares their run times.

Static tests are represnted by json files.
run_tests runs the simulator for each json file.
If the user specifies a reference executable,
then run_tests runs the static tests with both the main and the reference executables,
and compares both their outputs and run times.
In the absence of a reference executable, the script compares against a matching ref file, if it exists.

The user can specify alternative executable and/or tests directory.
Run "./run_tests.py --help" for details.

Tests which reside under directories named "help_scripts" are ignored.
'''


import importlib
import os
import argparse
import random
serv = importlib.import_module('src.qiskit-simulator.test.service_functions_for_tests', None)
import subprocess as sp
import time
import difflib
import re


file_types = ['py', 'json']


def collect_test_files(dir_name):

    if dir_name is None:
        files_and_dirs = collect_files_and_dirs(os.path.abspath(os.path.dirname(__file__)))
        files = {'py': [], 'json': []}
    else:
        files_and_dirs = collect_files_and_dirs(dir_name)
        files = files_and_dirs['files']

    dirs = files_and_dirs['dirs']
    for d in dirs:
        deep_collect_files(d, files)

    return files


def collect_files_and_dirs(dir_name):
    ls_result = next(os.walk(dir_name))

    files = {}
    for ft in file_types:
        files[ft] = []
        files[ft].extend([os.path.abspath(os.path.join(dir_name, f)) for f in ls_result[2] if f.endswith('.' + ft)])
    
    dirs = [os.path.abspath(os.path.join(dir_name, d))
            for d in ls_result[1] if not d.startswith('__') and not d.startswith('.') and d != 'help_scripts']
    
    return {'files': files, 'dirs': dirs}


def deep_collect_files(dir_name, files):
    files_and_dirs = collect_files_and_dirs(dir_name)

    for ft in file_types:
        files[ft].extend(files_and_dirs['files'][ft])
        
    for d in files_and_dirs['dirs']:
        deep_collect_files(d, files)


def compare_run_time(elapsed1, elapsed2, exe1, exe2):
    faster = None
    if elapsed2 > 2*elapsed1:
        faster = exe1
    elif elapsed2 > 2*elapsed1:
        faster = exe2

    if faster is not None:
        print('** Note: ' + faster + ' is faster')
        print(exe1 + ' run time: ' + str(elapsed1))
        print(exe2 + ' run time: ' + str(elapsed2))


if __name__=='__main__':

    parser = serv.parse(description = 'Run all simulator tests')     
    parser.add_argument('--reference_executable', type = str, dest = 'reference_executable',
                        help = 'qiskit simulator reference executable, to be compared with the main executable')
    parser.add_argument('--dir', type = str, dest = 'dir',
                        help = 'tests folder')
    
    args = parser.parse_args()

    files = collect_test_files(args.dir)

    for f in files['py']:
        print(f)

        local_seed = 1 + random.randint(0, 1000000)

        if args.reference_executable is not None:
            print('Running ' + args.executable)

        start_time = time.time()
        sp.run([f, '--seed', str(local_seed), '--executable', args.executable])
        elapsed = (time.time() - start_time)

        if args.reference_executable is not None:
            print('Running ' + args.reference_executable)
            start_time = time.time()
            sp.run([f, '--seed', str(local_seed), '--executable', args.reference_executable])
            reference_elapsed = (time.time() - start_time)
            compare_run_time(elapsed, reference_elapsed, args.executable, args.reference_executable)
            

    for f in files['json']:
        print(f)

        if args.reference_executable is not None:
            print('Running ' + args.executable)

        start_time = time.time()
        output = sp.check_output([args.executable, f]).decode()
        elapsed = (time.time() - start_time)

        reference_output = None
        if args.reference_executable is not None:
            start_time = time.time()
            reference_output = sp.check_output([args.reference_executable, f]).decode()
            reference_elapsed = (time.time() - start_time)
            compare_run_time(elapsed, reference_elapsed, args.executable, args.reference_executable)
            
        else:
            ref_file = f[:-5] + '.ref'

            try:
                with open(ref_file, "r") as ref_stream:
                    reference_output = ref_stream.read()
            except IOError:
                print('Cannot compare with ' + ref_file + ': file does not exist')
                reference_output = None
                

        if reference_output is not None:
            output_lines = output.splitlines(1)
            ref_output_lines = reference_output.splitlines(1)

            num_of_lines = len(output_lines)
            if num_of_lines != len(ref_output_lines):
                print('** Note: reference output is different')
            else:
                for i in range(num_of_lines):
                    if output_lines[i] != ref_output_lines[i]:
                        if not output_lines[i].lstrip().startswith('"time_taken"') or \
                               not ref_output_lines[i].lstrip().startswith('"time_taken"'):
                            print('** Note: reference output is different')
                            break
                        


        
        
    

    
