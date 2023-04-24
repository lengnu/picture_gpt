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

for ratio in ratio_range:
    cost = []
    for num_sm in index_range:
        cost_result = (6 * z_p_start_length) + (2 * num_sm - 2 * num_sm * (ratio / 100.0) + 2) * n_length
        cost_result = cost_result / 1_000_000
        cost.append(cost_result)

    key = '{:2d}'.format(ratio) + '% SM failures'
    dict_result[key] = cost

df = pd.DataFrame(dict_result, index=index_range)

# 设定颜色列表，为每条线分配不同颜色
#colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231']
colors = ['#2E86C1', '#B03A2E', '#229954', '#9B59B6', '#F1C40F']
fig, ax = plt.subplots()

for index, scheme in enumerate(df.columns):
    # 使用颜色列表中的颜色，为每条线分配颜色
    ax.plot(df[scheme], linestyle='-', marker='*', color=colors[index], label=scheme)

ax.set_xlabel('No. of SMs')
ax.set_ylabel('Communication overhead (Mb)')

# 设置横坐标的刻度
ax.set_xticks(index_range)
ax.set_xticklabels([str(x) for x in index_range])
ax.legend()
plt.show()
