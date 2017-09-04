import re
import os

class Template():
    def __init__(self):
        self.pattern = re.compile(r'{%(.*?)%}', re.DOTALL)

    def render(self, text):
        result = text
        tokens = []
        for index, token in enumerate(self.pattern.split(text)):
            if index % 2 == 0:
                if token:
                    tokens.append(token)
            else:
                directive = token.strip().split(' ')
                tokens.append(getattr(self, directive[0])(directive))
        result = ''.join(tokens)
        return result

    def include(self, directive):
        fullname = os.path.dirname(os.path.abspath(__file__)) + '/templates/' + directive[1]
        with open(fullname, 'r') as f:
            data = f.read()
        return data