import pandas as pd
from sklearn.feature_selection import mutual_info_regression
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# data = pd.read_csv (r'Files/Forecast_report.csv')
data = pd.read_csv (r'Files/combined_forecast.csv')

X = data.copy()
y = X.pop("Max")
X = X[['Shows','Clicks','CTR','FirstPlaceCTR', 'FirstPlaceClicks', 'PremiumCTR', 'PremiumClicks']]

#CTR,Clicks,Currency,FirstPlaceCTR,FirstPlaceClicks,IsRubric,Max,Min,Phrase,PremiumCTR,PremiumClicks,PremiumMax,PremiumMin,Shows

for colname in X.select_dtypes("object"):
    X[colname], _ = X[colname].factorize()

def make_mi_scores(X, y, discrete_features):
    mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features)
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    return mi_scores

discrete_features = X.dtypes == float

mi_scores = make_mi_scores(X, y, discrete_features)
print(mi_scores[::3])

def plot_mi_scores(scores):
    scores = scores.sort_values(ascending=True)
    width = np.arange(len(scores))
    ticks = list(scores.index)
    plt.barh(width, scores)
    plt.yticks(width, ticks)
    plt.title("Mutual Information Scores - all")
    plt.savefig('all.png', dpi=1500, bbox_inches="tight")


plt.figure(dpi=100, figsize=(8, 5))
plot_mi_scores(mi_scores)
# plt.show()
# sns.lmplot(x="stuff", y="shows", hue="fuel_type", data=discrete_features)



# features = ['Min',"Shows", 'Clicks','CTR', 'FirstPlaceClicks']
# f,ax = plt.subplots(1,1)
# sns.heatmap(data[features].corr(), annot=True, square=True, cmap='coolwarm')
# plt.show()
# plt.close()

