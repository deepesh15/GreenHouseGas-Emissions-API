import uuid        #for generating unique ids
import pandas as pd
import sqlite3
import  csv

#open csv for cleaning and renaming categories
df = pd.read_csv('greenhouse_gas.csv')
# get a set of countries and categories
countries = set(df.country_or_area)
categories = set(df.category)

# use uuid to generate a unique id for a country and category and store it csv
countries_dic = {}
categories_dic = {}
for country in countries:
    countries_dic[country] = uuid.uuid4().hex[:8]
for category in categories:
    categories_dic[category] = uuid.uuid4().hex[:8]

# create two new columns country_id and category_id
df.insert(0, "country_id", "", True)
df.insert(4, "category_id", "", True)

# insert ids in their  respective columns
for i in range(len(df)):
    df['country_id'][i] = countries_dic[(df['country_or_area'][i])]
    df['category_id'][i] = categories_dic[(df['category'][i])]

# the categories are a bit to big and difficult to work
# so replace them with short and easy to understand strings

rename_category = {'carbon_dioxide_co2_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent' :' CO2',
                  'methane_ch4_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent' :' CH4',
                  'nitrogen_trifluoride_nf3_emissions_in_kilotonne_co2_equivalent' :' NF3',
                  'greenhouse_gas_ghgs_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent' :' GHG',
                  'nitrous_oxide_n2o_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent' :' N20',
                  'unspecified_mix_of_hydrofluorocarbons_hfcs_and_perfluorocarbons_pfcs_emissions_in_kilotonne_co2_equivalent' :' HFC(unspecified)',
                  'hydrofluorocarbons_hfcs_emissions_in_kilotonne_co2_equivalent' :' HFC',
                  'sulphur_hexafluoride_sf6_emissions_in_kilotonne_co2_equivalent' :' SF6',
                  'greenhouse_gas_ghgs_emissions_including_indirect_co2_without_lulucf_in_kilotonne_co2_equivalent' :' GHG(indirect)',
                  'perfluorocarbons_pfcs_emissions_in_kilotonne_co2_equivalent' :' PFC',
                  }

for i in df.index:
    temp = rename_category[df.at[i,"category"]]
    df.at[i,"category"] = temp

#use temp.csv to create data.db
df.to_csv('temp.csv', index=False)

#use the edited csv file to create database and create the table 
connection = sqlite3.connect("data.db")
cur = connection.cursor()
cur.execute("CREATE TABLE data ('country_id' VARCHAR,'country' VARCHAR,'year' INTEGER,'value' DOUBLE,'category_id' VARCHAR,'category' )")
file_csv = open("temp.csv")
rows = csv.reader(file_csv)

#using the edited csv add the data into database
cur.executemany("INSERT INTO data VALUES (?,?,?,?,?,?)",rows)

connection.commit()
connection.close()
