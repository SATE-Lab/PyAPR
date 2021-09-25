

import reWriteName
import astunparse
import ast


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # github = Github(login_or_token='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')
    # repo_name = ['ray-project/ray']
    # for repo in repo_name:
    #     r = github.get_repo(repo).get_pulls(state='closed')
    #     print(repo,r.totalCount)

    with open('breadth_first_search.py', 'r') as f:
        file = f.readlines()

    buggyCodeAST = ast.parse(file).body
    visitor = reWriteName.ReWriteName()
    for node in buggyCodeAST:
        funNode = visitor.visit(node)
        buggyCode = astunparse.unparse(funNode)


