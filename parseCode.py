import ast
import difflib


class parseCode:

    def __init__(self,filepath):
        self.filepath = filepath

    def getCode(self):
        code = open(self.filepath).read()
        return code

    def getCodeAST(self):
        code = open(self.filepath).read()
        codeAST = ast.parse(code)
        return codeAST

    def getCodeAST_byFunName(self,nodeName):
        code = open(self.filepath).read()
        codeAST = ast.parse(code).body
        for node in codeAST:
            if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
                if node.name == nodeName:
                    # print(node.name)
                    return node
                for subnode in node.body:
                    if isinstance(subnode,ast.FunctionDef):
                        if subnode.name == nodeName:
                            # print(subnode.name)
                            return subnode

    def getSimilarMethod(self,codeAST,methodName):
        sequenceMatcher = difflib.SequenceMatcher()
        result = []
        for node in codeAST:
            if isinstance(node,(ast.FunctionDef,ast.ClassDef)):
                similarity_score = sequenceMatcher.set_seqs(methodName,node.name)
                similarity_score = sequenceMatcher.ratio()
                if similarity_score>0.5 or methodName in node.name:
                # if methodName in node.name:
                    result.append([node.name])

                for subnode in node.body:
                    if isinstance(subnode,ast.FunctionDef):
                        similarity_score = sequenceMatcher.set_seqs(methodName,subnode.name)
                        similarity_score = sequenceMatcher.ratio()
                        if similarity_score>0.5 or methodName in subnode.name:
                        # if methodName in subnode.name:
                            result.append([subnode.name])
        return result
