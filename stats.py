#!/usr/bin/env python3
import numpy as np
import json

def calculate_stats(truth, data, statsoutname=None, verbose=False):
    correlation_matrix = np.corrcoef(truth, data)
    correlation_xy = correlation_matrix[0,1]
    r_squared = correlation_xy**2
    bias = np.mean(data) - np.mean(truth)
    moratio = np.mean(data) / np.mean(truth)
    rbias = bias / np.mean(truth)
    ssize = len(truth)

    stats_dict = {
        'Counts': "%.0f" % ssize,
        'Absolute Bias': "%.3f" % bias,
        'Relative Bias': "%.3f" % rbias,
        'R': "%.3f" % correlation_xy,
        'R\u00b2': "%.3f" % r_squared,
    }
    if verbose:
        print(stats_dict)

    if statsoutname is not None:
        with open(statsoutname, 'w') as f:
            json.dump(d, f)

    return stats_dict

def is_significant(data1, data2, n_boot, ci_level=95):
    n_bootstraps = n_boot
    boot_diffs = np.empty(n_bootstraps)

    for i in range(n_bootstraps):
        sample1 = np.random.choice(data1, size=len(data1), replace=True)
        sample2 = np.random.choice(data2, size=len(data2), replace=True)
        boot_diffs[i] = np.mean(sample1) - np.mean(sample2)

    width = round((100 - ci_level)/2, 1)
    ci_lower = np.percentile(boot_diffs, width)
    ci_upper = np.percentile(boot_diffs, 100 - width)

    significant = not (ci_lower <= 0 <= ci_upper)

    return significant
