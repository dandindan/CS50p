import openpyxl
print("hello")
# Load the file(change the Path to where the file is stored)
book  = openpyxl.load_workbook(r'/Users/maozlahav/Desktop/marks.xlsx')
sheet = book["Results"]


# Print rows 1 to 5 and columns 3 to 6.
for row in sheet.iter_rows(min_row=1,max_row=5,min_col=3,max_col=6,values_only=True):
    print(row)