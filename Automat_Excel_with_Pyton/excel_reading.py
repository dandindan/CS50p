import openpyxl

wb = openpyxl.load_workbook('store.xlsx')

print(wb.sheetnames)

