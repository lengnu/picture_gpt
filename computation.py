"""
@FileName：computation.py
@Description：
@Author：duwei
@Time：2023/4/21 10:35
@Email: 1456908874@qq.com
"""
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

t_point = 6.8780577
t_pair = 3.7929045
t_hash = 0.1697992

t_exp = 0.8186955000
t_add = 0.0000881400
t_mul = 0.0003266900
max_number = 500

step = 100
col_index = range(100, max_number + 1, step)
# 0.3649   1.6976  2.8104  7.6116  13.7901  20.5776  32.9723  47.3940  63.7902   82.2772
# t_func_dict = {
#     51: 0.3649,
#     101: 1.6976,
#     151: 2.8104,
#     201: 7.6116,
#     251: 13.7901,
#     301: 20.5776,
#     351: 32.9723,
#     401: 47.3940,
#     451: 63.7902,
#     501: 82.2772
# }

t_func_dict = {
    51: 0.0743419000,
    101: 0.1507826000,
    151: 0.2064470000,
    201: 0.2735668000,
    251: 0.3321555000,
    301: 0.4132675000,
    351: 0.4889837000,
    401: 0.5355212000,
    451: 0.6104819000,
    501: 0.6840049000
}


def vpmda_costs(n):
    vpmda_cost = {
        'init': n * t_exp + n * t_add + n * t_hash,
        'enc': n * (2 * t_exp + 2 * t_mul + t_hash),
        'agg': (n - 1) * t_mul,
        'dec': t_mul + t_add,
    }
    vpmda_cost['total'] = sum(vpmda_cost.values())
    return vpmda_cost


def fpda_costs(n, t_func):
    fpda_cost = {
        'init': 2 * n * t_exp + n * (n - 1) * t_func + 2 * n * t_mul + 3 * n * t_add + n * t_hash,
        'enc': n * (2 * t_exp + 2 * t_mul + t_hash),
        'agg': (n - 1) * t_mul,
        'dec': t_exp + 3 * t_mul + t_add,
    }
    fpda_cost['total'] = sum(fpda_cost.values())
    return fpda_cost


def ftma_costs(n, t):
    ftma_cost = {
        'init': t * t_pair + t * t_point + 2 * t * t_mul + t * t_add + t * t_hash,
        'enc': n * (3 * t_exp + 3 * t_mul + t_add + t_hash),
        'agg': (n - 1) * t_mul,
        'dec': t_exp + 2 * t_mul + t_add,
    }
    ftma_cost['total'] = sum(ftma_cost.values())
    return ftma_cost


def efdpa_costs(n, t_func):
    efpda_cost = {
        'init': 2 * n * t_func + n * (n - 1) * t_add + n * (n - 1) * t_mul,
        'enc': n * (2 * t_exp + 4 * t_mul + t_add + t_hash),
        'agg': t_exp + (n + 1) * t_mul + t_add + t_hash,
        'dec': t_add,
    }
    efpda_cost['total'] = sum(efpda_cost.values())
    return efpda_cost


colors = ['#0072BD', '#D95318', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F']
styles = {
    'VPMDA': {'linestyle': '-', 'marker': 'o', 'color': '#0072BD'},
    'FPDA': {'linestyle': '-', 'marker': 'x', 'color': '#D95318'},
    'FTMA': {'linestyle': '-', 'marker': 'v', 'color': '#EDB120'},
    'EFDPA': {'linestyle': '-', 'marker': '*', 'color': '#7E2F8E'},
}
scheme_list = ['VPMDA', 'FPDA', 'FTMA', 'EFDPA']
result = {}
for scheme in scheme_list:
    total_costs = []
    for n in col_index:
        t = int(math.floor(n / 2) + 1)
        t_func = t_func_dict[t]

        cur_cost = 0
        if scheme == 'VPMDA':
            cur_cost = vpmda_costs(n)['total']
        elif scheme == 'FPDA':
            cur_cost = fpda_costs(n, t_func)['total']
        elif scheme == 'FTMA':
            cur_cost = ftma_costs(n, t)['total']
        elif scheme == 'EFDPA':
            cur_cost = efdpa_costs(n, t_func)['total']
        total_costs.append(cur_cost)
    result[scheme] = total_costs

df = pd.DataFrame(result, index=col_index)
fig, ax = plt.subplots()

# 修改画图部分，使用不同线形和标记
for scheme in scheme_list:
    ax.plot(df[scheme], linestyle=styles[scheme]['linestyle'],
            color=styles[scheme]['color'], marker=styles[scheme]['marker'], label=scheme)

ax.set_xlabel('No. of SMs')
ax.set_ylabel('Computation overhead (ms)')
ax.set_xticks(col_index)
ax.set_xticklabels([str(x) for x in col_index])
ax.set_ylim(np.min(df['VPMDA']) * 0.9, np.max(df['FPDA']) * 1.1)
# ax.set_yscale('log')  # 修改为正确的对数刻度设置
ax.legend()
plt.show()
# plt.savefig('Computation_overhead_schemes.pdf')
