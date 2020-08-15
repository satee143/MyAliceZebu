# import pandas as pd
#
# # making data frame
# df = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")
# #print(df.iloc[[-2]]['Weight'])
# #print(df)
# #print((df.iloc[-1:-8:-1]['Weight']))
# print(df.iloc[(df.iloc[-1:-8:-1]['Weight'].idxmin())-1]['Weight'])
# #print(df[df.columns[-1]]['Weight'])
# #print(df[['Weight']].idxmin())


s = 'abrakadabara'

l = list(s)
l1 = []
for x in l:
    if x not in l1:
        l1.append(x)
l2 = []
for x in l:
    c = 0
    for x in l:
        c = c + 1
    print(c)
    if x in l:
        l2.append(x)
        l.remove(x)

print(l2)
