import pandas as pd

df=pd.read_excel("roadmap.xlsx")

syllabus=""
for i in df["Description"]:
#     print(i.split())
    for k in i.split(","):
        syllabus=syllabus+'{} , '.format(k)
        
# print(syllabus)