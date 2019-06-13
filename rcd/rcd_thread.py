import re
from rcd.rcd_tree import build_tree, is_deadlock


class Thread:
    def __init__(self, thread_creation_src, created_in_function):
        code = thread_creation_src.strip().replace("pthread_create", '')[1:-1]  # remove function name with parenthesis
        tokens = code.split(",")
        self.resources_pointer = self.__remove_casting(tokens.pop())
        self.function = tokens.pop().strip()
        self.attrs = tokens.pop().strip()
        self.name = tokens.pop().strip().replace('&', '').replace('*', '')
        self.created_in = created_in_function
        self.thread_function = None
        self.timeframes = []

    def __remove_casting(self, code):
        value = re.sub(r'static_cast<(\w+)\**>', '', code)
        value = re.sub(r'(\(\S+\**\))(?=.)>', '', value)
        value = value.strip()
        while value.startswith('('):
            value = value[1:]
        while value.endswith(')'):
            value = value[:-1]
        return value

    def __repr__(self):
        return 'Thread<'+', '.join("%s: %s" % item for item in vars(self).items())+'>'

    @staticmethod
    def extract_thread_name(line):
        line = line.strip().replace("pthread_create", '')[1:-1]
        return line.split(",")[0].replace('&', '').replace('*', '')

    def add_timeframe(self, timeframe):
        pass #self.timeframes.append(timeframe)

    def add_thread_function(self, function):
        self.thread_function = function

    def __by_mutual_exclusion(self):
        pass

    def __by_nested_unlocking(self):
        braces_num = 0
        tokens = list()
        for line in self.thread_function.body.split('\n'):
            line = line.strip()
            if line.startswith("if") or line.startswith("else"):
                tokens.append((line, braces_num, self.thread_function.name))
            braces_num += line.count("{") - line.count("}")
            if "pthread_mutex_lock" in line:
                tokens.append((line, braces_num, self.thread_function.name))
            if "pthread_mutex_unlock" in line:
                tokens.append((line, braces_num, self.thread_function.name))

        trees = build_tree(tokens)
        for tree in trees:
            if "pthread_mutex_lock" in tree.body or "pthread_mutex_unlock" in tree.body:
                continue
            result = is_deadlock(tree, [])
            if result:
                print("Use this stack trace to eliminate resource conflict in thread {}".format(self.name))
            for element in result:
                while element:
                    print(f'{element.function} -> {element.body}')
                    element = element.parent
                print("="*60)

    def __by_looping(self):
        pass

    def __by_recursion(self):
        pass

    def can_generate_deadlock(self):
        if not self.thread_function:
            return
        self.__by_mutual_exclusion()
        self.__by_nested_unlocking()
        self.__by_looping()
        self.__by_recursion()
