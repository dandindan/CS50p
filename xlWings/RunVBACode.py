# Call a VBA Macro using the xlWings library.
# YouTube Video: https://youtu.be/6qo3ly3-_I8
import xlwings as xw

# Open the workbook - change the path as applicable
wk = xw.books.open(r'c:\sandbox\vbacode.xlsm')
# Get the macro
displaytext = wk.macro('module1.DisplayText')

# Call the macro
displaytext("I was called from Python")

wk.close