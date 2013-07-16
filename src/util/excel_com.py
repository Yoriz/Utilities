'''
Created on 1 Jul 2013

@author: Dave Wilson
'''

import win32com.client as win32_client


def cellRef(col, row):
        return '{}{}'.format(col, row)


class ExcelApp(object):
    def __init__(self, visible=True):
        self.visible = visible
        self.app = win32_client.Dispatch("Excel.Application")
        self.app.Visible = self.visible
        self.filename = ""
        self.workbook = None

    def openWorkBook(self, filename):
        self.workbook = self.app.Workbooks.Open(filename)
        self.filename = filename

    def closeWorkBook(self, saveChanges=False):
        self.workbook.Close(SaveChanges=saveChanges)

    def protectSheet(self, sheetName, password):
        sht = self.workbook.Sheets(sheetName)
        sht.Protect(password)

    def isWorkBookReadOnly(self):
        return self.workbook.ReadOnly

    def writeRange(self, sheetName, rangeName, data):
        sht = self.workbook.Sheets(sheetName)
        sht.Range(rangeName).Value = data

    def writeMergedColRange(self, sheetName, rangeName, data):
        data = [(line,) for line in data]
        self.writeRange(sheetName, rangeName, data)

    def writeCell(self, sheetName, cellRef, data):
        sht = self.workbook.Sheets(sheetName)
        sht.Range(cellRef).Value = data
