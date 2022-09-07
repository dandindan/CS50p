# Read from and write to worksheet using the xlWings library.
# YouTube Video: https://youtu.be/6qo3ly3-_I8
import xlwings as xw
xw.books # Active app
wk  = xw.books.open(r'c:\sandbox\marks.xlsx')

sheet = wk.sheets("Results")
rg = sheet.range("A1:C2")

print(rg.value)

sheet.range("A16").value = "correct1"
