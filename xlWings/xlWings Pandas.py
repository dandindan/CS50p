# Examples of manipulating data using the Pandas library
# YouTube Video: https://youtu.be/6qo3ly3-_I8
import xlwings as xw
import pandas as pd

#app = xw.App()
wk  = xw.books.open(r'c:\sandbox\marks.xlsx')
sheet = wk.sheets("Results")

# Load the data from the range to the data frame
df = sheet.range("A1:K13").options(pd.DataFrame).value 

# NOTE: Remove the # to run any of these lines
result = df.iloc[:2] # get the first 2 rows
#result = df.iloc[:5,2:5] # get the first 5 rows and columns History to Maths
#result = df[df['Class'].str.match('B')] # Returns rows from Class B
#result = df[df['Students'].str.contains('2')] # Return rows where student contains a 2

# These two lines go together
#classData = df.groupby('Class')
#result = classData.get_group("A").mean() # return the average of each subject for Class A


# This will show the result in a table in a new Excel workbook
xw.view(result)

wk.close