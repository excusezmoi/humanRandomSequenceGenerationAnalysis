# read a txt file and convert it into a pandas dataframe

import numpy as np
import pandas as pd

from main import configFilePath

def convertTxtStringsToDataFrame(txtFileFolder):
    allResults, rowNames = [], []

    for i in range(1, totalParticipant+1):
        for j in ["snum", "fnum", "sact", "fact"]:
            txtFileName = f'/p{i} {j} calc.txt'
            txtFilePath = txtFileFolder + txtFileName

            with open(txtFilePath, 'r') as txtFile:
                txtContent = txtFile.read()

            txtFileData = txtContent.split('\t')
            txtFileData.pop()
            allResults.append(txtFileData)
            rowNames.append(f"p{i} {j}")
            print(txtFileData)

    colNames = ["sample size", "R", "RNG", "NSQ", "RNG2", "TPI", "runs", "coupon",
                "ascending (adjacent)", "descending (adjacent)", "combined (adjacent)",
                "response frequencies for each alternative", *[" " for _ in range(5)],
                "first-order differences", *[" " for _ in range(10)],
                "repetition distance frequency (length 1-20, and a summed value for lengths greater than 20)",
                *[" " for _ in range(20)], "mean repetition gap", "median repetition gap",
                "modal repetition gap", "Phi index values (orders 2 to 7)", *[" " for _ in range(5)]]

    df = pd.DataFrame(allResults, columns=colNames)
    df.index = rowNames
    print(df)

if __name__ == "__main__":
    totalParticipant = 9

    txtFileFolder = configFilePath("FOLDER","rgCalcResultsFolder")
    convertTxtStringsToDataFrame(txtFileFolder)
    # Write dataframe to a csv file
    # df.to_csv("W:/Me/Research/心理/0427報告/rgCalcResults/rgCalcResults.csv", index=True)
