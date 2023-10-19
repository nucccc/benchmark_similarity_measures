'''
hopefully this could recompile stuff, switch branches and so on
'''

import json

import git

import subprocess

from getpass import getpass

import pandas as pd

def run_benchmark() -> dict[str:dict[str:any]]:
    '''
    run_benchmark shall execute all the benchmark
    '''
    RUN_BENCHMARK_CMD = 'python3 run_benchmark.py'.split()
    cmd = subprocess.run(
        RUN_BENCHMARK_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="ascii",
    )
    result = cmd.stdout
    #print(result)
    benchmark_result = json.loads(result)
    return benchmark_result


def checkout_and_install(branch_name : str, repo : git.Repo, psw : str):
    branch = repo.heads[branch_name]
    branch.checkout()
    cmd = subprocess.run(
        INSTALL_CMD_SUDO, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=psw, encoding="ascii",
    )
    #print(cmd.stdout)

def benchmark_branch(branch_name : str, repo : git.Repo, psw : str) -> dict[str:dict[str:any]]:
    checkout_and_install(branch_name, repo, psw)
    return run_benchmark()

psw = getpass("password: ")

REPO_PATH = '/home/nuc/cod/projs/similarity_measures'

MASTER_HEAD = 'master'
CYTHON_HEAD = 'feature/cython_3_0'

INSTALL_CMD = 'python3 -m pip install /home/nuc/cod/projs/similarity_measures'.split()
INSTALL_CMD_SUDO = ['sudo'] + INSTALL_CMD

repo = git.Repo(REPO_PATH)

print('running benchmarks for master branch')
master_result = benchmark_branch(MASTER_HEAD, repo, psw)

print('running benchmarks for cython branch')
cython_result = benchmark_branch(CYTHON_HEAD, repo, psw)

common_keys = set(master_result.keys()).intersection(set(cython_result.keys()))

to_be_df = list()
for key in common_keys:
    avg = master_result[key]['avg']
    cy_avg = cython_result[key]['avg']
    entry = {
        'benchmark_name' : key,
        'master_avg' : avg,
        'cython_avg' : cy_avg
    }
    entry['improv'] = (avg - cy_avg) / avg * 100
    to_be_df.append(entry)

df = pd.DataFrame(to_be_df)
df.to_csv('comparison.csv', index=False)