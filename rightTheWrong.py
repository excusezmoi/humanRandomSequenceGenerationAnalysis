from utils import configFilePath, readCSVFile, correctDict
import pandas as pd
import itertools

originalFile = readCSVFile()
# print(originalFile)

# df = originalFile[(originalFile["participantNumber"] > 12) & (originalFile["numberOrAction"] == "a")]
df = originalFile[originalFile["numberOrAction"] == "a"]
# print(df)

bigList = []

for participantNumber in range(1, 25):

    actSequenceAll = {
            "as1":{1:"l",2:"q",3:"s",4:"w",5:"r",6:"j"},
            "as2":{1:"w",2:"l",3:"q",4:"r",5:"j",6:"s"},
            "as3":{1:"r",2:"s",3:"l",4:"j",5:"w",6:"q"},
            "as4":{1:"s",2:"w",3:"j",4:"l",5:"q",6:"r"},
            "as5":{1:"q",2:"j",3:"r",4:"s",5:"l",6:"w"},
            "as6":{1:"j",2:"r",3:"w",4:"q",5:"s",6:"l"}
    }
    wrongActSequence = actSequenceAll[f"as{7-(participantNumber % 6) if participantNumber % 6 else 1}"]
    # correctActSequence = actSequenceAll[f"as{participantNumber % 6 if participantNumber % 6 else 6}"]

    ironRule = {a: n for n, a in actSequenceAll["as1"].items()}

    renameColumn = {}
    for i in range(1,7):
        for j in range(1,7):
            if i<j:
                if ironRule[wrongActSequence[i]]<ironRule[wrongActSequence[j]]:
                    renameColumn[f"({i}, {j})"] = f"({wrongActSequence[i]}, {wrongActSequence[j]})"
                else:
                    renameColumn[f"({i}, {j})"] = f"({wrongActSequence[j]}, {wrongActSequence[i]})"
                    
                    
    # renameColumn = {f"({i}, {j})": f"({wrongActSequence[i]}, {wrongActSequence[j]})" for i in range(1,7) for j in range(1,7) if i<j}

    df2 = df[df["participantNumber"] == participantNumber].rename(columns = renameColumn)
    # print(renameColumn)
    # print(df2)
    bigList.append(df2)

bigDf = pd.concat(bigList)

print(renameColumn)

actComb = list(itertools.combinations('lqswrj', 2))
# print(actComb)
columnOrder = {comb: ind for ind, comb in enumerate(actComb)}

formattedColumnOrder = {f'({key[0]}, {key[1]})': value for key, value in columnOrder.items()}


bigDf = bigDf[formattedColumnOrder.keys()]

print(bigDf)

# bigDf.to_csv(configFilePath("FILES", "subjectiveActionFile"), index=False)
# 
# df2 = originalFile[originalFile["numberOrAction"] == "n"]
# df2.to_csv(configFilePath("FILES", "subjectiveNumberFile"), index=False)


# for participantNumber in range(1, 25):
#     print(participantNumber)
#     correctDict(originalFile, participantNumber, "a")
