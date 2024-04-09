
import numpy as np
import pandas as pd

df=pd.read_excel("Recomandation.xlsx")




df['tags'] = df['Name'] +" "+ df['Category'] +" "+ df['Rating'].astype(str)






df["tags"]=df["tags"].str.lower()



from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')
    




vector = cv.fit_transform(df['tags']).toarray()



from sklearn.metrics.pairwise import cosine_similarity



similarity = cosine_similarity(vector)





def recommend(Category):
    index = df[df['Category'] == Category].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    new_list=[]
    for i in distances[1:4]:
        new_list.append(df.iloc[i[0],:])
    return pd.DataFrame(new_list,columns=["Name"])






