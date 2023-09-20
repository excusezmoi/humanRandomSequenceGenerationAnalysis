# Human Random Sequence Generation Analysis

A set of programs to analyze the random sequences generated by humans

## Configuration

The configuration file for the analysis. The file is in the format of ini file, named "config.ini". The file contains the following sections:

### Files
- subjectiveFile: the file that contains the subjective similarity data

### Folders
- responseFileFolder: containing the response files, which are the txt files with responses of the subjects
- rgCalcResultsFolder: containing the output result files of the software "rgCalc"

## Data Processing

Python is used in this stage of data processing.

### Purely Subjective Similarity Related

#### utils.py

Containing the essential functions to process the data. These functions are called by the other Python files.

#### MDS.py

Perform MDS analysis on the subjective similarity data. The MDSPlotter class has two main functions, the first one plotting the individual MDS according to the given parameters, and the second one plotting the MDS plots of all participants given the parameters.

#### cluster.py (failed)

Perform clustering analysis on the subjective similarity data. Nothing is found in this step.

#### similarityCorrelation.py

Calculate the correlation of the subjective similarity matrices between two participants.

### Both Subjective Similarity and Actual Sequence Related

#### Markov.py

**Show the Markov matrix of the "number" condition** of each participant. And also the weighted Markov matrix, which considers the objective distance between the numbers. The objective distance is also provided.

The MarkovChainAll class has the attribute of participant, such as p1, p2. And the respective participant attribute has the condition attribute, such as snum, fact. The respective condition attribute is a MarkovChain class object, which has the attribute of Markov matrix, Weighted Markov matrix, and the average objective difference. 

#### subjectiveDistance.py

Shows
- randomDistance: the average subjective distance if the sequence is random
- averageDistance: the average actual distance from their random sequence

Both the values of "numbers" or "action" conditions can be shown. 

## Before Data Analysis...

### Purely Actual Sequence Related
 
#### rgCalc

The software "rgCalc" is used to calculate the randomness of the sequences.

#### readRgcalcResults.py

Read the TXT results of the software "rgCalc" and convert them to pandas dataframe. It also writes the dataframe to CSV files.

#### CfIndex.py

Calculate the correlation function index of the sequences. The index is calculated by the following formula:

```
Cf(i) = X(i) / n  
```

## Data Analysis

This stage of data analysis is done in R.

### nonParametric.r

First, read the data from the results of "rgCalc" and then perform non-parametric tests on the data. The test used is the Aligned Rank Transform test. Many indices could be tested with this test, for now only the following indices are tested:
- R (used Shannon's entropy)

### indicesTesting.R and indicesTesting.ipynb

The same as the previous one. Currently bootstrapping has been done to estimate the power of the test. The indices tested are:
- R (used Shannon's entropy)

### subjectiveDistance.R

Plot the expected subjective distance and the actual subjective distance of the sequences in every participant. The expected subjective distance is calculated by the average subjective distance of the subjective similarity. The actual subjective distance is calculated by the average subjective distance of the actual sequences.

The objective distance is also plotted in the number condition.

## Functional File

### rightTheWrong.py

This file contains some miscellaneous functions for a single use to convert the file to desirable format etc.

# To Be Done

- how is the similarity of the phonetics of the numbers or actions related to the subjective similarity?

- use the Academia Sinica 平衡語料庫 https://asbc.iis.sinica.edu.tw/

- Analysis with 筠潔's suggestion: gap analysis

