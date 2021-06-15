import numpy as np 
import scipy as sp 
import pandas as pd

class StatFunctions():
    def _init_(self):
        self.DataFrame = DataFrame
        self.FilePath = FilePath
        self.columns = columns

    def NormalizeDF(self, df):
        '''Normalizes all columns of the dataframe independantly from zero 
        to the maximum value found in the column

        Input: dataframe

        Output: dataframe
        '''
        dfNorm = df.loc[:, df.columns != 'SKU'].copy()
        #dfNorm = df.drop('SKU', axis = 1, inplace = True)
        for column in dfNorm.columns:
            dfNorm[column] = dfNorm[column] / dfNorm[column].abs().max()

        dfNorm['SKU'] = df['SKU']
        cols = dfNorm.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        dfNorm = dfNorm[cols]
        return dfNorm

    def RowParameterCount(self, df):
        '''Checks the dataframe row by row  to determine the number of columns 
        that do not contain a zero value and creates a new column with that
        value

        Input: dataframe

        Output: dataframe
        '''
        Colnumber = len(df.columns) - 1
        df['NonZeroCount'] = Colnumber - (df == 0).astype(int).sum(axis=1)
        return df

    def RawTestScore(self, df, Property = "All"):
        '''Subtracts the value from the first row of the dataframe from each
        cell in the dataframe. This creates a new dataframe with raw distance
        values. Then sums up all of the cells values and creates a column with 
        that value. That column is then added to the initial dataframe. 

        Inputs:
            dataframe: The dataframe containing all of the data

            Property: Checks to see if a specific Property is of interest. 
            If so, will give an output of the raw distance dataframe to be
            used later. 

        Output: dataframe
        '''
        dfRaw = df.drop(['SKU','NonZeroCount'],axis = 1).copy()
        dfRowOne = dfRaw.iloc[0]
        dfRaw = abs(dfRaw - dfRowOne)

        dfRaw['SKU'] = df['SKU']
        cols = dfRaw.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        dfRaw = dfRaw[cols]
        dfRaw['Raw Test Score'] = dfRaw.sum(axis = 1)

        df['Raw Test Score'] = dfRaw['Raw Test Score']
        if Property is "All":
            return df
        return dfRaw

    def TestScore(self, df):
        '''Creates a column comprised of the raw test value divided by the
        number of non zero columns to give a relative test score to sort by. 

        Input: dataframe

        Output: dataframe
        '''
        df['Test Score'] = df['Raw Test Score'] / df['NonZeroCount']
        return df

    def SortDf(self, df, nresults, Property = 'Test Score'):
        '''Creates a smaller dataframe featuring either the test value of the 
        result of being selected over all properties or the property itself
        if selected. 

        Inputs: 
            dataframe: The dataframe containing all of the Test scores.

            nresults: an integer value that determines how many values of interest
            will be in the output dataframe. In ascending order. 

            Property: Determines the property of interest if not All properties
            together. Will also select the new column being created in the output. ;


        Output: smaller dataframe
        '''
        df = df.iloc[1:]
        df = df.nsmallest(nresults, Property)
        return df

    def PolymerSelection(self, df, nresults, Property = "All"):

        '''Runs all of the above functions in one neat function. 

        Inputs: 
            dataframe: The dataframe containing all of the data.

            Int: an integer value that determines how many values of interest
            will be in the output dataframe. In ascending order. 

            Property: Determines the property of interest if not All properties
            together. Will also select the new column being created in the output.


        Output: results dataframe
        '''
        if Property is not "All":
            dfNorm = self.NormalizeDF(df)
            dfRowParamCount = self.RowParameterCount(dfNorm)
            dfRawTestScore = self.RawTestScore(dfRowParamCount, Property) 

            dfResults = dfRawTestScore#.drop(0,axis=0,inplace=True)
            dfResults = self.SortDf(dfResults, nresults, Property)
            dfResults[Property] = df[Property]
            dfResults = dfResults[['SKU',Property]]
        else: 
            dfNorm = self.NormalizeDF(df)
            dfRowParamCount = self.RowParameterCount(dfNorm)
            dfRawTestScore = self.RawTestScore(dfRowParamCount)
            dfTestScore = self.TestScore(dfRawTestScore)

            dfResults = self.SortDf(dfTestScore,nresults)
            dfResults = dfResults[['SKU','Test Score']]
        return dfResults