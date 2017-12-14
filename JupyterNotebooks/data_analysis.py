#!/usr/bin/python3
import numpy as np
import pandas as pd
import os
import math
import matplotlib.pyplot as plt


directory = "../clean_data/"

pass_df = pd.DataFrame()
files = os.listdir(directory)
for f in files:
    if "CleanedData" in f:
        pass_df = pass_df.append(pd.read_csv(directory + f))


'''
print(pass_df)
print(list(pass_df.columns.values))
print(pass_df['isAlleyOOp'].describe())
print(pass_df['PassDist'].describe())
print(pass_df['passInHull'].describe())
print(pass_df['receiverinHull'].describe())
print(pass_df['HullArea'].describe())
print(pass_df['receiverIsOpen'].describe())
print(pass_df['ShotClock'].describe())
print(pass_df['Success'].describe())
'''
pass_successes = pass_df[pass_df['Success'] == True]
pass_fails = pass_df[pass_df['Success'] == False]
'''
print(pass_successes['isAlleyOOp'].describe())
print(pass_successes['PassDist'].describe())
print(pass_successes['passInHull'].describe())
print(pass_successes['receiverinHull'].describe())
print(pass_successes['HullArea'].describe())
print(pass_successes['receiverIsOpen'].describe())
print(pass_successes['ShotClock'].describe())
'''
print(pass_fails['isAlleyOOp'].describe())
print(pass_fails['PassDist'].describe())
print(pass_fails['passInHull'].describe())
print(pass_fails['receiverinHull'].describe())
print(pass_fails['HullArea'].describe())
print(pass_fails['receiverIsOpen'].describe())
print(pass_fails['ShotClock'].describe())
