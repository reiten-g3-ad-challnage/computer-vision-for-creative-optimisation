import pandas as pd
import os

class Extract:
    """Extract the start and end frames"""

    def dataloader(self, path):
        """
        Load data from pandas dataframe
        Args:
            path: The path of the csv file
        Return:
            df: dataframe
        """
        df = pd.read_csv(path, index_col=0)
        return df

    def select_columns(self, df, col):
        """
        select column from a dataframe
        Args:
            df: dataframe
            col: column name
        Returns:
            df[col]: column of the dataframe
        """
        return df[col]

    def merge_data(self, data, filename):
        """
        Merge csv files
        Args:
            data: list of csv files
            filename: filename of the csv to be saved
        """
        df1 = data[0]
        for i in range(len(data)):
            df1 = pd.merge(df1, data[i], on="game_id")
        df1.to_csv(filename)