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
import seaborn as sns
import math

sns.set_theme(style="darkgrid")


#%% importing data

os.chdir(
    r"C:\Users\JM070903\OneDrive - Jacobs\Documents\NWLWWTP\WSP Comment Responses\Pump Curves\Small Pump"
)  # move to directory
xl = pd.read_excel(
    r"Small Pump MinFlow Fathom_Output.xlsx", sheet_name=None
)  # import excel file
sheet_names = xl.keys()
sheet_names = list(sheet_names)

#%% Create pump curve class


class Curve:
    def __init__(
        self,
        speed=None,
        pump_flow=None,
        pump_head=None,
        system_curve_flow=None,
        system_curve_head=None,
        efficiancy=None,
        aor_flow=None,
        aor_head=None,
        por_flow=None,
        por_head=None,
        npsha_head=None,
        npshr_flow=None,
        npshr_head=None,
        intersection_head=None,
        intersection_flow=None,
    ):
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
        self.npsha_head = npsha_head
        self.npshr_flow = npshr_flow
        self.npshr_head = npshr_head
        self.intersection_flow = intersection_flow
        self.intersection_head = intersection_head

    def curve_speed(self):
        print("Speed is: \n" + str(self.speed))

    def curve_pump_flow(self):
        print("pump flow is: \n" + str(self.pump_flow))

    def curve_pump_head(self):
        print("pump head is: \n" + str(self.pump_head))

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

    def curve_npsha_head(self):
        print("NPSHA Head is: \n" + str(self.npsha_head))

    def curve_npshr_flow(self):
        print("NPSHR Flow is: \n" + str(self.npshr_flow))

    def curve_npshr_head(self):
        print("NPSHR Head is: \n" + str(self.npshr_head))

    def curve_intersection(self):
        print(
            f"Intersection point is: Flow: {self.intersection_flow}, Head: {self.intersection_head}"
        )


#%% NPSHA Caclulation
p_atm = 10.3  # default (metres) - assuming sea level
p_vap = 0.125  # assuming water at 10C. Lookup other values in steam table if reqd
pipe_area = ((math.pi * (xl["Sheet1"]["Suction Pipe Diameter"][0] ** 2))) / 4
suction_head_static = (
    xl["Sheet1"]["Inlet Resevoir Level"][0]
    - xl["Sheet1"]["NPSH Elevation Reference"][0]
)
suction_velocity = (0.001 * xl["Sheet1"]["Pump Flow"]) / pipe_area

suction_losses = (
    xl["Sheet1"]["Pipe Friction Factor"][0]
    * xl["Sheet1"]["Suction Pipe Length"][0]
    / xl["Sheet1"]["Suction Pipe Diameter"][0]
) * (
    (suction_velocity ** 2) / (2 * 9.81)
)  # uses the pipe friction factor to calculate friction losses in suction pipe

for sheet in sheet_names:
    xl[sheet]["NPSHA"] = (
        p_atm + suction_head_static - suction_losses - p_vap
    )  # NPSHA calc.Same for every sheet, does not update with different pump speeds. \
    # See https://www.youtube.com/watch?v=VlHgxwZBe1A for calc example. Does not account for mionor velocity losses

#%% Remove AOR and POR Zeros

for sheet in sheet_names:
    xl[sheet]["AOR Flow"] = xl[sheet]["AOR Flow"].replace(0, np.nan)
    xl[sheet]["AOR Head"] = xl[sheet]["AOR Head"].replace(0, np.nan)
    xl[sheet]["POR Flow"] = xl[sheet]["POR Flow"].replace(0, np.nan)
    xl[sheet]["POR Head"] = xl[sheet]["POR Head"].replace(0, np.nan)


#%% getting intersections
for sheet in sheet_names:
    xl[sheet]["Pump_System Head Diff"] = (
        xl[sheet]["Pump Head"] - xl[sheet]["System Curve Head"]
    ).abs()
    # create a new column in each sheet with the difference between pump and system head
    head_diff_min = xl[sheet]["Pump_System Head Diff"].min()
    head_diff_min_index = np.where(
        (xl[sheet]["Pump_System Head Diff"] == head_diff_min) == True
    )[0].astype(int)
    xl[sheet]["intersection_flow"] = xl[sheet]["Pump Flow"][head_diff_min_index]
    xl[sheet]["intersection_head"] = xl[sheet]["Pump Head"][head_diff_min_index]

#%%
curve_dict = {}  # create empty dict to hold sheet info
for i in range(0, len(xl)):
    curve_dict[
        "Sheet%s" % i
    ] = {}  # create a new dict key for each sheet, Sheet1, sheet2, sheet3 etc

for (
    sheet
) in (
    sheet_names
):  # create classes for each sheet and store them in the ditionary previously created
    curve_dict[sheet] = Curve(
        speed=xl[sheet]["Speed (%)"][0],
        pump_flow=xl[sheet]["Pump Flow"],
        pump_head=xl[sheet]["Pump Head"],
        system_curve_flow=xl[sheet]["System Curve Flow"],
        system_curve_head=xl[sheet]["System Curve Head"],
        efficiancy=xl[sheet]["Efficiancy Percent"],
        aor_flow=xl[sheet]["AOR Flow"].dropna(),
        aor_head=xl[sheet]["AOR Head"].dropna(),
        por_flow=xl[sheet]["POR Flow"].dropna(),
        por_head=xl[sheet]["POR Head"].dropna(),
        npsha_head=xl[sheet]["NPSHA"],
        npshr_flow=xl[sheet]["NPSHR Flow"],
        npshr_head=xl[sheet]["NPSHR Head"],
        intersection_flow=xl[sheet]["intersection_flow"].dropna(),
        intersection_head=xl[sheet]["intersection_head"].dropna(),
    )

#%%

""" 
To access the Curve functions you have to call the functions from within the curve dictionary e.g:                                                          
curve_dict["Sheet1"].curve_intersection()   
curve_dict["Sheet1"].curve_intersection()     
curve_dict["Sheet1"].curve_npshr_head()                                             
"""

#%%
graph_title = "Small Pump Min Flow"
letter_portrait = (6.7, 3.5)
letter_landscape = (5, 9)
tabloid_portrait = (9, 4.75)
tabloid_landscape = (15, 7.4)
seaborn_background_color = [0.234, 0.234, 0.242]

x_axis_limit = xl["Sheet1"]["Pump Flow"].max()


fig, ax = plt.subplots(figsize=letter_portrait)
system_curve_min = sns.lineplot(
    x=curve_dict["Sheet1"].system_curve_flow,
    y=curve_dict["Sheet1"].system_curve_head,
    ax=ax,
    label="System Curve Min",
    linestyle="dashed",
    zorder=3,
)  # This assumes 100% speed is on sheet1, if not the system curve may not intersect your highest pump speed
system_curve_max = sns.lineplot(
    x=curve_dict["Sheet4"].system_curve_flow,
    y=curve_dict["Sheet4"].system_curve_head,
    ax=ax,
    label="System Curve Max",
    linestyle="dashed",
    zorder=3,
)

npshr_curve = sns.lineplot(
    x=curve_dict["Sheet1"].npshr_flow,
    y=curve_dict["Sheet1"].npshr_head,
    ax=ax,
    label="NPSHr",
    linestyle="dashdot",
)
npsha_curve = sns.lineplot(
    x=curve_dict["Sheet1"].pump_flow,
    y=curve_dict["Sheet1"].npsha_head,
    ax=ax,
    label="NPSHa",
    linestyle="dashdot",
)


for sheet in sheet_names:
    pump_curve = sns.lineplot(
        x=curve_dict[sheet].pump_flow,
        y=curve_dict[sheet].pump_head,
        ax=ax,
        label=f"{curve_dict[sheet].speed} % Speed",
    )
    aor_plot = sns.scatterplot(
        x=curve_dict[sheet].aor_flow,
        y=curve_dict[sheet].aor_head,
        color="k",
        ax=ax,
        label="AOR" if sheet == "Sheet1" else "",
        zorder=3,
    )
    por_plot = sns.scatterplot(
        x=curve_dict[sheet].por_flow,
        y=curve_dict[sheet].por_head,
        color="g",
        ax=ax,
        label="POR" if sheet == "Sheet1" else "",
        zorder=3,
    )
    # intersection_plot = sns.scatterplot(x = curve_dict[sheet].intersection_flow, y = curve_dict[sheet].intersection_head, ax = ax, \
    #                                     zorder = 3, color = "r", label = "Intersection Points" if sheet =="Sheet1" else "", \
    #                                         s = 100, marker = "^")
#     intersection_callouts = ax.text\
#         (x = (x_axis_limit - x_axis_limit*0.12), \
#           y = (curve_dict[sheet].pump_head.max() - curve_dict[sheet].pump_head.max()/10),\
#             s = f'({xl[sheet]["intersection_flow"].max().round(1)} , {xl[sheet]["intersection_head"].max().round(1)})')

# duty_point_text = ax.text(x = (x_axis_limit - x_axis_limit*0.12), \
#                           y = (curve_dict["Sheet1"].pump_head.max() - curve_dict[sheet].pump_head.max()/20), \
#                           s = "Duty Points:")

sns.set_palette("deep")
ax.set_xlabel("Flow (L/s)")
ax.set_ylabel("Head (m)")
ax.legend(
    loc="lower center", bbox_to_anchor=(0.5, -0.5), ncol=3
)  # This is set for letter_portrait figsize, might need adjusting for others
ax.set_title(graph_title)
ax.set_xlim(
    left=0, right=(x_axis_limit + x_axis_limit * 0.1)
)  # extending the x acis to 10% more than the max flow as a buffer
plt.show()

# ax1 = plt.twinx()
# sns.lineplot( x = curve_dict["Sheet1"].system_curve_flow, y = curve_dict["Sheet1"].efficiancy, ax = ax1)

fig.savefig("Small Pump Min Flow.jpg", dpi=1200, bbox_inches="tight")
print("System and Pump Curves.jpg' saved in current directory")


#%% Graveyard of stuff that didnt work. RIP.

# Finding intersections - single intersection prior to looping

# xl["Sheet1"]["Pump_System Head Diff"] = (xl["Sheet1"]["Pump Head"] - xl["Sheet1"]["System Curve Head"]).abs()
# head_diff_min = xl["Sheet1"]["Pump_System Head Diff"].min()

# head_diff_min_index = np.where((xl["Sheet1"]["Pump_System Head Diff"] == head_diff_min) ==True)[0].astype(int)

# intersection1_flow = xl["Sheet1"]["Pump Flow"][head_diff_min_index]
# intersection1_head = xl["Sheet1"]["Pump Head"][head_diff_min_index]

# print(intersection1_flow)

# sns.scatterplot(x = intersection1_flow, y = intersection1_head)

# intersections = {}
# head_diff_min = {}
# head_diff_min_index = {}
# sheet_range = list(range(0,len(xl)))
# for i in sheet_range:
#     intersections["Intersection%s" %i] = {}

# for sheet in sheet_names:
#     xl[sheet]["Pump_System Head Diff"] = (xl[sheet]["Pump Head"] - xl[sheet]["System Curve Head"]).abs()
#     head_diff_min[sheet] = xl[sheet]["Pump_System Head Diff"].min()
#     head_diff_min_index[sheet] = np.where((xl[sheet]["Pump_System Head Diff"] == head_diff_min) ==True)[0].astype(int)
#     intersection_flow[sheet] = xl[sheet]["Pump Flow"][head_diff_min_index]

#     print(inter_section_flow[sheet])
# #%%
# print(curve_dict["Sheet1"].pump_head)
# print(curve_dict["Sheet2"].speed)


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
