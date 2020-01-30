import numpy
import pandas
import matplotlib
from sklearn.model_selection import train_test_split
import os,glob
from itertools import combinations


def process_data (filename):
    df = pandas.read_csv(filename)
    heroes = df["Column 1"]
    win_info = df["Column 5"]
    data_set = list()
    for index in range(1,len(heroes)):
      temp_win_info = win_info[index].split()
      win_rate = temp_win_info[0]
      win_match_num = temp_win_info[1]
      data_row = (heroes[index], win_rate, win_match_num)
      data_set.append(data_row)
    return data_set


def open_file(name):
    result = list()
    path = "heroes/"
    filename = name+".csv"
    df = pandas.read_csv(path+filename)
    heroes = df["Column 1"]
    win_rate = df["Column 3"]
    advantage = df["Column 4"]
    for index in range(1, len(heroes)):
        data_row = (heroes[index], win_rate[index],advantage[index])
        result.append(data_row)
    return result


def find(set, hero_name):
    for item in set:
        if item[0] == hero_name:
            result = item
            break
    return result

def calculate_factor( data_set, hero1_set, hero1, hero2):
    temp1 = find(data_set, hero1)
    base_win_rate = temp1[1]
    temp2 = find(hero1_set, hero2)
    factor = temp2[1]
    result = float(base_win_rate) - float(factor)
    return result

def calculate_advan(set, hero_name):
    temp = find(set, hero_name)
    result = temp[2]
    return result

def calculate_winrate(radi, dire):
    data_set = process_data("pros.csv")
    result = 0.0
    for radi_name in radi:
        base_info = find(data_set,radi_name)
        base_rate = float(base_info[1])
        hero_set = open_file(radi_name)
        factor = 0.0
        advan = 0.0
        advantage = 0.0
        for dire_name in dire:
          factor += calculate_factor(data_set, hero_set, radi_name, dire_name)
          advan += calculate_advan(hero_set,dire_name)
        base_rate += factor
        result += base_rate
        advantage = advan
    result = result/len(radi)
    return [result,advantage]

def print_match_info (radi, dire):
    radi_camp = ""
    dire_camp = ""
    for name in radi:
        radi_camp += name + " "
    for name in dire:
        dire_camp += name + " "
    print("Radiance: "+radi_camp +
          "\n" + "   |Versus|   " +
          "\n"+ "Dire: "+ dire_camp)
    print ("***********************************")

def print_winrate(winrate):
    if winrate > 50.00:
        print("Radiance will win~")
    elif winrate < 50.00:
        print ("Dire will win~")
    elif winrate == 50.00:
        print ("Match probably draw")
    else:
        print("Error: cannot calculate")
    print ("***********************************")

def generator(radi, dire):
    info = calculate_winrate(radi, dire)
    WR = info[0]
    AD = info[1]
    info1 = calculate_winrate(dire, radi)
    AD1 = info1[1]
    print_match_info(radi, dire)
    print("Predicted Win Rate : ")
    print(WR)
    print("R-D Advantage State:")
    print(AD)
    print("D-R Advantage State:")
    print(AD1)
    ad_rate = (AD / (AD + AD1)) * 100
    print("Winrate based on advantage:")
    print(ad_rate)

    print("====================================")

def switcher(winner, predictor):
    if winner == "Radiance" and predictor == 1:
        return True
    elif winner == "Dire" and predictor == 0:
        return True
    else:
        return False

def comparator(radi, dire, winner):
    info = calculate_winrate(radi, dire)
    WR = info[0]
    AD = info[1]
    info1 = calculate_winrate(dire, radi)
    AD1 = info1[1]
    print_match_info(radi, dire)
    print("Predicted Win Rate : ")
    print(WR)
    print("R-D Advantage State:")
    print(AD)
    print("D-R Advantage State:")
    print(AD1)
    ad_rate = (AD / (AD + AD1)) * 100
    print("Winrate based on advantage:")
    print(ad_rate)
    print("====================================")

    if WR >= 50.0:
        bool = 1
        predict_winner = "Radiance"
    elif WR < 50:
        bool = 0
        predict_winner = "Dire"
    if ad_rate >= 50:
        ad_bool = 1
        ad_winner = "Radiance"
    elif ad_rate < 50:
        ad_bool = 0
        ad_winner = "Dire"
    p_flag = switcher(winner, bool)
    a_flag = switcher(winner, ad_bool)

    return [p_flag,a_flag,"Predict winner is: "+predict_winner+ " AD_winner: "+ad_winner +" |True winner is: " +winner]


