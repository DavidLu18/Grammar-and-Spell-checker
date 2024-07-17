import language_tool_python

class GrammarChecker:
    def __init__(self, language='en-US'):
        self.tool = language_tool_python.LanguageTool(language)

    def check_grammar(self, text):
        matches = self.tool.check(text)
        return matches

# Ví dụ sử dụng khi kiểm tra:
if __name__ == "__main__":
    checker = GrammarChecker()
    text = "This are a example sentence with bad grammar."
    matches = checker.check_grammar(text)
    for match in matches:
        print(match)
