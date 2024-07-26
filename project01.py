import pandas as pd
import numpy as np
from plotnine import *
import scipy.stats as st

# reading in the csv form of the hospital charge dataset
hospital_charge_df = pd.read_csv('/Users/maciewheeler/Downloads/Inpatient_Prospective_Payment_System__IPPS__Provider_'
                                 'Summary_for_All_Diagnosis-Related_Groups__DRG__-_FY2017.csv')

#### Question 1

### 1.1

## Part a

# number of unique Provider Ids
number_of_unique_provider_ids = len(hospital_charge_df['Provider Id'].unique())
# print(number_of_unique_provider_ids)

# state that has the most number of unique providers among all states
unique_states = hospital_charge_df['Provider State'].unique()
unique_providers_max = 0
unique_providers_max_state = ''

for state in unique_states:
    providers = hospital_charge_df['Provider Id'][hospital_charge_df['Provider State'] == state]
    unique_providers = len(providers.unique())

    if unique_providers > unique_providers_max:
        unique_providers_max = unique_providers
        unique_providers_max_state = state

# print(unique_providers_max_state)

## Part b

# mean
mean = np.mean(hospital_charge_df['Total Discharges'])
# print(mean)

# median
median = np.median(hospital_charge_df['Total Discharges'])
# print(median)

# standard deviation
std = np.std(hospital_charge_df['Total Discharges'])
# print(std)

## Part c

# number of unique DRG definitions
number_of_unique_drg_definitions = len(hospital_charge_df['DRG Definition'].unique())
# print(number_of_unique_drg_definitions)

## Part d

# category of drg that has the least number of hospital discharges
unique_drg_definitions = hospital_charge_df['DRG Definition'].unique()

first_discharges = hospital_charge_df['Total Discharges'][hospital_charge_df['DRG Definition'] == unique_drg_definitions[0]]
first_sum_of_discharges = sum(first_discharges)
drg_definition_min_value = first_sum_of_discharges
drg_definition_min = unique_drg_definitions[0]

for drg in unique_drg_definitions[1:]:
    discharges = hospital_charge_df['Total Discharges'][hospital_charge_df['DRG Definition'] == drg]
    sum_of_discharges = sum(discharges)

    if sum_of_discharges < drg_definition_min_value:
        drg_definition_min_value = sum_of_discharges
        drg_definition_min = drg

# print(drg_definition_min)

# total discharges in the category of drg that has the least number of hospital discharges
# print(drg_definition_min_value)

### 1.2

## Part a

# histogram for Total Discharges
p1 = ggplot(data=hospital_charge_df, mapping=aes(x = 'Total Discharges')) +\
    geom_histogram(bins=60) +\
    xlim(0, 200) +\
    ylab('Counts') +\
    ggtitle('Histogram of Total Discharges')

# print(p1)

## Part b

# histogram for Average Covered Charges
p2 = ggplot(data=hospital_charge_df, mapping=aes(x = 'Average Covered Charges')) +\
    geom_histogram(bins=80) +\
    xlim(0, 400000) +\
    ylab('Counts') +\
    ggtitle('Histogram of Average Covered Charges')

# print(p2)

## Part c

# scatterplot of Average Total Payments vs. Average Medicare Payments
p3 = ggplot(data=hospital_charge_df, mapping=aes(x = 'Average Total Payments', y = 'Average Medicare Payments')) +\
    geom_point() +\
    ggtitle('Scatterplot of Average Total Payments vs. Average Medicare Payments')

# print(p3)

## Part d

# scatterplot of Average Covered Charges vs. Average Medicare Payments
p4 = ggplot(data=hospital_charge_df, mapping=aes(x = 'Average Covered Charges', y = 'Average Medicare Payments')) +\
    geom_point() +\
    ggtitle('Scatterplot of Average Covered Charges vs. Average Medicare Payments')

# print(p4)

#### Question 2

### 2.1

# For this question I would first sort the DRG Definitions by their mean Average Covered Charges in descending order.
# I would then access the first 100 DRG Definitions, since we want the top 100 most frequently billed discharges of DRG.
# Next, I got the DRG Definitions from the previous step and put them into a list.
# I also made a list of the DRG Definitions with Provider Id and Provider State added to the beginning to use later for
# column names.
# Then I grouped by Provider Id, Provider State, and DRG Definition and aggregated that groupby to get the means of the
# Average Covered Charges.
# Next I got the index of my dataframe that was created in the previous step and used that index to get the level values
# for the DRG Definitions, in order to create a column of the DRG Definitions.
# I then created a new dataframe with the DRG Definition column and the Average Covered Charges column.
# With that dataframe I made a pivot table indexing by Provider Id and Provider State and setting the columns to be the
# DRG Definitions and the values to be the Average Covered Charges.
# I removed the DRG column title from that pivot table and then reset the index.
# I then created a new dataframe with the Provider Id, Provider State, and each of the 100 DRG Charges.
# Lastly, I got the new column names for the Provider Id, Provider State, and for each DRG Charge and replaced the old
# column names with those names.

### 2.2

# grouping the dataframe by DRG Definition and getting the means of each DRG definitions for each column
group = (hospital_charge_df.groupby('DRG Definition')).mean()
# sorting the dataframe by the Average Covered Charges in descending order
sorted1 = group.sort_values(by='Average Covered Charges', ascending=False).reset_index()

# getting the top 100 DRG definitions and adding them to a list
drgs = (sorted1['DRG Definition'][0:100]).tolist()

# list with Provider Id, Provider State and the DRG Definitions to use later as column names
column_names = ['Provider Id'] + ['Provider State'] + drgs

# grouping by Provider Id, Provider State, and DRG Definition then getting average covered charge means for each DRG
group1 = hospital_charge_df.groupby(['Provider Id', 'Provider State', 'DRG Definition']).agg({'Average Covered Charges': np.mean})

# index for group1 dataframe
i = group1.index

# getting the level values for the DRGs and creating a new column
group1['DRG'] = i.get_level_values(2)

# creating a new dataframe with only the DRG definitions and the average covered charges
df = group1[['DRG', 'Average Covered Charges']]

# making a pivot table with provider id and provider state as the index, DRG definitions as the columns and average
# covered charges as the values
new_df = pd.pivot_table(df, index=['Provider Id', 'Provider State'], values='Average Covered Charges', columns='DRG')

# removing the DRG column title
new_df.columns.name = None

# resetting the dataframes' index
new_df = new_df.reset_index()

# getting the final dataframe with the Provider Id, Provider State, and the 100 DRG Charges
answer = new_df[column_names]

# names for the columns of each DRG
answer_columns = ['DRG Charges ' + str(x[0:3]) for x in drgs]

# names of the columns for Provider Id, Provider State and each DRG
new_column_names = ['Provider Id'] + ['Provider State'] + answer_columns

# adding the column names to the dataframe
answer.columns = new_column_names

print(answer)

### 2.3

# A potential issue is NA values.
# In order to handle missing values in the data I could either remove the rows that have NA values,
# or I could replace all the NA/missing values with 0 so that I wouldn't have to get rid of any rows.
# You can't plot a NA value, however when creating a scatterplot in Python it just doesn't plot the NA values, so that
# shouldn't provide an issue.
# But, when creating a boxplot in Python if there is a NA value within what you're trying to plot the boxplot will not
# be plotted, therefore the NA rows either need to be removed or the NA values need to be changed to 0.
# Also, you can't do hypothesis testing with NA values or computations.

#### Question 3

## Part a

# high positive correlation scatterplot number 1
high_pos_corr_1 = ggplot(data=answer, mapping=aes(x='DRG Charges 001', y='DRG Charges 474')) +\
    geom_point(color='blue') +\
    ggtitle('HEART TRANSPLANT OR IMPLANT OF HEART ASSIST SYSTEM W MCC vs. AMPUTATION FOR MUSCULOSKELETAL SYS & CONN TISSUE DIS W MCC')

# print(high_pos_corr_1)

# high positive correlation scatterplot number 2
high_pos_corr_2 = ggplot(data=answer, mapping=aes(x='DRG Charges 031', y='DRG Charges 271')) +\
    geom_point(color='purple') +\
    ggtitle('VENTRICULAR SHUNT PROCEDURES W MCC vs. OTHER MAJOR CARDIOVASCULAR PROCEDURES W CC')

# print(high_pos_corr_2)

# low positive correlation scatterplot number 1
low_pos_corr_1 = ggplot(data=answer, mapping=aes(x='DRG Charges 260', y='DRG Charges 654')) +\
    geom_point(color='red') +\
    ggtitle('CARDIAC PACEMAKER REVISION EXCEPT DEVICE REPLACEMENT W MCC vs. MAJOR BLADDER PROCEDURES W CC')

# print(low_pos_corr_1)

# low positive correlation scatterplot number 2
low_pos_corr_2 = ggplot(data=answer, mapping=aes(x='DRG Charges 837', y='DRG Charges 656')) +\
    geom_point(color='green') +\
    ggtitle('CHEMO W ACUTE LEUKEMIA AS SDX OR W HIGH DOES CHEMO AGENT W MCC vs. KIDNEY & URETER PROCEDURES FOR NEOPLASM W MCC')

# print(low_pos_corr_2)

## Part b

# correlation for high positive scatterplot number 1
corr_1 = answer['DRG Charges 001'].corr(answer['DRG Charges 474'])
# print(corr_1)

# correlation for high positive scatterplot number 2
corr_2 = answer['DRG Charges 031'].corr(answer['DRG Charges 271'])
# print(corr_2)

# correlation for low positive scatterplot number 1
corr_3 = answer['DRG Charges 260'].corr(answer['DRG Charges 654'])
# print(corr_3)

# correlation for low positive scatterplot number 2
corr_4 = answer['DRG Charges 837'].corr(answer['DRG Charges 656'])
# print(corr_4)

#### Question 4

## Part a

# new dataframe with only the six chosen states
boxplotdf = answer[((answer['Provider State'] == 'AL') |
                   (answer['Provider State'] == 'CO') |
                   (answer['Provider State'] == 'FL') |
                   (answer['Provider State'] == 'NC') |
                   (answer['Provider State'] == 'OH') |
                   (answer['Provider State'] == 'WA'))]

# First boxplot
boxplot1 = ggplot(data=boxplotdf, mapping=aes(x='Provider State', y='DRG Charges 460')) +\
    geom_boxplot(aes(fill='Provider State')) +\
    ggtitle('SPINAL FUSION EXCEPT CERVICAL W/O MCC by Six States')

# print(boxplot1)

# Second boxplot
boxplot2 = ggplot(data=boxplotdf, mapping=aes(x='Provider State', y='DRG Charges 271')) +\
    geom_boxplot(aes(fill='Provider State')) +\
    ggtitle('OTHER MAJOR CARDIOVASCULAR PROCEDURES W CC by Six States')

# print(boxplot2)

# Third boxplot
boxplot3 = ggplot(data=boxplotdf, mapping=aes(x='Provider State', y='DRG Charges 840')) +\
    geom_boxplot(aes(fill='Provider State')) +\
    ggtitle('LYMPHOMA & NON-ACUTE LEUKEMIA W MCC by Six States')

# print(boxplot3)

## Part b

# answer dataframe with NAs replaced as 0s
answer_no_na = answer.fillna(0)

# new dataframe without NA values with only the six chosen states
boxplotdf2 = answer_no_na[((answer_no_na['Provider State'] == 'AL') |
                   (answer_no_na['Provider State'] == 'CO') |
                   (answer_no_na['Provider State'] == 'FL') |
                   (answer_no_na['Provider State'] == 'NC') |
                   (answer_no_na['Provider State'] == 'OH') |
                   (answer_no_na['Provider State'] == 'WA'))]

# two-sample student's t-test, two-sided
t,p = st.ttest_ind(boxplotdf2['DRG Charges 460'][boxplotdf2['Provider State'] == 'FL'],
                   boxplotdf2['DRG Charges 460'][boxplotdf2['Provider State'] == 'AL'])
# print(t)
# print(p)

## Part c

# getting data from each DRG for Colorado
colorado_460 = boxplotdf2['DRG Charges 460'][boxplotdf2['Provider State'] == 'CO']
colorado_271 = boxplotdf2['DRG Charges 271'][boxplotdf2['Provider State'] == 'CO']
colorado_840 = boxplotdf2['DRG Charges 840'][boxplotdf2['Provider State'] == 'CO']

# concatenating all three DRG data values into one vector for Colorado
colorado_data = pd.concat([colorado_460, colorado_271, colorado_840])

# getting data from each DRG for Ohio
ohio_460 = boxplotdf2['DRG Charges 460'][boxplotdf2['Provider State'] == 'OH']
ohio_271 = boxplotdf2['DRG Charges 271'][boxplotdf2['Provider State'] == 'OH']
ohio_840 = boxplotdf2['DRG Charges 840'][boxplotdf2['Provider State'] == 'OH']

# concatenating all three DRG data values into one vector for Ohio
ohio_data = pd.concat([ohio_460, ohio_271, ohio_840])

# downsampling the Texas vector
new_ohio_data = np.random.choice(ohio_data, size=len(colorado_data), replace=False)

# two-sample paired student's t-test, two-sided
t,p = st.ttest_rel(colorado_data, new_ohio_data)
# print(t)
# print(p)

# two-sample unpaired student's t-test, two-sided
t,p = st.ttest_ind(colorado_data, ohio_data)
# print(t)
# print(p)
