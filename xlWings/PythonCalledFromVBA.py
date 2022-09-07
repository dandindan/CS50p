# Call python code from VBA using xlWings library.
# This code is called from the workbook: "VBA call Python code.xlsm".
# YouTube Video: https://youtu.be/6qo3ly3-_I8
import xlwings as xw

def main():
    wb = xw.Book.caller()
    sheet = wb.sheets('Sheet1')
    sheet["A1"].value = "Called from VBA"