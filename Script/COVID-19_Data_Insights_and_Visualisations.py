# -*- coding: utf-8 -*-
"""
Created on Thu May  2 19:02:16 2024

@author: keneo
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import the confirmedcases dataset
confirmed_cases = pd.read_excel(r"C:\Users\keneo\Downloads\Project Dataset\OxCGRT_summary.xlsx",
                                sheet_name = "confirmedcases")

# Import the confirmeddeaths dataset
confirmed_deaths = pd.read_excel(r"C:\Users\keneo\Downloads\Project Dataset\OxCGRT_summary.xlsx", 
                                 sheet_name = "confirmeddeaths")

# Import the stringencyindex dataset
stringency_index = pd.read_excel(r"C:\Users\keneo\Downloads\Project Dataset\OxCGRT_summary.xlsx", 
                                 sheet_name = "stringencyindex")

# Find the missing values in each dataset
confirmed_cases_missing = confirmed_cases.isnull().sum()
confirmed_deaths_missing = confirmed_deaths.isnull().sum()
stringency_index_missing = stringency_index.isnull().sum()

# Fill the missing values in confirmedcases dataset with zeros
# JUSTIFICATION:
# The whole of the Turkmenistan row (ROW 166) has missing values. I filled this row with zeros.
# I acknowledge that this means Turkmenistan had zero cases of COVID during the time period stated
# in the dataset, which could be wrong, but with no value in the entire row, there are only two 
# logical ways to handle it, which are to drop the entire row or to fill it with zeros. To justify why 
# I filled it with zeros, this is because I want to capture the data for all countries stated in 
# the dataset.
confirmed_cases = confirmed_cases.fillna(0)

# Replace the inconsistent values in the France row (ROW 58) with numbers generated between 63588 and 107712
# JUSTIFICATION:
# This is because it is noticed in the dataset that France has a high number of COVID cases 
# and a constant increase daily, and the values for eight days in France have a decrease, which 
# indicates an error in data collection. Therefore, instead of dropping the column, it makes 
# more sense to fill the cells that have inconsistent values with increasing numbers between
# the two neighboring cells with consistent values.

# Generate numbers between 63588 and 107712
print(np.linspace(63588, 107712, 10).round())

# Use the generated numbers to replace the inconsistent values
confirmed_cases.loc[58] = confirmed_cases.loc[58].replace({46483: 68491, 
                                                           47299: 73393, 
                                                           49934: 78296, 
                                                           46400: 83199,
                                                           50242: 88101,
                                                           54003: 93004,
                                                           55538: 97907,
                                                           56972: 102809})

# Fill the missing values in confirmeddeaths dataset with zeros
# JUSTIFICATION:
# The whole of the Turkmenistan row (ROW 166) has missing values. I filled this row with zeros.
# Since it is the same country with missing values in the confirmedcases dataset, the reason I
# filled the missing row with zeros is the same reason I filled the confirmedcases dataset with
# zeros, which is stated above.
confirmed_deaths = confirmed_deaths.fillna(0)

# Fill the missing values in stringencyindex dataset with the neighboring values
# JUSTIFICATION:
# (i.) Columns "05May2020", "06May2020", and "07May2020" were filled with "69.44" because 
# "69.44" is the value in the column before and after the columns with missing values.

# (ii.) Columns "08May2020", "09May2020", and "10May2020" were filled with "75" because
# "75" is the value in the column before the columns with missing values.
stringency_index[["05May2020", "06May2020", "07May2020"]] = stringency_index[["05May2020", "06May2020", "07May2020"]].fillna(69.44)
stringency_index[["08May2020", "09May2020", "10May2020"]] = stringency_index[["08May2020", "09May2020", "10May2020"]].fillna(75)

# Fill the rest of the missing values with zeros
# JUSTIFICATION:
# I filled them with zeros for the same reason above in the confirmed cases and confirmed deaths 
# datasets which is to capture all the data in the datasets.
stringency_index = stringency_index.fillna(0)






# Get all the cases between 20th March 2020 and 10th April 2020
march_april_cases = confirmed_cases.loc[:, "20Mar2020":"10Apr2020"]

# Get the difference between each case and put in a dataframe
new_confirmed_cases = pd.DataFrame(march_april_cases.diff(axis = 1))

# Add the country_name to the new dataframe
new_confirmed_cases.insert(0, "country_name", confirmed_cases["country_name"])

# Fill the index date with zero
new_confirmed_cases["20Mar2020"] = new_confirmed_cases["20Mar2020"].fillna(0)






# Add the total cases confirmed on 10 April 2020 to the new confirmed cases dataframe
new_confirmed_cases["total_cases"] = confirmed_cases["10Apr2020"]

# Arranged the descending order based on the total_cases
new_confirmed_cases = new_confirmed_cases.sort_values(by = "total_cases", ascending = False)

# Get the top 10 countries with the highest total_cases
top_10_new_confirmed_cases = new_confirmed_cases.iloc[:10, :]

# Drop the country_name and total_cases columns to feed the data into the heatmap
heat_map_data = top_10_new_confirmed_cases.drop(columns = ["country_name", "total_cases"])

# Plot the heatmap
plt.figure(figsize = (15, 10))
heatmap = sns.heatmap(heat_map_data, cmap = sns.color_palette("YlOrRd", as_cmap = True), 
                      linewidths = .1, yticklabels = top_10_new_confirmed_cases["country_name"],
                      cbar_kws = {"orientation": "horizontal", "pad": 0.05, "aspect": 60})
plt.title("TOP 10 COUNTRIES WITH THE HIGHEST COVID-19 CASES ON 10TH APRIL 2020")
heatmap.tick_params(axis = "x", labelrotation = 40, top = True, labeltop = True, 
                    bottom = False, labelbottom = False)

# Add the total_cases on the right side
for a, total_case in enumerate(top_10_new_confirmed_cases["total_cases"]):
    plt.text(23, a + 0.5, f"{int(total_case):,}", ha = "center", va = "center")

# Add a title above the total_cases on the right side
plt.text(23, -0.5, "Total", ha = "center", va = "center", fontsize = 15)
plt.show()






############################ CALCULATION FOR TOTAL DAILY CONFIRMED CASES ##########################
# Insert the 10May2020 column and country_name column from confirmed_cases into an new dataframe
total_cases = pd.DataFrame({"country_name": confirmed_cases["country_name"],
                            "total_cases": confirmed_cases["10May2020"]})

# Get the total cases for only United States
total_cases_US = total_cases.loc[[177]].values[0][1]

# Get the total cases for the other countries
total_cases_others = total_cases.drop(index = 177).iloc[:, 1].sum()

# Insert the two total cases into a dataframe
total_cases_US_Others = pd.DataFrame({"country_name": ["United States", "Rest of the World"],
                                      "total_cases": [total_cases_US, total_cases_others]})

############################ CALCULATION FOR TOTAL DAILY CONFIRMED DEATHS ##########################
# Insert the 10May2020 column and country_name column from confirmed_deaths into an new dataframe
total_deaths = pd.DataFrame({"country_name": confirmed_deaths["country_name"],
                             "total_cases": confirmed_deaths["10May2020"]})

# Get the total deaths for only United States
total_deaths_US = total_deaths.loc[[177]].values[0][1]

# Get the total deaths for the other countries
total_deaths_others = total_deaths.drop(index = 177).iloc[:, 1].sum()

# Insert the two total deaths into a dataframe
total_deaths_US_Others = pd.DataFrame({"country_name": ["United States", "Rest of the World"],
                                      "total_deaths": [total_deaths_US, total_deaths_others]})

# Create a dataframe to store the population of US vs Rest of the World
population = pd.DataFrame({"country_name": ["United States", "Rest of the World"],
                           "total_population": [328000000, 7800000000]})


# Plot the piechart
plt.figure(figsize = (15, 10))
plt.suptitle("US COVID-19 VS Rest of the World", fontsize = "xx-large")

# Population piechart
plt.subplot(1, 3, 1)
plt.title("Population")
piechart_1 = plt.pie(data = population, x = "total_population", 
                     colors = ["RoyalBlue", "DarkOrange"], 
                     autopct = lambda p: f"{p:.0f}%" if p > 10 else None, counterclock = False, 
                     startangle = 90, textprops = {"fontsize": 12}, wedgeprops = {"edgecolor":"white"})

# Add a line from the United States pie chart slice
plt.annotate("United States \n 4%", xy = (piechart_1[0][0].get_path().vertices[1]), xytext = (0.5, 1), 
             arrowprops = dict(arrowstyle = "-"), fontsize = 12)

# Add total_population below the population piechart
for a, populations in enumerate(population["total_population"]):
    plt.text(0, -1.5 - a * 0.1, f"{populations:,}", ha = "center", va = "center", fontsize = 12)

# Add the Rest of the World label
plt.text(0, -0.3, "Rest of the World", ha = "center", va = "center", fontsize = 12)

# Confirmed cases piechart
plt.subplot(1, 3, 2)
plt.title("Confirmed Cases")
piechart_2 = plt.pie(data = total_cases_US_Others, x = "total_cases", 
                     colors = ["RoyalBlue", "DarkOrange"], 
                     autopct = lambda p: f"{p:.1f}%" if p < 50 else None, counterclock = False,
                     startangle = 90, textprops = {"fontsize": 12}, wedgeprops = {"edgecolor":"white"})

# Add total_cases below the confirmed cases piechart
for a, total_case in enumerate(total_cases_US_Others["total_cases"]):
    plt.text(0, -1.5 - a * 0.1, f"{int(total_case):,}", ha = "center", va = "center", fontsize = 12)

# Confirmed deaths piechart
plt.subplot(1, 3, 3)
plt.title("Confirmed Deaths")
piechart_3 = plt.pie(data = total_deaths_US_Others, x = "total_deaths", 
                     colors = ["RoyalBlue", "DarkOrange"], 
                     autopct = lambda p: f"{p:.1f}%" if p < 50 else None, counterclock = False,
                     startangle = 90, textprops = {"fontsize": 12}, wedgeprops = {"edgecolor":"white"})

# Add total_deaths below the confirmed deaths piechart
for a, total_death in enumerate(total_deaths_US_Others["total_deaths"]):
    plt.text(0, -1.5 - a * 0.1, f"{int(total_death):,}", ha = "center", va = "center", fontsize = 12)

plt.tight_layout()
plt.show()






# Filter the confirmed_cases by 04May2020
filtered_cases = confirmed_cases[confirmed_cases["04May2020"] > 1000]

# Insert the country_name and 04May2020 column from the filtered confirmed_cases in a dataframe
filtered_04May2020_cases = pd.DataFrame({"country_name": filtered_cases["country_name"],
                                         "04May2020_cases": filtered_cases["04May2020"]})

# Insert the country_name and 04May2020 confirmed_deaths in a dataframe
filtered_04May2020_deaths = pd.DataFrame({"country_name": confirmed_deaths["country_name"],
                                          "04May2020_deaths": confirmed_deaths["04May2020"]})

# Insert the country_name and 04May2020 stringency_index in a dataframe
filtered_04May2020_stringency = pd.DataFrame({"country_name": stringency_index["country_name"],
                                              "04May2020_stringency": stringency_index["04May2020"]})

# Merge the filtered 04May2020 confirmed_cases and the filtered 04May2020 confirmed_deaths
cases_deaths = filtered_04May2020_cases.merge(filtered_04May2020_deaths, how = "left", 
                                              on = "country_name")

# Merge the combined cases and deaths with the filtered 04May2020 stringency_index
cases_deaths_stringency = cases_deaths.merge(filtered_04May2020_stringency, how = "left", 
                                             on = "country_name")


# Plot the scatterplot
plt.figure(figsize = (15, 10))
plt.scatter(data = cases_deaths_stringency, x = "04May2020_cases", y = "04May2020_stringency", 
            s = cases_deaths_stringency["04May2020_deaths"]/10, alpha = 0.5, color = "red")

plt.title("Correlation between the number of COVID-19 cases on 4th May 2020 and the stringency index")
plt.xscale("log")
plt.xlabel("Confirmed Cases")
plt.ylabel("Stringency Index")
plt.show()










