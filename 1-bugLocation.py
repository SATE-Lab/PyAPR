import re
import xlrd
from github import Github
from dataPreprocessing import write_excel_xls_append

def readBody(path, sheet):
    github = Github(login_or_token='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')
    repo = github.get_repo('pandas-dev/pandas')

    xlsx = xlrd.open_workbook(path)
    sheet_names = xlsx.sheet_names()
    pandas_report = xlsx.sheets()[sheet_names.index(sheet)]
    numbers = pandas_report.col_values(0)

    for index in range(1, len(numbers)):
        try:
            num = str(numbers[index]).split('/')[6]
            title = repo.get_issue(int(num)).title

            body = repo.get_issue(int(num)).body
            body = re.search(r'[#](\d+)', body)

            if body is not None:
                ref_num = str(body).split('match=')[1].replace('\'#', '').replace('\'>', '')
                ref_title = repo.get_issue(int(ref_num)).title
                ref_body = repo.get_issue(int(ref_num)).body
                name = pandas_report.col_values(6)[index]

                if ', line ' in ref_body:

                    t = ''
                    text = str(ref_body).splitlines()
                    for j in range(0,len(text)):
                        if (name in text[j]) and (', line ' in text[j]):
                            func = (text[j].split(' ')[-1]+'|').strip()
                            code = (text[j+1]+'|').strip()
                            b = func+code
                            t+=b
                    ref_num = numbers[index].replace(num,ref_num)
                    result = [numbers[index],title,ref_num,ref_title,pandas_report.col_values(5)[index],pandas_report.col_values(6)[index],t]
                    write_excel_xls_append(result,'pandas')

        except Exception as e:
            pass
            # print(e)

if __name__ == '__main__':
    readBody('BugReports.xlsx', 'BugsInPy')
