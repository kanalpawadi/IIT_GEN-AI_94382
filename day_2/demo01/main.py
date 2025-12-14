import pandas as pd 
import pandasql as ps 

fileapth="books_hdr.csv"
df=pd.read_csv(fileapth)
print("dataframe columns types :")
print(df.dtypes)
print("\n Emp data:")
print(df.head())
query="select *from data where sal between 1000 and 2000 order by sal "
result=ps.sqldf(query,{"data":df})
print("\n query result:\n " )
print(result)