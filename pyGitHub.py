import re
from pprint import pprint
import patiencediff
import difflib

import xlsxwriter
import xlrd
from xlutils.copy import copy
import xlwt

from github import Github, GithubException

pull_list = []

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

def getRepo(repo):
    def readIssueInfo(pull):
        is_merged = pull.is_merged()
        if is_merged:
            title = pull.title
            merge_commit_sha = pull.merge_commit_sha
            try:
                commit = repo.get_commit(sha=merge_commit_sha)
                files = commit.files

                if len(files) == 1:
                    filename = files[0].filename
                    stats = files[0].status

                    if stats == 'modified' and filename.endswith('py'):
                        print(pull.html_url, title)

                        title = pull.title
                        body = pull.body
                        fixed_sha = commit.sha
                        buggy_sha = commit.parents[0].sha

                        searchObj_title = re.search(r'(if|when|while).∗', title, re.M | re.I)
                        if searchObj_title is not None:
                            title = "*****   "+pull.title

                        searchObj_body = re.search(r'[a-zA-Z.]*(Exception|Error)', body, re.M | re.I)
                        if searchObj_body is None:
                            body = ''

                        buggy_contents = repo.get_contents(filename, ref=buggy_sha).decoded_content.decode().split('\n')
                        fixed_contents = repo.get_contents(filename, ref=fixed_sha).decoded_content.decode().split('\n')
                        code_diff = patiencediff.unified_diff(buggy_contents,fixed_contents)
                        code_diff = '\n'.join(code_diff)

                        print('********************************************')
                        print(code_diff)
                        print('********************************************')

                        result = [pull.html_url, title, body, buggy_sha, fixed_sha,code_diff]
                        # print(repo.name)
                        write_excel_xls_append(result,repo.name.split('/')[0])

                        # pull_list.append(result)

            except Exception as e:
                print(e)

    github = Github(login_or_token='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')
    repo = github.get_repo(repo, lazy=False)

    '''
    *** bug in title OR bug in label ***
    bug, fix, wrong, error, nan, inf, issue, fault, fail, crash   -- ref：ISSTA-18
    '''
    bug_keywords = ['bug', 'fix', ' wrong ', 'error', ' nan ', ' inf ', ' issue ', ' fault ', ' fail ', ' crash ']
    stop_keywords = ['typo', 'doc', 'spell', 'minor', 'message', 'msg', 'description', 'example', 'compatibility']
    try:
        pulls = repo.get_pulls(state='closed',base='master')
        print(pulls.totalCount)

        for pull in pulls:
            if not pull.merged_at: continue

            title = str(pull.title.lower())
            if any(s in str(title) for s in stop_keywords):
                continue
            else:
                title = str(pull.title.lower())
                if any(s in str(title) for s in bug_keywords):
                    readIssueInfo(pull)
                    continue
                else:
                    for label in pull.labels:
                        if label.name in bug_keywords:
                            readIssueInfo(pull)
                            break
    except Exception as e:
        print(e)

if __name__ == '__main__':

    github = Github(login_or_token='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')

    '''
    ansible/ansible 45171
    pytorch/pytorch	23987
    pandas-dev/pandas	20728
    django/django 14518
    tensorflow/tensorflow	15232
    apache/airflow 12866
    
    matplotlib/matplotlib	9982
    ray-project/ray 9746
    apache/incubator-mxnet	9117
    numpy/numpy	7636
    scipy/scipy	6575
    chainer/chainer	5067
    
    apache/incubator-tvm	4992
    keras-team/keras	4150
    Theano/Theano	4002
    eclipse/deeplearning4j	3404
    scikit-image/scikit-image 3233
    kivy/kivy 3132
    pallets/flask 1975
    boto/boto 1909
    onnx/onnx	1846
    RaRe-Technologies/gensim 1504
    BVLC/caffe	1225
    pygame/pygame	1084
    openai/gym	910
    mila-iqia/blocks	631
    apple/coremltools	454
    Microsoft/CNTK	390
    Lasagne/Lasagne	381
    microsoft/MMdnn	307
    onnx/onnxmltools	300
    facebookresearch/maskrcnn-benchmark	255
    PaddlePaddle/Paddle	148
    '''

    # repo_name = ['tensorflow/tensorflow', 'keras-team/keras', 'pytorch/pytorch', 'BVLC/caffe', 'Theano/Theano',
    #              'apache/incubator-mxnet', 'Microsoft/CNTK', 'eclipse/deeplearning4j']
    # repo_name = ['apache/incubator-mxnet', 'microsoft/MMdnn', 'onnx/onnxmltools',
    #              'openai/gym', 'mila-iqia/blocks', 'Lasagne/Lasagne', 'pygame/pygame']
    # repo_name = ['ansible/ansible','apache/airflow','boto/boto','django/django','pallets/flask','RaRe-Technologies/gensim','kivy/kivy']
    repo_name = ['apache/incubator-mxnet', 'microsoft/MMdnn', 'onnx/onnxmltools',
                  'openai/gym', 'mila-iqia/blocks', 'Lasagne/Lasagne', 'pygame/pygame']
    create_excel_xls(repo_name)

    for repo in repo_name:
        print(repo)
        getRepo(repo)

        # r = github.get_repo(repo, lazy=False).get_pulls(state='closed', sort='created', base='master').totalCount
        # print(repo,r)
