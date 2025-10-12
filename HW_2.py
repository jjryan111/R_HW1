# JJ Ryam
# HW 2

# Q1
# Find the distance between objects 1 and 3 by using the formula provided on the slides. Notice that we have mixed type
# of attributes. (You can scan and submit your handwritten calculation) (25/20 points)

# Object Identifier test-1(nominal) test-2 (ordinal) test-3 (numeric)
# 1 A excellent 45
# 2 B fair 22
# 3 C good 64
# 4 A excellent 28

# Nominal Distance (C->A) = 1 because the items are of different categories
# Ordinal Distance (norm(G) - norm(E)) = 1 - 0.5 = 0.5
# Numerical Distance (64-45)/(65-22) = 0.45
# Answer: d(1,3) = (1 + 0.5 + 0.45)/(1+1+1) = 0.65

# 2. Write a program in any language which can compute Manhattan and Euclidean distances
# between any two given vectors with any length. You can pass the length to your function,
# but please don’t limit the dimension to 2. You can test
# your function on vectors you fill in your code without asking user input. (25/20 points)
import math
def manhat(v1, v2):
    v1_length = len(v1)
    v2_length = len(v2)
    if v2_length != v1_length:
        return None
    manhat_dist = 0
    for n in range(v1_length):
        manhat_dist += abs(v1[n] - v2[n])
    return manhat_dist

def euc(v1, v2):
    v1_length = len(v1)
    v2_length = len(v2)
    if v2_length != v1_length:
        return None
    euc_dist = 0
    for n in range(v1_length):
        euc_dist += (v1[n] - v2[n])**2
    return math.sqrt(euc_dist)

v1 = [1,25,47,55,-1]
v2 = [3,0,22,80,4]
print(manhat(v1,v2))
print(euc(v1,v2))
# 3. In the table below, determine whether passing a class has a dependency on
# attendance by using Chi-square test.
# Please refer to the formula in the slides. (25/20 points)
# (For the expected value for each cell, multiply the total counts in
# the rows and columns of the cell and divide by total count.
# For example: Expected value for Attended-Pass=33*31/54 = 18.94. You can scan and submit
# your handwritten calculation)
# Passed Failed Total
# Attended 25 6 31
# Skipped 8 15 23
# Total 33 21 54
# Expected Attend-Pass = (33*31)/54 = 18.94 = ~19
# Expected Skip-Fail = (23*21)/54 = 8.94 = ~9
# Expected Attend-Fail = (31*21)/54 = 12.06 = ~12
# Expected Skip-Pass = (23*33)/54 =  14.06 = ~14
# NULL = No correlation between Attendance and Passing
# Chi^2 = ((25-19)^2)/19 + ((8-14)^2)/9 + ((6-12)^2)/12 + ((15-9)^2)/14
# Chi^2 = 1.89 + 4 + 3 + 2.57 = 11.46
# NULL fails

# 4. In R, there is a built-in data frame called mtcars. Please calculate the correlation between mpg and wt attributes of
# mtcars by using cor() function. Then generate scatter plot based on these two attributes. Your scatter plot should be
# like the one below. You don’t need to submit the image, but R script should be submitted (25/20 points)
# library(ggplot2)
# data(mtcars)
#
# corr_val <- cor(mtcars$mpg, mtcars$wt)
#
# ggplot(mtcars, aes(x = wt, y = mpg)) +
#   geom_point(color = "blue", size = 3)

# 5. Grad Students Only Write an R or Python script which removes or drops the columns which have more than 75%
# missing values. Then it should replace the missing values in the remaining columns with the median value of the
# existing values of that particular column. Download metabolite.csv from Google Drive and use this data set to test your
# code. Please check the end of this document for some useful R examples and hints. (10 points)
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv('metabolite.csv')
thresh = 0.75
cols_to_add = []
for col in df:
    null_count = df[col].isna().sum()/len(df)
    if null_count < thresh:
        cols_to_add.append(col)
clean_df = df[cols_to_add]
df_no_na = clean_df.fillna(df.median(numeric_only=True))
print(df_no_na.head())
print(df.shape)
print(df_no_na.shape)
# 6. Grad Students Only Please apply PCA on the processed metabolites data and create a scatter plot by using first two
# principal components in which points are colored based on the Label column. Please submit your code along with
# your figure in the same file. (10 points)
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv('metabolite.csv')
thresh = 0.75
cols_to_add = []
for col in df:
    null_count = df[col].isna().sum() / len(df)
    if null_count < thresh:
        cols_to_add.append(col)
clean_df = df[cols_to_add]
df_no_na = clean_df.fillna(df.median(numeric_only=True))
print(df_no_na.head())
print(df.shape)
print(df_no_na.shape)
# 6. Grad Students Only Please apply PCA on the processed metabolites data and create a scatter plot by using first two
# principal components in which points are colored based on the Label column. Please submit your code along with
# your figure in the same file. (10 points)
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

no_labels = df_no_na.drop(columns=['Label'])
labels = df_no_na['Label']

scaler = StandardScaler()
no_labels_scaled = scaler.fit_transform(no_labels)

pca = PCA(n_components=2)
no_labels_pca = pca.fit_transform(no_labels_scaled)
print(no_labels_pca)
pca_df = pd.DataFrame(data=no_labels_pca, columns=['PC1', 'PC2'])
pca_df = pd.concat([pca_df, labels.reset_index(drop=True)], axis=1)

for label in pca_df['Label'].unique():
    subset = pca_df[pca_df['Label'] == label]
    plt.scatter(subset['PC1'], subset['PC2'], label=label)

print(pca_df.head)
plt.xlabel('PCA_1')
plt.ylabel('PCA_2')
plt.savefig("alz.png", dpi=300, bbox_inches='tight')
plt.show()
