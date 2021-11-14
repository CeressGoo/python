from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt
import random

draw_count = 0
hit_count = 0
prob = 0.02
loop_time = 50000000
wait_list = []

for i in range(loop_time):
    draw_count += 1
    #dice = np.random.ranf(1)[0]
    dice = random.random()
    if draw_count > 50:
        prob = np.min([prob+0.02, 1])
    if dice <= prob:
        hit_count += 1
        wait_list.append(draw_count+0.1)
        draw_count = 0
        #print(f'{hit_count} hits in {i} tries.')
        prob = 0.02

print(f'{hit_count} hits in {i+1} tries.')
print(f'{loop_time/hit_count} tries to hit once in average.')

wait_arr = np.array(wait_list)
plt.hist(wait_arr, bins=102, range=(0,101), rwidth=0.8)
plt.xlim(0,101)
plt.ylim(0,60000)
plt.xticks(range(0,100,10))
plt.xlabel('Interval between two 6*')
plt.ylabel('Counts')
plt.vlines(50, 0, 60000, colors='red', linestyles='dashed')
plt.savefig('D:/CeressCode/python/DrawSim/hist1.png')
plt.show()

plt.hist(wait_arr, bins=102, range=(0,101), rwidth=0.2, cumulative=True)
plt.xlim(0,101)
plt.xticks(range(0,100,10))
plt.hlines(int(hit_count/4), 0, 100, colors='green', linewidth=1.0, linestyles='dotted')
plt.hlines(int(hit_count/2), 0, 100, colors='green', linewidth=1.5, linestyles='dashed')
plt.hlines(int(hit_count*0.75), 0, 100, colors='green', linewidth=1.0, linestyles='dotted')
plt.hlines(int(hit_count), 0, 100, colors='green', linewidth=1.5, linestyles='dashed')
plt.vlines(50, 0, 1500000, colors='red', linestyles='dashed')
plt.xlabel('Interval between two 6*')
plt.ylabel('Accumulated counts')
plt.savefig('D:/CeressCode/python/DrawSim/cumu2.png')
plt.show()
