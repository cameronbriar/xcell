#!/usr/bin/env/ python

"""
x Cell -- No more cells.
Tool to rid Excel from the pipeline.

Run: python xcell.py

See: README.md
"""

import os, sys
import xlwt, xlrd


SHEETNAME_DELIM = "--"
COLUMN_DELIM    = "|"
ENDSHEET_DELIM  = "+"
OUTPUT_FILENAME = 'xcell'
BLANK_CELL_FLAG = False

class XC(object):

    def __init__(self):
        self.SD  = SHEETNAME_DELIM
        self.CD  = COLUMN_DELIM
        self.ES  = ENDSHEET_DELIM
        self.OUT = OUTPUT_FILENAME
        self.WRITE_BLANKS = BLANK_CELL_FLAG
        return

    def build(self, filename='xcell.txt'):
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
        quota.save(self.OUT + ".xls")
        return

    def convert(self, filename='xcell.xls'):
        quota  = xlrd.open_workbook(filename)
        sheets = [str(sheet) for sheet in quota.sheet_names()]
        data   = []
        flag   = self.WRITE_BLANKS
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
            with open(self.OUT + ".txt", 'w') as f:
                f.write('\n'.join(data))
        return


def main():
    argCount = len(sys.argv)
    task, filename = "", ""
    options = {}

    xc = XC()

    available_flags = {}
    available_flags["-s"] = None
    available_flags["-c"] = None
    available_flags["-n"] = None
    available_flags["-e"] = None
    available_flags["-x"] = None
    available_flags["-f"] = None
    available_flags["-o"] = None

    available_flags['single'] = ['-s', '-f', '-o'] # flags with no value following

    if argCount == 3:
        _, task, filename = sys.argv

    elif argCount >= 4:
        _, task, filename = sys.argv[:3]
        flags = sys.argv[3:]

        for i, flag in enumerate(flags):
            if flag in available_flags['single']:
                available_flags[flag] = True
            else:
                if flag in available_flags.keys():
                    available_flags[flag] = flags[i + 1]

        if available_flags['-x']:
            xc.CD, xc.SD, xc.ES = available_flags['-x'].replace('tab', '\t').split('_')
        else:
            if available_flags['-c']:
                xc.CD = available_flags['-c'].replace('tab', '\t')
            if available_flags['-n']:
                xc.SD = available_flags['-n']
            if available_flags['-e']:
                xc.ES = available_flags['e']

        if available_flags['-f']:
            xc.OUT = filename.split('.')[0]

        if available_flags['-s']:
            xc.WRITE_BLANKS = True
    else:
        print '\nUsage: python xcell.py <build|convert> [filename]'

    options = {
        'build'   : lambda filename:        xc.build(filename),
        'compile' : lambda sheets, markers: xc.compile(sheets, markers),
        'convert' : lambda filename:        xc.convert(filename),
        'o'       : lambda filename:        os.system('cat ' + filename)
    }

    options['1'] = options['']  = options['build']
    options['2'] = options['convert']

    options[task](filename)

    if available_flags['-o']:
        filename = filename.split('.')[0]
        if available_flags['-f']:
            filename = xc.OUT
        if task == 'build':
            print filename
            options['o'](filename + ".xls")
        else:
            options['o'](filename + ".txt")
    return

if __name__ == '__main__': sys.exit(main())
