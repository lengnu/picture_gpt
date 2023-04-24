"""
@FileName：commuication.py
@Description：
@Author：duwei
@Time：2023/4/18 16:57
@Email: 1456908874@qq.com
"""
import pandas as pd
import matplotlib.pyplot as plt

z_p_start_length = 1024
n_length = 1024
max_number = 1000
step = 100
ratio_max = 0.4
index_range = range(100, max_number + 1, step)
ratio_range = [0, 10, 20, 30, 40]
dict_result = {}
colors = ['#0072BD', '#D95318', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F']
styles = [
    {'linestyle': '-', 'marker': 'o', 'color': '#0072BD'},
    {'linestyle': '-', 'marker': 'x', 'color': '#D95318'},
    {'linestyle': '-', 'marker': 'v', 'color': '#EDB120'},
    {'linestyle': '-', 'marker': '*', 'color': '#7E2F8E'},
    {'linestyle': '-', 'marker': 'D', 'color': '#77AC30'},
]
# styles = [
#     {'linestyle': '-', 'marker': 'o', 'color': '#D35400'},
#     {'linestyle': '--', 'marker': 'x', 'color': '#16A085'},
#     {'linestyle': '-.', 'marker': 'v', 'color': '#7D3C98'},
#     {'linestyle': ':', 'marker': '*', 'color': '#2874A6'},
#     {'linestyle': (0, (3, 5, 1, 5)), 'marker': 'D', 'color': '#F39C12'},
# ]
# styles = [
#     {'linestyle': '-', 'marker': 'o', 'color': '#2E86C1'},
#     {'linestyle': '-', 'marker': 'x', 'color': '#B03A2E'},
#     {'linestyle': '-', 'marker': 'v', 'color': '#229954'},
#     {'linestyle': '-', 'marker': '*', 'color': '#9B59B6'},
#     {'linestyle': '-', 'marker': 'D', 'color': '#F39C12'},
# ]
for ratio in ratio_range:
    cost = []
    for num_sm in index_range:
        cost_result = (6 * z_p_start_length) + (2 * num_sm - 2 * num_sm * (ratio / 100.0) + 2) * n_length
        cost_result = cost_result / 1_000_000
        cost.append(cost_result)

    key = '{:2d}'.format(ratio) + '% SM failures'
    dict_result[key] = cost
df = pd.DataFrame(dict_result, index=index_range)
# df.to_csv('./ratio.csv', sep='\t', index=True)

fig, ax = plt.subplots()
index = 0
for scheme in df.columns:
    ax.plot(df[scheme], linestyle=styles[index]['linestyle'], marker=styles[index]['marker'],
            color=styles[index]['color'], label=scheme)
    index = index + 1
ax.set_xlabel('No. of SMs')
ax.set_ylabel('Communication overhead (Mb)')

# 设置横坐标的刻度
ax.set_xticks(index_range)
ax.set_xticklabels([str(x) for x in index_range])
ax.legend()
plt.savefig('communication_overhead.pdf')
