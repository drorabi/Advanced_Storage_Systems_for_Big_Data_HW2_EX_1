import numpy as np
import random
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def set_pages_calls():
    pages_calls = list(range(1000))
    pages = list(np.arange(2000))
    index = list(np.arange(1000))
    x_80_percent_index, x_20_percent_index = train_test_split(index, test_size=.20, shuffle=True)
    x_80_percent_pages, x_20_percent_pages = train_test_split(pages, test_size=.20, shuffle=True)

    for i in range(1000):
        if i in x_80_percent_index:
            page_to_call = random.choice(x_20_percent_pages)
        else:
            page_to_call = random.choice(x_80_percent_pages)

        pages_calls[i] = page_to_call

    return pages, pages_calls


def calc_dis_to_next_call(pages_calls_left, page):
    dis = 0
    for call in pages_calls_left:
        if page != call:
            dis += 1
        else:
            break
    return dis


def find_furthest_page_call_loc_in_cache(pages_calls_left, opt_cache):
    index = list(np.arange(len(opt_cache)))
    furthest_index = 0
    furthest_dis = calc_dis_to_next_call(pages_calls_left, opt_cache[0])

    for i in index[1:]:
        dis_to_next_call = calc_dis_to_next_call(pages_calls_left, opt_cache[i])
        if dis_to_next_call >= len(pages_calls_left):
            furthest_index = i
            break
        if dis_to_next_call > furthest_dis:
            furthest_index = i

    return furthest_index


def run_workload(pages, pages_calls):
    cache_sizes = [20, 50, 70, 100, 200]
    rand_avg_miss = []
    opt_avg_miss = []
    for size in cache_sizes:
        rand_miss = 0
        opt_miss = 0
        for iter in range(10):
            rand_cache = list(np.ones(size) * -1)
            opt_cache = list(np.ones(size) * -1)
            for i in range(len(pages_calls)):
                called_page = pages_calls[i]
                if called_page not in rand_cache:
                    rand_miss += 1
                    i = random.choice(range(size))
                    rand_cache[i] = called_page

                if called_page not in opt_cache:
                    opt_miss += 1
                    i = find_furthest_page_call_loc_in_cache(pages_calls[i:], opt_cache)
                    opt_cache[i] = called_page

        rand_avg_miss.append(rand_miss / 10)
        opt_avg_miss.append(opt_miss / 10)
    return cache_sizes, opt_avg_miss, rand_avg_miss


def plot_data(cache_sizes, opt_avg_miss, rand_avg_miss):
    plt.xlabel("Cache size", fontsize=10)
    plt.ylabel("Page miss avg", fontsize=10)
    plt.plot(cache_sizes, opt_avg_miss, label="OPT cache")
    plt.plot(cache_sizes, rand_avg_miss, label="RAND cache")
    plt.legend()
    plt.show()


def ex1():
    pages, pages_calls = set_pages_calls()
    cache_sizes, opt_avg_miss, rand_avg_miss = run_workload(pages, pages_calls)
    plot_data(cache_sizes, opt_avg_miss, rand_avg_miss)


if __name__ == '__main__':
    ex1()
