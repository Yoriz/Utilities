'''
Created on 1 Jul 2013

@author: Dave Wilson
'''

import win32com.client as win32_client
import pythoncom
import datetime

# allows any cell to be selected
XLNORESTRICTIONS = 0
# allows only those cells whose Locked property is False to be selected
XLUNLOCKEDCELLS = 1
# prevents any selection on the sheet
XLNOSELECTION = 4142


def cell_ref(col, row):
        return '{}{}'.format(col, row)


def cell_result_to_string(result):
    if type(result) == float:
        result = int(result)
    return str(result).rstrip()


def excel_app(visible=True):
    pythoncom.CoInitialize()  # @UndefinedVariable
    app = win32_client.Dispatch("Excel.Application")
    if not app.ActiveWorkbook:
        app.Visible = visible

    return app


def open_work_book(app, file_name):
    return app.Workbooks.Open(file_name)


def save_work_book(work_book):
    work_book.Save()


def save_work_book_as(work_book, file_name):
    work_book.SaveCopyAs(file_name)


def close_work_book(work_book, save_changes=False):
    work_book.Close(SaveChanges=save_changes)


def close_an_open_workbook(app, file_name, save_changes=False):
    try:
        app.Workbooks(file_name).Close(SaveChanges=save_changes)
    except Exception:
        pass


def select_sheet(work_book, sheet_name):
    work_book.sheets(sheet_name).Select()


def select_cell(work_book, sheet_name, range_name):
    sht = work_book.Sheets(sheet_name)
    sht.Range(range_name).Select()


def protect_sheet(work_book, sheet_name, password):
    sht = work_book.Sheets(sheet_name)
    sht.Protect(password)


def enable_selection(work_book, sheet_name, selection=XLUNLOCKEDCELLS):
    sht = work_book.Sheets(sheet_name)
    sht.EnableSelection = selection


def print_sheet(work_book, sheet_name):
    sht = work_book.Sheets(sheet_name)
    sht.PrintOut()


def is_work_book_read_only(work_book):
    return work_book.ReadOnly


def write_range(work_book, sheet_name, range_name, data):
    sht = work_book.Sheets(sheet_name)
    sht.Range(range_name).Value = data


def write_merged_col_range(work_book, sheet_name, range_name, data):
    data = [(line,) for line in data]
    write_range(work_book, sheet_name, range_name, data)


def write_cell(work_book, sheet_name, cell, data):
    sht = work_book.Sheets(sheet_name)
    sht.Range(cell).Value = data


def read_range(work_book, sheet_name, range_name):
    sht = work_book.Sheets(sheet_name)
    return sht.Range(range_name).Value


def read_date_range(work_book, sheet_name, range_name):
    date = read_range(work_book, sheet_name, range_name)
    if date:
        return datetime.datetime.strptime(str(date), '%m/%d/%y %H:%M:%S')

    return None


def read_int_range(work_book, sheet_name, range_name):
    value = read_range(work_book, sheet_name, range_name)
    try:
        return int(value)
    except TypeError as exception:
        print exception, value
        return 0


def read_str_range(work_book, sheet_name, range_name):
    value = read_range(work_book, sheet_name, range_name)
    return cell_result_to_string(value)


def read_merged_col_range(work_book, sheet_name, range_name):
    values = read_range(work_book, sheet_name, range_name)
    return '\n'.join(
        map(cell_result_to_string, (item[0] for item in values if item[0])))


class ExcelApp(object):
    def __init__(self, visible=True):
        self.visible = visible
        self.app = win32_client.Dispatch("Excel.Application")
        if not self.app.ActiveWorkbook:
            self.app.Visible = self.visible
        self.filename = ""
        self.workbook = None

    def open_work_book(self, file_name):
        self.workbook = self.app.Workbooks.Open(file_name)
        self.filename = file_name

    def save(self):
        self.workbook.Save()

    def save_copy_as(self, file_name):
        self.workbook.SaveCopyAs(file_name)

    def close_work_book(self, save_changes=False):
        self.workbook.Close(SaveChanges=save_changes)

    def close_a_open_workbook(self, file_name, save_changes=False):
        try:
            self.app.Workbooks(file_name).Close(SaveChanges=save_changes)
        except Exception:
            pass

    def select_sheet(self, sheet_name):
        self.workbook.sheets(sheet_name).Select()

    def select_cell(self, sheet_name, cell_ref):
        sht = self.workbook.Sheets(sheet_name)
        sht.Range(cell_ref).Select()

    def protect_sheet(self, sheet_name, password):
        sht = self.workbook.Sheets(sheet_name)
        sht.Protect(password)

    def print_sheet(self, sheet_name):
        sht = self.workbook.Sheets(sheet_name)
        sht.PrintOut()

    def is_work_book_read_only(self):
        return self.workbook.ReadOnly

    def write_range(self, sheet_name, range_name, data):
        sht = self.workbook.Sheets(sheet_name)
        sht.Range(range_name).Value = data

    def write_merged_col_range(self, sheet_name, range_name, data):
        data = [(line,) for line in data]
        self.write_range(sheet_name, range_name, data)

    def write_cell(self, sheet_name, cell_ref, data):
        sht = self.workbook.Sheets(sheet_name)
        sht.Range(cell_ref).Value = data

if __name__ == '__main__':
    from mg.ncr_form_emailer import constants as cons
    file_path = 'C:/Documents and Settings/Dave Wilson/Desktop/1201-13.xls'

    app = excel_app()
    work_book = open_work_book(app, file_path)
    range_name = 'B24:B32'
    print read_range(work_book, cons.NCR_FORM_SHEET_NAME, range_name)
    