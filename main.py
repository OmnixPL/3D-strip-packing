#!/usr/bin/env python
"""Kacper Kula - projekt AAL
Pakowanie pudełek do pojemnika o ograniczonych dwóch wymiarach, minimalizacja trzeciego"""

from random import randrange

from algorithms import *
from box import Box
import timeit


def load_config():
    """Load user-defined variables from config.txt"""
    # config variables are fetched from file, but if not, then here are defaults
    x_of_outer = 30
    y_of_outer = 30

    min_percent = 30
    max_percent = 100

    gen = False

    measure_levels = False
    measure_simple = False
    measure_list = False

    sizes = [500, 1000, 1500, 2000, 2500]
    tries = 10

    # opens and loads variables from config file
    try:
        with open('config.txt') as config:
            for line in config:
                if line.startswith('x_of_outer='):
                    x_of_outer = int(line.split('=')[1])

                if line.startswith('y_of_outer='):
                    y_of_outer = int(line.split('=')[1])

                if line.startswith('min_percent='):
                    min_percent = int(line.split('=')[1])

                if line.startswith('max_percent='):
                    max_percent = int(line.split('=')[1])

                if line.startswith('use_generator='):
                    gen_temp = line.split('=')[1].rstrip()
                    if gen_temp == 'yes':
                        gen = True
                        print("Using generator")

                if line.startswith('measure_levels='):
                    lvl_temp = line.split('=')[1].rstrip()
                    if lvl_temp == 'yes':
                        measure_levels = True
                        print("Measuring levels algorithm")

                if line.startswith('measure_simple='):
                    simple_temp = line.split('=')[1].rstrip()
                    if simple_temp == 'yes':
                        measure_simple = True
                        print("Measuring simple algorithm")

                if line.startswith('measure_list='):
                    list_temp = line.split('=')[1].rstrip()
                    if list_temp == 'yes':
                        measure_list = True
                        print("Measuring list algorithm")

                if line.startswith('sample_sizes='):
                    gen_temp = line.split('=')[1].rstrip()
                    if gen_temp != "default":
                        sizes = list(map(int, gen_temp.split(",")))

                if line.startswith('tries='):
                    tries = int(line.split('=')[1])

    except FileNotFoundError:
        print("Could not load config file.")

    box_no = sizes[-1]

    if min_percent < 0:
        min_percent = 0
    if max_percent > 100:
        max_percent = 100

    return x_of_outer, y_of_outer, min_percent, max_percent, gen, box_no, \
        measure_levels, measure_simple, measure_list, sizes, tries


def generate_boxes(x_of_outer, y_of_outer, min_percent, max_percent, box_no):
    boxes = []

    if x_of_outer < y_of_outer:
        smaller = x_of_outer
    else:
        smaller = y_of_outer

    for i in range(box_no):
        x = randrange((min_percent * smaller) // 100, (max_percent * smaller) // 100 + 1)
        y = randrange((min_percent * smaller) // 100, (max_percent * smaller) // 100 + 1)
        z = randrange((min_percent * smaller) // 100, (max_percent * smaller) // 100 + 1)
        boxes.append(Box(x, y, z))
    return boxes


def measurements(levels_results, measure_levels, simple_results, measure_simple, list_results, measure_list,
                 sizes, boxes, outer_box, tries):
    """Measure time spent on adding/removing/enumerating elements for different sample sizes etc"""
    for size in sizes:
        # there may be too few boxes for this size of sample, so skip it
        if len(boxes) < size:
            print("Not enough boxes in dictionary for size: " + str(size))
            continue

        boxes_sized = boxes[:size]

        if measure_levels is True:
            t = timeit.Timer(lambda: levels_algorithm(outer_box, boxes_sized))
            result = t.timeit(number=tries) / tries
            levels_results.append(result)

        if measure_simple is True:
            t = timeit.Timer(lambda: simple_algorithm(outer_box, boxes_sized))
            result = t.timeit(number=tries) / tries
            simple_results.append(result)

        if measure_list is True:
            t = timeit.Timer(lambda: list_algorithm(outer_box, boxes_sized))
            result = t.timeit(number=tries) / tries
            list_results.append(result)


def display_results(level_results, measure_levels, simple_results, measure_simple, list_results, measure_list, sizes):
    if measure_levels is True:
        median = len(sizes)//2
        print("\nLevel results:")
        print("Size\tTime\t\tq")
        for i in range(len(sizes)):
            q = level_results[i] * sizes[median]**2 / (sizes[i]**2 * level_results[median])
            print('{0: >5}'.format(str(sizes[i])) + "\t" + '{:.6f}'.format(level_results[i]) + "\t" + '{:.6f}'.format(q))

    if measure_simple is True:
        median = len(sizes)//2
        print("\nSimple results:")
        print("Size\tTime\t\tq")
        for i in range(len(sizes)):
            q = simple_results[i] * sizes[median] / (sizes[i] * simple_results[median])
            print('{0: >5}'.format(str(sizes[i])) + "\t" + '{:.6f}'.format(simple_results[i]) + "\t" + '{:.6f}'.format(q))

    if measure_list is True:
        median = len(sizes)//2
        print("\nList results:")
        print("Size\tTime\t\tq")
        for i in range(len(sizes)):
            q = list_results[i] * sizes[median] / (sizes[i] * list_results[median])
            print('{0: >5}'.format(str(sizes[i])) + "\t" + '{:.6f}'.format(list_results[i]) + "\t" + '{:.4f}'.format(q))


def main():
    print("For more information: README.md")
    print("For options: config.txt")

    # variables from config file
    x_of_outer, y_of_outer, min_percent, max_percent, gen, box_no, \
        measure_levels, measure_simple, measure_list, sizes, tries = load_config()

    if gen:
        inner_boxes = generate_boxes(x_of_outer, y_of_outer, min_percent, max_percent, box_no)
    else:
        inner_boxes = [Box(10, 20, 30), Box(9, 18, 27), Box(8, 24, 16),
                       Box(1, 2, 3), Box(25, 1, 1), Box(20, 20, 20), Box(10, 10, 10)]

    levels_results = []
    simple_results = []
    list_results = []

    measurements(levels_results, measure_levels, simple_results, measure_simple, list_results, measure_list,
                 sizes, inner_boxes, Box(x_of_outer, y_of_outer, 0), tries)

    display_results(levels_results, measure_levels, simple_results, measure_simple, list_results, measure_list, sizes)

    return


if __name__ == "__main__":
    main()
