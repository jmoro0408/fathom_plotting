# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 19:45:46 2020

@author: JM070903
"""

#%% Imports

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
#%% importing data

os.chdir(r"C:\Users\JM070903\PycharmProjects\Fathom_Matplotlib_Pipeline") #move to directory
xl = pd.read_excel(r"Fathom/Fathom_Output.xlsx", sheet_name = None) #import excel file
sheet_names = xl.keys()
sheet_names = list(sheet_names)


#%% Create pump curve class

class Curve:
    def __init__(self, speed = None, pump_flow = None, pump_head = None, system_curve_flow = None, system_curve_head = None, efficiancy = None, \
                 aor_flow = None, aor_head = None, por_flow = None, por_head = None):
        self.speed = speed
        self.pump_flow = pump_flow
        self.pump_head = pump_head
        self.system_curve_flow = system_curve_flow
        self.system_curve_head = system_curve_head
        self.efficiancy = efficiancy
        self.aor_flow = aor_flow
        self.aor_head = aor_head
        self.por_flow = por_flow
        self.por_head = por_head
        
    def curve_speed(self):
        print("Speed is: \n" + str(self.speed))
    def curve_pump_flow(self):
        print("pump flow is: \n" + str(self.pump_flow))
    def curve_pump_head(self):
        print("pump head is: \n" +str(self.pump_head))
    def curve_system_flow(self):
        print("system curve flow is: \n" + str(self.system_curve_flow))
    def curve_system_head(self):
        print("system curve head is: \n" + str(self.system_curve_head))
    def curve_efficiancy(self):
        print("efficiancy is: \n" + str(self.efficiancy))
    def curve_aor_flow(self):
        print("AOR Flow is: \n" + str(self.aor_flow))
    def curve_aor_head(self):
        print("AOR Head is: \n" + str(self.aor_head))     
    def curve_por_flow(self):
        print("POR Flow is: \n" + str(self.por_flow))  
    def curve_por_head(self):
        print("POR Head is: \n" + str(self.por_head))  
               


#%%
curve_dict = {}
for i in range(0,len(xl)):
    curve_dict["Sheet%s" %i] = {}

for sheet in sheet_names:
    curve_dict[sheet] = Curve(speed = xl[sheet]["Speed (%)"][0], pump_flow = xl[sheet]["Pump Flow"], \
                                     pump_head = xl[sheet]["Pump Head"], system_curve_flow = xl[sheet]["System Curve Flow"], \
                                         system_curve_head = xl[sheet]["System Curve Head"], efficiancy= xl[sheet]["Efficiancy Percent"], \
                                             aor_flow = xl[sheet]["AOR Flow"].dropna(), aor_head = xl[sheet]["AOR Head"].dropna(), \
                                                 por_flow = xl[sheet]["POR Flow"].dropna(), por_head = xl[sheet]["POR Head"].dropna())
    
        
#%%
print(curve_dict["Sheet1"].pump_head)

#%%
fig,ax = plt.subplots()
for sheet in sheet_names:
    plt.plot(curve_dict[sheet].system_curve_flow, curve_dict[sheet].system_curve_head)
    plt.plot(curve_dict[sheet].pump_flow, curve_dict[sheet].pump_head)





#%% Graveyard of stuff that didnt work. RIP.


# print(xl["Sheet1"]["Speed (%)"][0])
# print(sheet_names)

# curve1 = Curve(speed = xl["Sheet1"]["Speed (%)"][0], pump_flow = xl["Sheet1"]["Pump Flow"], \
#                pump_head = xl["Sheet1"]["Pump Head"], system_curve_flow = xl["Sheet1"]["System Curve Flow"], \
#                    system_curve_head = xl["Sheet1"]["System Curve Head"], efficiancy= xl["Sheet1"]["Efficiancy Percent"], \
#                        aor_flow = xl["Sheet1"]["AOR Flow"].dropna(), aor_head = xl["Sheet1"]["AOR Head"].dropna(), \
#                            por_flow = xl["Sheet1"]["POR Flow"].dropna(), por_head = xl["Sheet1"]["POR Head"].dropna())

# curve1.curve_speed()
# curve1.curve_pump_flow()
# # curve1.curve_pump_head()
# # curve1.curve_system_flow()
# # curve1.curve_system_head()
# # curve1.curve_efficiancy()
# # curve1.curve_aor_flow()
# curve1.curve_aor_head()
# # curve1.curve_por_flow()
# # curve1.curve_por_head()


# # df = pd.concat(xl, keys = sheets,ignore_index = False, names = ["Sheet"]) #concat all sheets into one df
# # df = df.droplevel(level =1)

# # #%% get speeds
# # speeds = []  #speed curve values (100%, 90% etc) are held in this list
# # for sheet in sheets:
# #     speed = df.loc[sheet,0][0]
# #     speeds.append(speed)
# #     print(speeds)


        
# #%% Class testing
# # curve1 = Curve(speed = speed, pump_flow = pump_flow, pump_head = pump_head, system_curve_flow = system_flow, system_curve_head = system_head, efficiancy = efficiancy, \
# #                  aor_flow = aor_flow, aor_head = aor_head, por_flow = por_flow, por_head = por_head)

# # curve1.curve_efficiancy()

# #%%

# speeds = []
# pump_flows = []
# pump_heads = []
# system_flows = []
# system_heads = []
# efficiancies = []
# aor_flows = []
# aor_heads = []
# por_flows = []
# por_heads = []
# for sheet in sheets:
#     speed = df.loc[sheet]["Speed (%)"].dropna()
#     speeds.append(speed)
    
#     pump_flow = df.loc[sheet]["Pump Flow"]
#     pump_flows.append(pump_flow)
    
#     pump_head = df.loc[sheet]["Pump Head"]
#     pump_heads.append(pump_head)
    
#     system_head = df.loc[sheet]["System Curve Head"]
#     system_heads.append(system_head) 
    
#     system_flow = df.loc[sheet]["System Curve Flow"]
#     system_flows.append(system_flow)
    
#     efficiancy = df.loc[sheet]["Efficiancy Percent"]
#     efficiancies.append(efficiancy)
    
#     aor_flow = df.loc[sheet]["AOR Flow"]
#     aor_flow = aor_flow.replace(0,np.nan)
#     aor_flow.dropna(inplace = True)
#     aor_flows.append(aor_flow)
    
#     aor_head = df.loc[sheet]["AOR Head"]
#     aor_head = aor_head.replace(0,np.nan)
#     aor_head.dropna(inplace = True)
#     aor_heads.append(aor_head)
    
#     por_flow = df.loc[sheet]["POR Flow"]
#     por_flow = por_flow.replace(0,np.nan)
#     por_flow.dropna(inplace = True)
#     por_flows.append(por_flow)
    
#     por_head = df.loc[sheet]["POR Head"]
#     por_head = por_head.replace(0,np.nan)
#     por_head.dropna(inplace = True)
#     por_heads.append(por_head)
# #%% Create curve object for each sheet

# for i in range(0,len(sheets)):
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
