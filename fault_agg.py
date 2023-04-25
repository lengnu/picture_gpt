import math

import pandas as pd
from matplotlib import pyplot as plt

t_point = 6.8780577
t_pair = 3.7929045
t_hash = 0.1697992

t_exp = 0.8186955000
t_add = 0.0000881400
t_mul = 0.0003266900
max_number = 500
t = int(max_number / 2 + 1)
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


def fpda_fault_costs(n, t, t_func, l):
    fpda_cost = {
        'init': 2 * n * t_exp + n * (n - 1) * t_func + 2 * n * t_mul + 3 * n * t_add + n * t_hash,
        'enc': (n - l) * (2 * t_exp + 2 * t_mul + t_hash),
        'agg': (l + l * t) * t_exp + (l * (t ** 2) + l * t - l + n - 1) * t_mul + (
                l * (t ** 2) - l * t + l) * t_add + l * t_hash,
        'dec': t_exp + 3 * t_mul + (l + 1) * t_add + t_hash,
    }
    fpda_cost['total'] = sum(fpda_cost.values())
    return fpda_cost


def ftma_fault_costs(n, t, l):
    ftma_cost = {
        'init': t * t_pair + t * t_point + 2 * t * t_mul + t * t_add + t * t_hash,
        'enc': (n - l) * (3 * t_exp + 3 * t_mul + t_add + t_hash),
        'agg': l * t_pair + l * t_point + 3 * t_exp + (n + l + 2) * t_mul + (l + 1) * t_add + (l + 1) * t_hash,
        'dec': t_exp + 2 * t_mul + (l + 1) * t_add,
    }
    ftma_cost['total'] = sum(ftma_cost.values())
    return ftma_cost


def efdpa_fault_costs(n, t_func, l):
    efpda_cost = {
        'init': 2 * n * t_func + n * (n - 1) * t_add + n * (n - 1) * t_mul,
        'enc': (n - l) * (2 * t_exp + 4 * t_mul + t_add + t_hash),
        'agg': t_exp + l * t_func + (n + 1) * t_mul + l * t_add + t_hash,
        'dec': t_exp + l * t_func + (l + 2) * t_mul + (l + 1) * t_add,
    }
    efpda_cost['total'] = sum(efpda_cost.values())
    return efpda_cost


colors = ['#0072BD', '#D95318', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F']
styles = {
    # 'VPMDA': {'linestyle': '-', 'marker': 'o', 'color': '#7E2F8E'},
    'FPDA [27]': {'linestyle': '-', 'marker': 'x', 'color': '#D95318'},
    'FTMA [31]': {'linestyle': '-', 'marker': '^', 'color': '#EDB120'},
    'EFDPA': {'linestyle': '-', 'marker': '*', 'color': '#0072BD'},
}
scheme_list = ['FPDA [27]', 'FTMA [31]', 'EFDPA']
result = {}
ratio_range = [5, 10, 15, 20, 25, 30, 35, 40]

for max_number in range(100,1000 + 1,100):
    t = int(max_number / 2 + 1)

    for scheme in scheme_list:
        total_costs = []
        for fault in ratio_range:
            cur_cost = 0
            t_func = t_func_dict[t]
            l = int(max_number * fault / 100)

            if scheme == 'FPDA [27]':
                cur_cost = fpda_fault_costs(max_number, t, t_func, l)['dec'] + fpda_fault_costs(max_number, t, t_func, l)[
                    'agg']
            elif scheme == 'FTMA [31]':
                cur_cost = ftma_fault_costs(max_number, t_func, l)['dec'] + ftma_fault_costs(max_number, t_func, l)['agg']
            elif scheme == 'EFDPA':
                cur_cost = efdpa_fault_costs(max_number, t_func, l)['dec'] + efdpa_fault_costs(max_number, t_func, l)['agg']
            total_costs.append(cur_cost)
        result[scheme] = total_costs
    df = pd.DataFrame(result, index=ratio_range)
    print(df
          )
# fig, ax = plt.subplots()

# # 修改画图部分，使用不同线形和标记
# for scheme in scheme_list:
#     ax.plot(df[scheme], linestyle=styles[scheme]['linestyle'],
#             color=styles[scheme]['color'], marker=styles[scheme]['marker'], label=scheme)
# ax.set_xlabel('Proportion of Faulty SMs')
# ax.set_ylabel('Computation overhead (ms)')
# ax.set_xticks(ratio_range)
# ax.set_xticklabels(['{:2d}%'.format(x) for x in ratio_range])
# # ax.set_yscale('log')  # 修改为正确的对数刻度设置
# ax.legend()
# # plt.savefig('./result/proportion_of_faulty.pdf')
# plt.show()
