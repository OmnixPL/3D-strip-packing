#!/usr/bin/env python
"""Kacper Kula - projekt AAL
Pakowanie pudełek do pojemnika o ograniczonych dwóch wymiarach, minimalizacja trzeciego"""

import timeit


def load_config():
    """Load user-defined variables from config.txt"""
    # config variables are fetched from file, but if not, then here are defaults
    x_of_outer = 300
    y_of_outer = 300

    min_percent = 30
    max_percent = 100

    box_no = 10

    measure_levels = False
    measure_simple = False
    measure_list = False

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

                if line.startswith('box_no='):
                    box_no = int(line.split('=')[1])

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

    except FileNotFoundError:
        print("Could not load config file.")
    return x_of_outer, y_of_outer, min_percent, max_percent, box_no, measure_levels, measure_simple, measure_list

