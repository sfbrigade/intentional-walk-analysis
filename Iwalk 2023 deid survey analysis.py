#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:53:03 2024

@author: tanvitilloo
"""

import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import uuid
from scipy import stats
import seaborn as sns

file_path = ("/Users/tanvitilloo/Desktop/SF Civic Tech/2023 Survey Data for SFCT - deidentified.xlsx")

iwalk_survey_raw = pd.read_excel(file_path, sheet_name= 1) 
#reads the second sheet that does not contain duplicates 



iwalk_survey_raw.info
iwalk_survey_raw.head(8)
iwalk_survey_raw.tail(8)
iwalk_survey_raw.columns
iwalk_survey_raw.isna().sum()


##################################################################

# DATA CLEANING

##################################################################


headers = iwalk_survey_raw.loc(0) #save the values from the first row
iwalk_survey_raw= iwalk_survey_raw.drop(0) #drop the first row

iwalk_survey_raw = iwalk_survey_raw.iloc[:-3] #drop the last three rows as they are empty

#drop the columns with open-ended questions (as these have not been translated)
open_ended_q = ['Why not?', 
                'Why not?.1',
                'Besides SF Giants tickets, what other prizes would motivate you to keep walking during the program? (e.g. grocery gift card, a pair of walking shoes, exercise equipment, etc.)',
                'What healthy lifestyle changes did you make?',
                'Why not?.2',
                'Is there anything you would change about the Intentional Walk app?']

iwalk_survey_raw.drop(open_ended_q, inplace = True, axis = 1)

#create unique ids for the respondent id column

  #this list comprehension uses the uuid package to generate a random alphanumeric id of length 8
iwalk_survey_raw["Respondent ID"] = [str(uuid.uuid4())[:8] for row in range(len(iwalk_survey_raw))]

#add a line that writes the raw data to a csv 

iwalk_survey_raw.columns #look at remaining columns

##################################################################

# DATA ANALYSIS

##################################################################

#Analyzing Q7 - Q10 (questions with no multiple choice)

#subset the data for responses to Q7 to Q10 
q7_to_q10_df = iwalk_survey_raw.loc[:,"Before the program, how many days a week did you walk for exercise?" : "Now that the program is over, how many days a week do you plan to continue walking for exercise?" ]

def no_multiple_choice_analysis (df): 
   
    """
    This function analyzes survey questions with likert scale responses.
    First, it assign a numerical values to likert responses and then creates
    summary counts for all the likert response options. Then it handles the
    likert questions with open-ended response options. Finally, it visualizes 
    the responses in a bar chart
    
    Parameters:
    df: DataFrame containing Likert responses
    other_column: Column name where "Other" option responses are present
    other_responses_column: Column name where open-ended "Other" responses are present
    
    Returns:
    None
    
    """
    for column in df.columns:
        
        #get the data from the current column in a df 
        question_df = df[column]
        
        #check for missing values
        missing_values = question_df.isna().sum()
        print(f"Missing values in {column}: {missing_values}")
        
        #drop missing values
        question_df_clean = question_df.dropna()
        
        #sum the unique values in the column
        summary_df = question_df_clean.value_counts().rename_axis('Number of days').reset_index(name = 'Counts')
       
        #sum the total number of observations
        total_counts = summary_df['Counts'].sum()
        
        #add a total row in the summary dataframe
        summary_df.loc[len(summary_df)] = ['Total', total_counts]
        
        print(summary_df)
            
        #get the plot data without the total counts
        plot_df = summary_df.iloc[:-1]
        
        #plot a bar graph for each column 
        plot_df.plot(kind = "bar", x = 'Number of days', y ='Counts', legend = False)
        
       # plt.xlabel('')
        plt.ylabel('Counts')
        plt.title(column)
        plt.tight_layout()
        plt.show()

no_multiple_choice_analysis(q7_to_q10_df)


#Analyzing Q11 - Q14 (questions with Likert scale )

#subset the data for responses to Q11 (as this is question contains an open-ended response option)
likert_with_open_ended_df = iwalk_survey_raw.loc[:, "How often did you look at the Top Walkers feature in the app?"]
open_ended_column = iwalk_survey_raw.loc[:, "Why not?.1"]
likert_df= iwalk_survey_raw.loc[:, "The Top Walkers feature was easy to use": "I liked being able to see my place among all walkers on the Top Walkers feature "]


def analyze_likert_with_other(df, open_ended_df):
  
    """
    This function analyzes survey questions with likert scale responses.
    First, it assign a numerical values to likert responses and then creates
    summary counts for all the likert response options. Then it handles the
    likert questions with open-ended response options. Finally, it visualizes 
    the responses in a bar chart
    
    Parameters:
    df: DataFrame containing Likert responses
    other_column: Column name where "Other" option responses are present
    other_responses_column: Column name where open-ended "Other" responses are present
    
    Returns:
    None
    
    """
    
   #Assign numeric values to likert options
   # likert_scale = {
   #     'Strongly Disagree': 1,
    #    'Disagree': 2,
     #   'Neutral': 3,
    #    'Agree': 4,
     #   'Strongly Agree': 5
   # }
    
    #Copy the df with likert questions and replace responses with numeric values
   # df_numeric = df.copy()
    #for col in df.columns:
          #  df_numeric[col] = df[col].replace(likert_scale)
   
    likert_scale = ['Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree']
 
    for column in df:
        
        #check for missing values 
        missing_values = df[column].isna().sum()
        print(f"Missing values in {column}: {missing_values}")
        
        #drop missing values 
        df_clean = df[column].dropna()
        
        #sum the unique values in the df
        summary_df = df_clean.value_counts(normalize = True).reindex(likert_scale).rename_axis('Response Options').reset_index(name = 'Percentage')
        
        # Output the summary table (in percentages)
        summary_df['Percentage'] = summary_df['Percentage'] * 100
        #total_counts = summary_df['Counts'].sum()
        #summary_df.loc[len(summary_df)] = ['Total', total_counts]
        
        print(summary_df)
        
        #Plot a bar graph for each question
        
        #plot a bar graph for each column 
        summary_df.plot(kind = "bar", x = 'Response Options', y ='Percentage', legend = False, color = "purple")
        
        plt.title(f'{column}')
        plt.ylabel('Percentage (%)')
        plt.xlabel('Response Options')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show() 
        
        
        # Count and plot the responses in the open-ended Likert question
        summary_open_df = open_ended_df.dropna().value_counts().rename_axis('Response Options').reset_index(name='Counts')
        total_open_counts = summary_open_df['Counts'].sum()
        summary_open_df.loc[len(summary_open_df)] = ['Total', total_open_counts]
        print(summary_open_df)
        
        
        # Plot the bar chart for open-ended Likert question without the "Total" row
       # plot_open_df = summary_open_df[:-1]  # Remove the "Total" row
       # summary_open_df.set_index('Response Options', inplace=True)

        summary_open_df.plot(kind = "bar", x = 'Response Options', y ='Counts', legend = False)
       # plt.xlabel('')
        plt.ylabel('Counts')
        plt.title(f'{column}')
        plt.tight_layout()
        plt.show()

        
        
    analyze_likert_with_other(likert_df, likert_with_open_ended_df)


def likert_scale_analysis (df):
        
        
        plt.bar(summary_open_df.index, summary_open_df['Counts'], color=sns.color_palette("coolwarm", len(summary_open_df)))
                plt.title(f'{open_ended_df} - Response Distribution (Including "Why not?")')
                plt.ylabel('Counts')
                plt.xlabel('Response Options')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.show()
    

column_names = iwalk_survey_raw.columns

#Data Analysis for Q1






#original_column_name17 = 'Which of the following options would make you walk more during the program? (Select all that apply)'
#q17_index = survey_df.columns.get_loc(original_column_name17)

#q17_df = survey_df.iloc[:, [q17_index + i for i in range(6)]]




iwalk_survey_raw.iloc[:,40:50].tail(25)

