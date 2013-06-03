#!/usr/bin/env/ python

"""
x Cell -- No more cells.
Tool to rid Excel from the pipeline.

Run: python xcell.py

See: README.md
"""

import sys
import xlwt, xlrd


SHEETNAME_DELIM = "--"
COLUMN_DELIM    = "|"
ENDSHEET_DELIM  = "+"

class XC(object):

    def __init__(self):
        self.SD = SHEETNAME_DELIM
        self.CD = COLUMN_DELIM
        self.ES = ENDSHEET_DELIM
        return

    def build(self, filename):
        filename = 'quota.txt' if filename == '' else filename.split(".")[0] + ".txt"
        sheets  = []
        markers = []
        with open(filename, 'r') as f:
            data = f.read().decode('string-escape').decode("utf-8").split('\n')
            section = []
            for each in data:
                if each[:len(self.SD)] == self.SD:
                    # new sheet
                    sheets.append(each[len(self.SD):])
                elif each == self.ES:
                    # end sheet
                    markers.append(section)
                    section = []
                else:
                    section.append(each)
        self.compile(sheets, markers)
        return sheets, markers

    def compile(self, sheets, markers):
        quota = xlwt.Workbook()
        all_sheets = [quota.add_sheet(x) for x in sheets]
        for i, s in enumerate(all_sheets):
            for r, marker in enumerate(markers[i]):
                data = marker.split(self.CD)
                if len(data) == 1:
                    s.write(r, 0, data[0])
                else:
                    for c, info in enumerate(data):
                        info = info if not info.isdigit() else int(info)
                        s.write(r, c, info)
        quota.save('xquota.xls')
        print 'Saved to xquota.xls'
        return

    def convert(self, filename, flag=False):
        filename = 'quota.xls' if filename == '' else filename.split('.')[0] + '.xls'
        quota  = xlrd.open_workbook(filename)
        sheets = [str(sheet) for sheet in quota.sheet_names()]
        data   = []
        for sheet in sheets:
            data.append(self.SD + sheet)
            s = quota.sheet_by_name(sheet)
            row_count = s.nrows
            for r in range(row_count):
                row = s.row(r)
                col_count = len(row)
                row_data  = []
                for c in range(col_count):
                    if s.cell_type(r, c) not in [0, 6] or flag:
                        val = s.cell_value(r, c)
                        try:
                            val = str(val) if type(val) != float else str(int(val))
                        except:
                            print 'Unicode char found'
                            val = val.encode('utf8') if type(val) != float else str(int(val))
                        row_data.append(val)
                data.append(self.CD.join(row_data))
            data.append(self.ES)
            with open('xquota.txt', 'w') as f:
                f.write('\n'.join(data))
        print filename, 'has been converted to xquota.txt!'
        return


def main():
    xc = XC()
    options = {
        'build'   : lambda filename:             xc.build(filename),
        'compile' : lambda sheets, markers:      xc.convert(sheets, markers),
        'convert' : lambda filename, flag=False: xc.convert(filename, flag)
    }

    argCount = len(sys.argv)
    if argCount == 1:
        task = raw_input("""
        Choose a task:
        1) BUILD   (txt -> xls)
        2) CONVERT (xls -> txt)
        >>  """)
        filename = raw_input("""
        Specify filename (default 'quota'):
        """)

        options['1'] = options['']  = options['build']
        options['2'] = options['convert']

        options[task](filename)
    elif argCount == 2:
        arg = sys.argv[1]

        filename = raw_input("""
        Would you like to specify a filename?
        (Default Input: quota.xls/quota.txt)
        (Default Output: xquota.xls/xquota.txt)
        """)

        filename = filename.split('.')[0]

        options[arg](filename)
    elif argCount == 3:
        _, task, filename = sys.argv
        options[task](filename)
    elif argCount == 4:
        _, task, filename, flag = sys.argv
        if task != 'convert':
            print 'No flags are available for BUILDING, you must have meant CONVERT - Try again!'
        else:
            options[task](filename, True)
    else:
        print '\nUsage: python xcell.py <build|convert> [filename]'
    return

if __name__ == '__main__': sys.exit(main())
