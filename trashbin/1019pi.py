import numpy as np
import matplotlib.pyplot as plt


def picalc(dot_num):
    in_range = 0
    dot_num_int = int(dot_num)
    for i in range(dot_num_int):
        loc = np.random.random(2)
        dist2 = (loc[0] - 0.5) ** 2 + (loc[1] - 0.5) ** 2
        if dist2 <= 0.25:
            in_range += 1
    return 4 * in_range / dot_num

def add_line(dotnum_lib):
    pi_res_raw = []
    for dot_num in dotnum_lib:
        pi_res_raw.append(picalc(dot_num))
    pi_res = np.array(pi_res_raw)
    #plt.scatter(dotnum_lib, pi_res, color='red', s=2, marker='x')
    plt.plot(dotnum_lib, pi_res, linewidth=0.3, color='red')

def main():
    dotnum_lib = np.logspace(1,6,11)
    try_time = 15
    for i in range(try_time):
        add_line(dotnum_lib)

    plt.axhline(y=3.1415926, ls='-',linewidth=0.5, color='blue')
    plt.xscale('log')
    plt.ylim(2.2,4.1)
    plt.xlim(1, 1000000)
    plt.show()


if __name__ == '__main__':
    main()