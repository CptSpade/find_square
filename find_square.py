#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

def grand_carre(files_names):
    line_nb = 0
    void_ch = "."
    obs_ch = "o"
    fill_ch = "x"

    for fn in files_names:
        first_line = True
        #I had an error on the 1st character, the solution I found was to use utf-16 as encoding
        with open(fn, "r", encoding="utf-16") as f:
            line = f.readline()
            if not (re.findall('\d+', line)) or not (line[0].isdigit()):
                print("map error")
                f.close()
            else:
                line_nb = int(re.findall('\d+', line)[0])
                if len(line) != len(str(line_nb)) + 4 or line_nb <= 0:
                    #this will cause a "map error" if the number of lines start by a 0 (ex: 09)
                    print("map error")
                    f.close()
                else:
                    void_ch = line[len(str(line_nb))]
                    obs_ch = line[len(str(line_nb)) + 1]
                    fill_ch = line[len(str(line_nb)) + 2]
                    if not (check_map(line_nb, void_ch, obs_ch, fill_ch, f)):
                        print("map error")
                        f.close()
                    else:
                        algo_replace(line_nb, void_ch, obs_ch, fill_ch, f)

def algo_replace(line_nb, void_ch, obs_ch, fill_ch, f):
    start_point = [0, 0]
    best_start_point = [0, 0]
    square_side = 0
    best_square_side = 0
    x = 0
    y = 0
    xi = 0
    yi = 0
    arr = []
    #replacing the cursor at the beginning of the file
    f.seek(0)
    #skipping the 1st line
    f.readline()
    for line in f:
        arr.append(list(line))
    while yi < line_nb:
        while xi < len(arr[0]):
            start_point = [xi, yi]
            obs_found = False
            if arr[yi][xi] == void_ch:
                x = xi
                y = yi
                if x < len(arr[0]) - 1 and y < line_nb - 1:
                    while (x < len(arr[0]) - 1 or y < line_nb - 1) and obs_found == False:
                        x += 1
                        y += 1
                        square_side += 1
                        if x >= len(arr[0]) or y >= line_nb:
                            obs_found = True
                        while x >= xi and obs_found == False:
                            if arr[y][x] == obs_ch:
                                obs_found = True
                            x -= 1
                        x = xi + square_side
                        while y >= yi and obs_found == False and y < line_nb:
                            if arr[y][x] == obs_ch:
                                obs_found = True
                            y -= 1
                        y = yi + square_side
                        if square_side > best_square_side:
                            best_square_side = square_side
                            best_start_point = start_point
                    x = 0
                    y = 0
                    square_side = 0
            xi += 1
        xi = 0
        yi += 1
    #prints solution
    f.seek(0)
    f.readline()
    square = ""
    while best_square_side > 0:
        square = square + fill_ch
        best_square_side -= 1
    for lidx, line in enumerate(f):
        if lidx >= best_start_point[1] and lidx < best_start_point[1] + len(square):
            print(line[:best_start_point[0]] + square + line[best_start_point[0]+len(square):])
        else:
            print(line)
    f.close()

def check_map(line_nb, void_ch, obs_ch, fill_ch, f):
    check_chars = [void_ch, obs_ch, fill_ch, "\n"]
    for line_idx, line in enumerate(f):
        for ch in line:
            if not ch in check_chars:
                return False
        if line[-1] != "\n":
            return False
    if line_idx + 1 != int(line_nb):
        return False
    len_line = len(line)
    f.seek(0)
    f.readline()
    for line in f:
        if len(line) != len_line:
            return False
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Missing parameters.')
        exit()
    grand_carre(sys.argv[1:])