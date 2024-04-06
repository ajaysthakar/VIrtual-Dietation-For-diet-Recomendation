#!/usr/bin/env python

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import random
from app import app, mysql


def calculateCalories(age, h, w, g, act):
    cal = float()
    if g == 'male':
        cal = 88.362 + (13.397*float(w)) + (4.799*float(h)) - (5.677*float(age))
        #print (cal)
    elif g == 'female':
        cal = 447.593 + (9.247*float(w)) + (3.098*float(h)) - (4.330*float(age))
        #print(cal)
    if act == 'Sedentary (little or no exercise)':
        cal = cal*1.2
    elif act == 'Lightly active (1-3 days/week)':
        cal = cal*1.375
    elif act == 'Moderately active (3-5 days/week)':
        cal = cal*1.55
    elif act == 'Very active (6-7 days/week)':
        cal = cal*1.725
    elif act == 'Super active (twice/day)':
        cal = cal*1.9
    #print (cal)
    return cal

def main(cal):
	dataset= pd.read_excel("Food_Display_Table.xlsx")
	ds=dataset[['Food_Code','Display_Name', 'Portion_Default', 'Portion_Amount','Portion_Display_Name','Solid_Fats','Saturated_Fats','Added_Sugars','Calories']]
	d=dietation(cal,ds)
	diet=d.createPlan()
	"""
	j=0
	slot=["morning","snack","lunch","evening snack","dinner"]
	for i in diet:
		print(slot[j].upper())
		d.displayDiet(i)
		j+=1
	"""
	return diet

class dietation:
    def __init__(self,cal,ds):
        self.cal=cal
        self.ds=ds
    def displayDiet(self,diet):
        print(diet[["Display_Name","Portion_Display_Name","Calories"]])
    def calorieDivide(self):
        return [self.cal/5,self.cal/10,self.cal/10,self.cal/20,self.cal/4]
    def cluster(self,temp,c):
        ind=list(temp.index)
        t,f=0,0
        items=[]
        while f < 10:
            i=random.choice(ind)
            if (t+temp.loc[i]['Calories']) > c:
                f+=1
                continue
            else:
                t+=temp.loc[i]['Calories']
                items.append(temp.loc[i])
        return pd.core.frame.DataFrame(items).to_html()
    def createPlan(self):
        diet=[]
        s=self.calorieDivide()
        for i in s:
            diet.append(self.cluster(self.ds[self.ds['Calories'] < i],i))
        return diet

def generator(user):

    name=user[0]
    age=float(user[1])
    h=float(user[2])
    w=float(user[3])
    g=user[4]
    act=user[5]
    #acts=['Sedentary (little or no exercise)','Lightly active (1-3 days/week)','Moderately active (3-5 days/week)','Very active (6-7 days/week)','Super active (twice/day)']
    
    """
    name="ajay"
    age=22
    h=160.0
    w=100.0
    g="male"
    act=acts[2]
    """
    cal=calculateCalories(age, h, w, g, act)
    hm=h/100  #cm to m converter
    bmi=w/(hm*hm)
    slot=["morning","snack","lunch","evening snack","dinner"]
    #bmi=31
    if (bmi >= 18.5) and (bmi <= 24.9):
        pass
    elif (bmi >= 25.0) and (bmi <= 29.9):
        cal=(cal*90)/100
    elif (bmi >= 30.0):
        cal=(cal*80)/100
    elif (bmi >= 17.0) and(bmi <= 18.4):
        cal=(cal*110)/100
    elif (bmi < 17.0):
        cal=(cal*120)/100
    diet=main(cal)
    return diet


#generator()
