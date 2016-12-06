import json

class KeyNode:
    def __init__(self):
        self.parent = None
        self.children = []
        self.action = ""

    def is_leaf(self):
        return len(self.children) == 0

    @staticmethod
    def createFromDic(dic):
        node = KeyNode()
        if "input_char" in dic:
            node.action = dic["input_char"]
        elif "act" in dic:
            node.action = dic["act"]

        if "keys" in dic:
            for child_key in dic["keys"]:
                child_node = KeyNode.createFromDic(child_key)
                child_node.parent = node
                node.children.append(child_node)
        return node

    @staticmethod
    def loadFromFile(filepath_str):
        file = open(filepath_str, 'r')
        node_object = json.loads(file.read())
        file.close()

        return KeyNode.createFromDic(node_object)