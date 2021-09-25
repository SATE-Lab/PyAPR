import os
from pprint import pprint
import xlrd
from future.moves import sys
from parseCode import parseCode
import astunparse
import ast


def walkFile(file):
    filepath = []
    for root, dirs, files in os.walk(file):
        for f in files:
            path = os.path.join(root, f)
            # if path.endswith('bug.py'):
            filepath.append(path)

    return filepath


def readBugReport(path, sheet):
    xlsx = xlrd.open_workbook(path)
    sheet_names = xlsx.sheet_names()
    report = xlsx.sheets()[sheet_names.index(sheet)]
    nrows = report.nrows
    ncols = report.ncols

    print(nrows)

    for i in range(1, nrows):
        data = [i for i in report.row_values(i) if i != '']

        title = report.row_values(i)[1]
        ref_Title = report.row_values(i)[3]
        sha = report.row_values(i)[4]
        filename = report.row_values(i)[5]

        for index in range(6, len(data), 2):
            # print(index, report.row_values(i)[index])
            func = report.row_values(i)[index]
            code = report.row_values(i)[index + 1]

            if func == ' ': continue

            print(func, '--->', code)
            buggy_funcAST, buggy_statement = readBugFile(sha, filename, func, code)
            print((buggy_funcAST), '--->', (buggy_statement))

            # patchInfo = findCandidatePatch(func, buggy_statement, filename)
            # print('*****************************************')
            # print(len(patchInfo))
            # # rankSimilarCode(sha,buggy_func, buggy_statement,patchInfo)

        print('----------------------------------------------')


def readBugFile(sha, filename, func, code):
    filename = filename.replace('/', '|')
    parse_Code = parseCode('./example/pandas-<' + filename + '>-' + sha + '-bug.py')

    # print(code)

    try:
        buggy_statement = ''
        buggy_funcAST = ''
        bugCode = ''
        bugNode = ''
        bugcodeAST = parse_Code.getCodeAST()

        for node in ast.walk(bugcodeAST):
            # print(node)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # print(node.name,node.lineno)
                if node.name == func:
                    # print(node.name,node.lineno)

                    if node.name == 'str_get':
                        print()
                    for subnode in ast.walk(node):
                        try:
                            temp = astunparse.unparse(subnode)

                            # if node.name == '_try_convert_data' :
                            #     print(temp)

                            if code in temp:
                                bugCode = temp.strip()
                                # print(temp)
                                bugNode = subnode
                        except Exception as e:
                            # print('sub bugcode---->',e)
                            continue

        if bugCode != '':
            buggy_statement = bugCode
            buggy_funcAST = bugNode

        return buggy_funcAST, buggy_statement
    except Exception as e:
        print('bugcodeAST---->',e)
        pass


def findCandidatePatch(func, code, filename):
    filename = filename.replace('/', '|')
    filepath = walkFile('/Volumes/Yang/sourceCode1/')
    # filepath = walkFile('./example')

    patchInfo = []
    patchSet = []

    def addPatch(bugcode, name, path):
        if bugcode not in patchSet:
            patchSet.append(bugcode)
            patchInfo.append([path, name, bugcode])
            # print(len(patchSet))

    for path in filepath:
        if path.endswith('bug.py'):
            parse_Code = parseCode(path)

            # if (filename not in path):
            # bugcode = parse_Code.getCode()
            # if 'if is_platform_mac():' in bugcode:
            #     print(path)
            #     print(bugcode)

            try:
                bugcodeAST = parse_Code.getCodeAST()
                for node in ast.walk(bugcodeAST):
                    if isinstance(node, (ast.FunctionDef)):
                        bugcode = astunparse.unparse(node)
                        if (filename not in path):
                            if (code in bugcode):
                                if (func == node.name):  # func + code
                                    print('1-----', node.name, path)
                                    # print(bugcode)
                                    addPatch(bugcode, node.name, path)
                                else:  # code
                                    print('2-----', node.name, path)
                                    # print(bugcode)
                                    addPatch(bugcode, node.name, path)
                            else:
                                if (func in node.name):  # func
                                    print('3-----', func, node.name, path)
                                    # print(bugcode)
                                    addPatch(bugcode, node.name, path)
                        else:  # filename in path
                            if (code in bugcode):
                                if (func == node.name):  # code
                                    print('4-----', func, node.name, path)
                                    # print(bugcode)
                                    addPatch(bugcode, node.name, path)
                                else:
                                    print('5-----', func, node.name, path)
                                    # print(bugcode)
                                    addPatch(bugcode, node.name, path)
            except Exception as e:
                pass

    return patchInfo


# def rankSimilarCode():
#     with open('Code_sim/demo/codes/code3.py',"w") as f: f.write(bugMethodCode)


if __name__ == '__main__':
    readBugReport('BugSet1111.xlsx', 'Sheet1')
    # findCandidatePatch('','','')
