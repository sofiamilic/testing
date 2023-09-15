import threading
import sys
from sampler import Sampler


def execute_script(script_path):
    current_thread_id = threading.get_ident()
    # print(f"Thread ID for script execution: {current_thread_id}")
    script_globals = {'__name__': '__main__', '__file__': script_path}
    with open(script_globals['__file__'], 'r') as script_file:
        script_code = script_file.read()
    exec(script_code, script_globals)


if __name__ == '__main__':
    script_path = "./input_code/"+sys.argv[1]+".py"
    p = threading.Thread(target=execute_script, args=(script_path,))
    p.start()
    profiler = Sampler(p.ident)
    profiler.start()
    p.join()
    profiler.stop()
    profiler.printReport()
