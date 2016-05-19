# -*- coding: utf-8 -*-
"""
Created on Tue May 17 20:53:48 2016

@author: Chris
"""
import pandas
import numpy

#bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)

#data here will act as the data frame containing the Mars crater data
data = pandas.read_csv('marscrater_pds.csv', low_memory=False)

#convert the latitude and diameter columns so that data is display as numeric
data['LATITUDE_CIRCLE_IMAGE'] = data['LATITUDE_CIRCLE_IMAGE'].convert_objects(convert_numeric=True)
data['DIAM_CIRCLE_IMAGE'] = data['DIAM_CIRCLE_IMAGE'].convert_objects(convert_numeric=True)

#debug print code for looking at the dimensions of the data
print(len(data))
print(len(data.columns))

#record the total number of observations performed for normalizing data later
totalobservations = len(data)

print('This table shows the frequency of craters by latitude.')
c1 = data.groupby('LATITUDE_CIRCLE_IMAGE').size()

print('This table shows the distribution by % of craters by latitude.')
p1 = data.groupby('LATITUDE_CIRCLE_IMAGE').size() * 100 / totalobservations

print('This table shows the frequency of craters by diameter.')
c2 = data.groupby('DIAM_CIRCLE_IMAGE').size()

print('This table shows the distribution by % of craters by diameter.')
p2 = data.groupby('DIAM_CIRCLE_IMAGE').size() * 100 / totalobservations

print('This table shows the frequency of the Ejecta morphology as determined by the shape of the ejecta.')
c3 = data.groupby('MORPHOLOGY_EJECTA_1').size()

print('This table shows the frequency of Ejecta morphology by % of craters.')
p3 = data.groupby('MORPHOLOGY_EJECTA_1').size() * 100 / totalobservations

#Because the latitude and diameter data show such high precision, it is not as clear what the distribution looks like.
#As such, we will provide a new table that reduces the precision to 1 significant figure and look at the
#distribution again

#create new columns where the significant digit has been reduced to 1
data['LATITUDE_CIRCLE_IMAGE_REDUCED'] = data.LATITUDE_CIRCLE_IMAGE.round(1)
data['DIAM_CIRCLE_IMAGE_REDUCED'] = data.DIAM_CIRCLE_IMAGE.round(1)

print('This table shows the frequency of craters by latitude when latitude is reduced to 1 sig. digit.')
c1v1 = data.groupby('LATITUDE_CIRCLE_IMAGE_REDUCED').size()

print('This table shows the distribution by % of craters by latitude when latitude is reduced to 1 sig. digit.')
p1v1 = data.groupby('LATITUDE_CIRCLE_IMAGE_REDUCED').size() * 100 / totalobservations

print('This table shows the frequency of craters by diameter when the diameter is reduced to 1 sig. digit.')
c2v1 = data.groupby('DIAM_CIRCLE_IMAGE_REDUCED').size()

print('This table shows the distribution by % of craters by latitude when the diameter is reduced to 1 sig. digit')
p2v1 = data.groupby('DIAM_CIRCLE_IMAGE_REDUCED').size() * 100 / totalobservations

#The majority of the data does not have ejecta morphology listed as such, we create another data set
#such that only craters with a category of ejecta is included. Fortunately, all categories that are not
#empty have at least 2 letters otherwise I would have to match up using regular expressions.

data2 = data.loc[data['MORPHOLOGY_EJECTA_1'].str.len()>1]

#The number of observations will be reduced since only a subset of craters had ejecta labeled
subsetobservations = len(data2)

print('This data shows the frequency of Ejecta morphology of craters with labeled Ejecta.')
c3v1 = data2.groupby('MORPHOLOGY_EJECTA_1').size()

print('This data shows the percentage of Ejecta by Ejecta type for craters with labeled Ejecta')
p3v1 = data2.groupby('MORPHOLOGY_EJECTA_1').size() * 100 / subsetobservations

#Merge the frequency and % series data into one data table and rename the index to show properly

finalc1v1p1v1 = pandas.concat([c1v1,p1v1],axis=1)
finalc2v1p2v1 = pandas.concat([c2v1,p2v1],axis=1)
finalc3v1p3v1 = pandas.concat([c3v1,p3v1],axis=1)

#creating a dictionary to rename the columns in the summary tables properly

renamingdictionary = {0:'FREQUENCY',1:'PERCENTAGE'}

print('This table shows the combined frequency and percent of craters by latitude.')
finalc1v1p1v1 = finalc1v1p1v1.rename(columns=renamingdictionary)

print('This table shows the combined frequency and percent of craters by diameter.')
finalc2v1p2v1 = finalc2v1p2v1.rename(columns=renamingdictionary)

print('This table shows the combined frequency and percent of craters by ejecta morphology.')
finalc3v1p3v1 = finalc3v1p3v1.rename(columns=renamingdictionary)