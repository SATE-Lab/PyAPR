import ast
import astunparse

import re
from pprint import pprint
import patiencediff
import difflib

import xlsxwriter
import xlrd
from xlutils.copy import copy
import xlwt

from github import Github, GithubException


def create_excel_xls(repo_name):
    path = './BugSet.xlsx'
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    for i in repo_name:
        worksheet = workbook.add_sheet(i.split('/')[1], cell_overwrite_ok=True)
    workbook.save(path)

def write_excel_xls_append(value,repo):
    path = './BugSet.xlsx'

    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格

    worksheet = workbook.sheet_by_name(repo)  # 获取 repo 工作簿
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(repo)  # 获取转化后工作簿中的第一个表格

    j = 0
    for i in range(0, index):
        new_worksheet.write(rows_old, i, value[i])  # 追加写入数据，注意是从i+rows_old行开始写入
        j = j+1

    new_workbook.save(path)  # 保存工作簿
    print(repo,": 追加数据成功！")

def codeDiff(repo,filename,buggy_sha,fixed_sha):

    buggy_contents = repo.get_contents(filename, ref=buggy_sha).decoded_content.decode()
    fixed_contents = repo.get_contents(filename, ref=fixed_sha).decoded_content.decode()

    # bugCode = ast.parse(buggy_contents)
    # bugCode = astunparse.unparse(bugCode).split('\n')
    #
    # fixedCode = ast.parse(fixed_contents)
    # fixedCode = astunparse.unparse(fixedCode).split('\n')
    # code_diff = difflib.unified_diff(bugCode,fixedCode)

    code_diff = difflib.unified_diff(buggy_contents.split('\n'),fixed_contents.split('\n'))
    code_diff = '\n'.join(code_diff)

    print('********************************************')
    print(code_diff)
    print('********************************************')

    # extractPatch(code_diff)
    return code_diff

def extractPatch(txt):
    temp = ''
    flag = 0
    for i in txt:
        if i.startswith('@@'):
            if flag == 0:
                flag = 1
                continue
            if flag == 1:
                print('___________________________')
                print(temp)
                print('___________________________')
                temp=''
                continue
        else:
            temp+=i

    print(temp)
    print('___________________________')
