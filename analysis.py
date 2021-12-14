# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:12:40 2021
@author: hp
"""

import pandas as pd
import numpy as np
import re
from ast import literal_eval
from functools import reduce

# Import data 

df = pd.read_csv("C:/Users/hp\Desktop/ReDI DataScience/ReDI Project/slimmed_df.csv", dtype= str)
# Data about Clinical trial and sponsors from AACT.
other_df = pd.read_csv("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/sponsors.csv", dtype= str)

# Clean up data; Remove Brackets

col_names = list(df.columns)

# This column is sequestered from columns undergoing cleaning because 
# its data type is boolean and can't be evaluated by ast.literal_eval
col_names.remove("openfda.is_original_packager")

# Simple function to unpack the JSON Array/List into strings
def clean_data(df):
    for element in col_names:
# First you separate NaN values and cells containing values
        notnan = df[element].notnull()
        isnan = df[element].isnull()
        df_nan = df[isnan]
        df_notnan = df[notnan]
# Clean/Process cells containing values
        df_notnan[element] = df_notnan[element].apply(literal_eval).apply(', '.join)
# Merge both columns at the end...
        df = pd.concat([df_nan, df_notnan], axis=0, sort=True)        
# Sort again according to indices
        df.sort_index(inplace=True)
    return df
        
# Expensive process therefore export cleaned data
df2 = clean_data(df)
df2.to_csv("df.csv", index=False)

# Clean the boolean column
df2["openfda.is_original_packager"] = df2["openfda.is_original_packager"].apply(lambda x: bool(str(x)[0]))

#Small subset of data for viewing and manipulation purposes 
# as raw data is expensive to play around with
sample_df = df2.head(100)   


# Company with most registrations of drugs

#Problem: Original data about companies are not uniform; cannot be "grouped by" in a consistent way
#Solution: Simple function to get a column that contains unique company name for every company by 
#getting the first 2 words in a company name,after eliminating endings and special characters.

def get_company_endings(name):
    name = str(name)
# Eliminate special characters
    name = re.sub(r"[^a-zA-Z0-9]+", " ", name)
# Get endings and compare to endings that indicate company business forms
    ending = name.rsplit(None, 1)[-1].lower()
    endings_list = ["inc", "llc", "corporation", "co", "company", "pharmacy", "limited", "ltd", "pharmaceuticals", "corp", "corps", "holdings"]
    if ending in endings_list:
# Remove those endings that correspond to company forms
        name = re.sub(r"\b" + ending + "\b", "", name)
# Return the first words in a company's name-
        return ' '.join(name.split()[:2]).lower()
    else:
        return ' '.join(name.split()[:2]).lower()
    
# Column "aggregate_name" makes every company'sname uniform regardless of the 
# slight differences in how they were entered
df2["aggregate_name"] = df2["openfda.manufacturer_name"].apply(get_company_endings)

#Perform group by with aggregate names
most_registrations = df2.groupby(by= "aggregate_name").size().reset_index(name="counts").sort_values(by="counts", ascending=False).iloc[1:, :]

# Problem: Present data in a way that the formal name of a company is used to represent it.
# Solution: Aggregate the diferent presentations of a company's name and use one of the as the 
# formal name with which to present the results.
fda_name_df = pd.DataFrame(df2.loc[:,[ "openfda.manufacturer_name", "aggregate_name"]])
fda_name_df = fda_name_df.groupby("aggregate_name")["openfda.manufacturer_name"].apply(list).reset_index(name="Component List")
fda_name_df["Formal Name"] = fda_name_df["Component List"].apply(lambda x: x[0])

# Result presentations.
most_registrations = most_registrations.merge(fda_name_df, how="left", on="aggregate_name").drop(columns="Component List")
# A prepacking company/Generics brand called Bryant Ranch has submitted the most appications to register new drugs

#What proportion of entries correspond to each product type?
product_type = df2.groupby(by= "openfda.product_type").size().reset_index(name="counts").sort_values(by="counts", ascending=False)
product_type["%"] = product_type["counts"].apply(lambda x: 100 * x / float(product_type["counts"].sum()))

#Result: 65.57% of the drugs registered are Human OTC drugs; 34.43% are Human Prescription drugs.
# In Germany, the percentage of Human Precription drugs will certainly be higher



# Companies that have carried out the most clinical trials 

#First: Find evidence that a company has carried out clinical trials. Find NCTID in dataset

# A RegEx function to search for unique NCT IDs in the clinical studies column
def find_clinical_trial(name):
    name = str(name)
    matches = re.findall(r'(NCT\w{8})|(\d{8})', name)
    empty_list = []
    match_list = [match[0] + match[1] for match in matches]
    return ', '.join(match_list)
    
# Application of function
sample_df["NCTID"] = sample_df["clinical_studies"].apply(find_clinical_trial)
df2["NCTID"] = df2["clinical_studies"].apply(find_clinical_trial)


# Get rows containing values of NCT ID
df2["NCTID"] = pd.DataFrame(df2["NCTID"].replace("", np.nan))
df3 = df2.dropna(subset=["NCTID"])
mini_df3 = df3.head(10)
# Reduce dimension for df3
df4 = df3.loc[:, ["spl_product_data_elements", "active_ingredient", 
                  "openfda.brand_name", "openfda.generic_name", "openfda.manufacturer_name", 
                  "openfda.product_type", "openfda.route", "openfda.substance_name", "aggregate_name", "NCTID"]]

mini_df4 = df4.head(20)
# Result: A paltry 1010 of the entire data contains evidence of clinical data. 
# Less than 1% of the entire data

# Separate the rows that have null values for "openfda.manufacturer_name".
isnan = df4["openfda.manufacturer_name"].isnull()
df4_nan = df4[isnan]
# left for future cleaning. Join with sponsors table at NCTID and fill in the sponsors as Manufacturers


# Group by aggregate name and melt all groups into one and count length of list
notnan = df4["openfda.manufacturer_name"].notnull()
df4_notnan = df4[notnan]


#Group by and compile every NCTID associated with each company into a component 
# list column and find the lenght of that list


clinical_trial_df = df4_notnan.groupby("aggregate_name")["NCTID"].apply(list).reset_index(name="Component List")
clinical_trial_df["Counts"] = clinical_trial_df["Component List"].apply(lambda x: len(list(set(set(x)))))
clinical_trial_df["%"] = clinical_trial_df["Counts"].apply(lambda x: 100 * x / float(clinical_trial_df["Counts"].sum()))
clinical_trial_df = clinical_trial_df.merge(fda_name_df, how="left", on="aggregate_name").drop(columns=["Component List_y"], axis=1)


clinical_trial_df["Counts"].sum() # Returns total of unique clinical trials = 821
# A prepack/generics company topped the list which is highly unusual. A quick check on Google 
# showed that many of the clinical trials carried out by the company was sponsored by J&J. Disregard 
# the importance of openfda.manufacturers_name and merge the entire data with NCTID(use df4); fill in missing "NCT" prefixes and join with AACT data


#Sanity proof result by joining dataframe with sponsors table and repeating the analyses
df3["NCTID"] = df3["NCTID"].apply(lambda x: str(x).split(', '))
mini_df3 = df3.head(10)
df5 = df3.loc[:, ["aggregate_name", "NCTID"]].explode("NCTID") #3380


df5 = df5.merge(fda_name_df, how="left", on = "aggregate_name")
    
df5["NCTID"] = df5["NCTID"].apply(lambda x: x if "NCT" in str(x) else "NCT" + x)

df5["check"] = df5["NCTID"].apply(lambda x: True if "NCT" in str(x) else False)
df5[df5["check"] == False].sum()
df5 = df5.drop_duplicates(subset=["NCTID"])  #1363 unique NCT IDs



df5 = df5.rename({"NCTID": "nct_id"}, axis=1)
mini_df5 = df5.head(20)

merged_aact = df5.merge(other_df, how="left", on="nct_id").drop(columns=["Component List", "check", "id"], axis=1)
#Dataframe returned with more rows than 1363. Returned 1623 rows. Investigate.

duplicates = merged_aact.duplicated(subset=["nct_id"], keep=False) #Keep first marks only subsequent occurrences after the first one as True and correctly returned
#260 rows. I will select keep=False to return every duplicated entry and analyse it
 
merged_duplicates = merged_aact[duplicates]
 
# Result: Data showed that for many of the clinical trials; there is a lead company and there is a collaborator company
# The Lead company is often the developer/owner/manufacturer of the product but other times both the lead, collaborator and 
# manufacturer are different companies. What could this mean? Is it about a complex web of ownership of IP and licensing that 
# means that different companies are involved in the development of a drug product, especially Biotech products.
# Open for future research.


#Moving on. Null values.
isnan = merged_aact["name"].isnull()
nctid_na = merged_aact[isnan]

# Analysis of the first 2 shows that even though the drugs were manufactured by Gilead. The collaborators include Bill/Melinda Gates 
# Foundation. Interesting insight! I have to bring the data for other organizations that are not Pharma companies.




merged_mini = merged_aact.head(25)



clin_trials_list = []
clin_trials_list.extend(df3["NCTID"].tolist()) #len(list) is 1010; 

clin_trials_list = [element for sublist in clin_trials_list for element in sublist] #Flattened to 3380.

unique_trials = list(set(clin_trials_list)) #1372


#def clinical_data():
#    for element in col_names:
#        df["NCTID"] = df[element].apply(find_clinical_trial)       
#df4 = df


# Find the active ingredient most represented in the data

#Problem: Prepare column/ingredients in a way that it makes it easy for it to be analysed.
# First: Split the ingredient "string" into a list
df2["ingredient_list"] = df2["openfda.substance_name"].apply(lambda x: sorted(str(x).replace(' /', ",").replace(" AND", ",").split(', ')))
sample_df = df2.head(100) 

# Second: Append this column into a flat list contains every element from every row.
ingredient_list = []
ingredient_list.extend(df2["ingredient_list"].tolist()) # Returns a list of 
# lists with size 193589 (same as no of rows of dataframe)

#Sanity check data. Find the final size/length of flattened list and compare after flattening
final_size = sum([len(x) for x in ingredient_list]) # Result = 271303

#Flatten list
ingredient_list = [element for sublist in ingredient_list for element in sublist] #Also = 271303


# Third: Perform calculations and percentages on every unique value in the list.
# Find unique entries
ingredients = sorted(list(set(ingredient_list))) #  5235 ingredients. 
#On inspection, some of the large organic molecules were affected by my split 
#and replace, For this analysis, I will ignore that, I have ideas about how to better 
# do the replace and split to preserve their integrity

#Calculate counts. Using a dictionary.
ingredients_count = {key: ingredient_list.count(key) for key in ingredients}

ingredients_df = pd.DataFrame.from_dict(ingredients_count, orient='index', columns=["Counts"])
ingredients_df = ingredients_df.reset_index().rename(columns={"index": "Ingredients"}).sort_values(by=["Counts"], ascending=False)
ingredients_df = ingredients_df.iloc[1:, :]
ingredients_df["%"] = ingredients_df["Counts"].apply(lambda x: round(100 * x / float(ingredients_df["Counts"].sum()), 3))

# Interesting insights: Alcohol is the most common ingredients. I wonder what 
# type of products contain all these alcohol













        