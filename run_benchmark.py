import similaritymeasures

import json
import timeit
import numpy as np

benchmark_result : dict[str:dict[str:any]] = dict()

x1 = np.linspace(0.0, 1.0, 500)
y1 = np.ones(500)*2
x2 = np.linspace(0.0, 1.0, 250)
y2 = np.ones(250)

np.random.seed(1212121)
curve_a_rand = np.random.random((100, 2))
curve_b_rand = np.random.random((90, 2))

curve1 = np.array((x1, y1)).T
curve2 = np.array((x2, y2)).T

r1 = 10
r2 = 100
theta = np.linspace(0.0, 2.0*np.pi, 500)
x1 = np.cos(theta)*r1
x2 = np.cos(theta)*r2
y1 = np.sin(theta)*r1
y2 = np.sin(theta)*r2
curve5 = np.array((x1, y1)).T
curve6 = np.array((x2, y2)).T

def run_frechet_c1_c2():
    return similaritymeasures.frechet_dist(curve1, curve2)

def run_frechet_c5_c6():
    return similaritymeasures.frechet_dist(curve5, curve6)

def run_area_between_two_curves_c1_c2():
    return similaritymeasures.area_between_two_curves(curve1, curve2)

def run_area_between_two_curves_c5_c6():
    return similaritymeasures.area_between_two_curves(curve5, curve6)

def run_pcm_c1_c2():
    return similaritymeasures.pcm(curve1, curve2)

def run_curve_length_measure_c1_c2():
    return similaritymeasures.curve_length_measure(curve1, curve2)

def run_dtw_c1_c2():
    return similaritymeasures.dtw(curve1, curve2)

def run_dtw_c5_c6():
    return similaritymeasures.dtw(curve5, curve6)

bnchmks = {
    'frechet_c1_c2':run_frechet_c1_c2,
    'frechet_c5_c6':run_frechet_c5_c6,
    'area_between_two_curves_c1_c2':run_area_between_two_curves_c1_c2,
    'area_between_two_curves_c5_c6':run_area_between_two_curves_c5_c6,
    'pcm_c1_c2':run_pcm_c1_c2,
    'curve_length_measure_c1_c2':run_curve_length_measure_c1_c2,
    'dtw_c1_c2':run_dtw_c1_c2,
    'dtw_c5_c6':run_dtw_c5_c6
}

n_repeats = 50
n_runs = 20

for name, func in bnchmks.items():

    times_list = timeit.repeat(func, repeat = n_repeats, number = n_runs)

    total = sum(times_list)
    avg = total / len(times_list)

    func_result = {
        'times_list':times_list,
        'total':total,
        'avg':avg
    }

    benchmark_result[name] = func_result

result_encoded = json.dumps(benchmark_result)
print(result_encoded)