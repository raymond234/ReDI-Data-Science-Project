# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:09:21 2021

@author: hp
"""
import json
import pandas as pd

#Open the first JSON dataset
data = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0001-of-0010.json"))


#Decipher the structure of the data
print(len(data))
# 2


#Digging deeper into the branches
print(data.keys())
# dict_keys(['meta', 'results'])


#Dig into the "meta" key
print(len(data["meta"]))
# 5

print(data["meta"])
# Meta doesn't seem to contain much data. Meta contains general information
# about the dataset.


#Digging deeper into the "results" key
print(len(data["results"]))
# 20000
# "results" contain the main data


#Check out the first index in "results"
print(data["results"][0])


#Check out the number of keys in the first 5 indices of "results"
for i in range(5):
    print(len(data["results"][i]))
#24 36 23 35 23. Total = 141
# Each index has a different number of keys
        
       
# Check out the number of unique keys in the first 5 indices of "results
column_names = []    
for i in range(5):
    for j in (data["results"][i]):
        if j not in column_names:
            column_names.append(j)
print(len(column_names))
# 56 unique keys
# The
print(column_names)
 
       
#Check out how many keys the first 5 indices have in common
common_keys = list(set(data["results"][0]) & set(data["results"][1]) & 
   set(data["results"][2]) & set(data["results"][3]) & set(data["results"][4]))
common_keys
# Size = 9. Common suspects 
#spl_product_data_elements  indications_and_usage  dosage_and_administration

     
#Check out the keys in the first five indices in "results"
for i in range(5):
    print("\n")
    for j in data["results"][i]:
        print(j)
        
        
#Parse JSON string into a Pandas DataFrame
#We use pd.json_normalize because each entry has a different number of keys
df = pd.json_normalize(data["results"])
df

sample_df = df.head(20)
df_colnames = list(df.columns)
#df has 158 columns


#Open the second JSON dataset
data2 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0002-of-0010.json"))

#Sanity check the second dataset
print(len(data2))
print(data2.keys())
print(len(data2["meta"]))
print(len(data2["results"]))

#Parse second dataset into a dataframe
df2 = pd.json_normalize(data2["results"])
dfhead = df2.head()
df2_colnames = list(df2.columns)
#df2 has 161 columns

# Compare the columns in df and df2
common_keys2 = list(set(df_colnames) & set(df2_colnames))
# Both dataframes contain 154 common columns; therefore I think they are 
# majorly related

#Let's take a look at the different columns
diff = list(set(df_colnames) - set(common_keys2))
diff2 = list(set(df2_colnames) - set(common_keys2))

#Which columns differ from both?




#Append to original dataframe. We use concat because of the different 
#number of columns
df_main = pd.concat([df, df2], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)

#Open the third JSON dataset
data3 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0003-of-0010.json"))

#Sanity check the third dataset
print(len(data3))
print(data3.keys())
print(len(data3["meta"]))
print(len(data3["results"]))

#Parse third dataset into a dataframe
df3 = pd.json_normalize(data3["results"])
df3_colnames = list(df3.columns)
#df3 has 159 columns

# Compare the columns in df_main and df2
common_keys3 = list(set(df_main_colnames) & set(df3_colnames))
diff3 = list(set(df3_colnames) - set(common_keys3))
# Both dataframes contain 154 common columns; Weird new columns are still coming up 
# majorly related

#Append df3 to main
df_main = pd.concat([df_main, df3], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)



#Open the fourth JSON dataset
data4 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0004-of-0010.json"))

#Sanity check the fourth dataset
print(len(data4))
print(data4.keys())
print(len(data4["meta"]))
print(len(data4["results"]))

#Parse fourth dataset into a dataframe
df4 = pd.json_normalize(data4["results"])
df4_colnames = list(df4.columns)
#df4 has 163 columns

# Compare the columns in df_main and df4
common_keys4 = list(set(df_main_colnames) & set(df4_colnames))
# 161
diff4 = list(set(df4_colnames) - set(common_keys4))

#Append df4 to df_main
df_main = pd.concat([df_main, df4], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)



#Open the fifth JSON dataset
data5 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0005-of-0010.json"))

#Sanity check the fifth dataset
print(len(data5))
print(data5.keys())
print(len(data5["meta"]))
print(len(data5["results"]))

#Parse fifth dataset into a dataframe
df5 = pd.json_normalize(data5["results"])
df5_colnames = list(df5.columns)
#df5 has 163 columns

# Compare the columns in df_main and df5
common_keys5 = list(set(df_main_colnames) & set(df5_colnames))
# 160. 3 extra columns
diff5 = list(set(df5_colnames) - set(common_keys5))

#Append df5 to df_main
df_main = pd.concat([df_main, df5], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)
#174 columns now



#Open the sixth JSON dataset
data6 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0006-of-0010.json"))

#Sanity check the sixth dataset
print(len(data6))
print(data6.keys())
print(len(data6["meta"]))
print(len(data6["results"]))

#Parse sixth dataset into a dataframe
df6 = pd.json_normalize(data6["results"])
df6_colnames = list(df6.columns)
#df6 has 163 columns

# Compare the columns in df_main and df6
common_keys6 = list(set(df_main_colnames) & set(df6_colnames))
# 162. 1 extra column.
diff6 = list(set(df6_colnames) - set(common_keys6))

#Append df6 to df_main
df_main = pd.concat([df_main, df6], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)
#175 columns now



#Open the seventh JSON dataset
data7 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0007-of-0010.json"))

#Sanity check the seventh dataset
print(len(data7))
print(data7.keys())
print(len(data7["meta"]))
print(len(data7["results"]))

#Parse seventh dataset into a dataframe
df7 = pd.json_normalize(data7["results"])
df7_colnames = list(df7.columns)
#df7 has 159 columns

# Compare the columns in df_main and df7
common_keys7 = list(set(df_main_colnames) & set(df7_colnames))
# 158. 1 extra column.
diff7 = list(set(df7_colnames) - set(common_keys7))

#Append df7 to df_main
df_main = pd.concat([df_main, df7], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)
# 176 columns now



#Open the eighth JSON dataset
data8 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0008-of-0010.json"))

#Sanity check the eighth dataset
print(len(data8))
print(data8.keys())
print(len(data8["meta"]))
print(len(data8["results"]))

#Parse eighth dataset into a dataframe
df8 = pd.json_normalize(data8["results"])
df8_colnames = list(df8.columns)
#df8 has 160 columns

# Compare the columns in df_main and df8
common_keys8 = list(set(df_main_colnames) & set(df8_colnames))
# 159. 1 extra column.
diff8 = list(set(df8_colnames) - set(common_keys8))

#Append df8 to df_main
df_main = pd.concat([df_main, df8], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)
#177 columns now.



#Open the ninth JSON dataset
data9 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0009-of-0010.json"))

#Sanity check the ninth dataset
print(len(data9))
print(data9.keys())
print(len(data9["meta"]))
print(len(data9["results"]))

#Parse ninth dataset into a dataframe
df9 = pd.json_normalize(data9["results"])
df9_colnames = list(df9.columns)
#df9 has 156 columns

# Compare the columns in df_main and df9
common_keys9 = list(set(df_main_colnames) & set(df9_colnames))
# 155. 1 more column to dataframe
diff9 = list(set(df9_colnames) - set(common_keys9))

#Append df9 to df_main
df_main = pd.concat([df_main, df9], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)
#178 columns now



#Open the tenth JSON dataset
data10 = json.load(open("C:/Users/hp/Desktop/ReDI DataScience/ReDI Project/Drug Labelling/drug-label-0010-of-0010.json"))

#Sanity check the tenth dataset
print(len(data10))
print(data10.keys())
print(len(data10["meta"]))
print(len(data10["results"]))

#Parse tenth dataset into a dataframe
df10 = pd.json_normalize(data10["results"])
df10_colnames = list(df10.columns)
#df10 has 155 columns

# Compare the columns in df_main and df10
common_keys10 = list(set(df_main_colnames) & set(df10_colnames))
# 155. No new columns
diff10 = list(set(df10_colnames) - set(common_keys10))

#Append df10 to df_main
df_main = pd.concat([df_main, df10], axis=0, ignore_index=True)
df_main_colnames = list(df_main.columns)


df_main_head = df_main.head(20)
     

counts = df_main.isna().sum()
counts = counts.to_dict()
counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}
counts_full = list(counts)
counts = counts_full[0:51]
df_main = df_main[counts]
df_main = df_main.drop(["set_id", "id", "effective_time", "version"], axis=1)

df_main.to_csv("slimmed_df.csv", index=False)














