import re
from rcd import function_declartation_pattern
from rcd.rcd_function import Function
from rcd.rcd_thread import Thread
from rcd.rcd_timeframe import Timeframe


def __get_function(functions, name, match=True):
    for f in functions:
        if match and name == f.name:
            return f


def __get_thread(threads, name):
    for t in threads:
        if name == t.name:
            return t


def pullout_threads(functions):
    threads = list()
    for f in functions:
        for line in f.body.split("\n"):
            if "pthread_create" not in line:
                continue
            t = Thread(line, f)
            t.add_thread_function(__get_function(functions, t.function))
            threads.append(t)

    return threads


def pullout_functions(code):
    functions = list()
    function_pattern = re.compile(function_declartation_pattern)
    braces_num = 0
    feed = False
    for line in code.split('\n'):
        if function_pattern.match(line):
            function = Function(line)
            braces_num += line.count("{") - line.count("}")
            feed = True
        elif feed:
            function.feed('\n'+line)
            braces_num += line.count("{") - line.count("}")
            if not braces_num:
                feed = False
                functions.append(function)
        else:
            #print("Skipped line: {}".format(line), file=sys.stderr)
            pass
    return functions


def pullout_timeframes(functions, threads):
    timeframe_counter = 1
    timeframes = [Timeframe(0)]
    main = __get_function(functions, "main")

    for line in main.body.split("\n"):
        if "pthread_create" in line:
            if len(timeframes) > timeframe_counter:
                tf = timeframes[timeframe_counter]
            else:
                tf = Timeframe(timeframe_counter)
                timeframes.append(tf)
            thread_name = Thread.extract_thread_name(line)
            tf.add_thread(__get_thread(threads, thread_name))
        elif "pthread_join" in line:
            timeframe_counter += 1

    return timeframes


def parse_code(code, functions, threads, timeframes):
    functions.extend(pullout_functions(code))

    if functions:
        threads.extend(pullout_threads(functions))

    if functions:
        timeframes.extend(pullout_timeframes(list(functions), threads))
