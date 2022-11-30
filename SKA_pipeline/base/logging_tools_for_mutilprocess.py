import logging
import os
import numpy as np


def setup_logger(log_directory='./../data/TemporaryData', log_filename="SH.log"):
    """
    Ensures the system logger is set up correctly. If a FileHandler logger has
    already been attached to the current logger, nothing new is done.

    Parameters
    ----------
    log_directory : str, optional 
        Location of log file, by default ''
    log_filename : str, optional
        Log file name, by default "astronomaly.log"

    Returns
    -------
    Logger
        The Logger object
    """
    root_logger = logging.getLogger()

    reset = False

    if len(root_logger.handlers) != 0:
        for h in root_logger.handlers:
            try:
                flname = h.baseFilename
                if flname != os.path.join(log_directory, log_filename):
                    print('Warning: logger already attached to log file:')
                    print(flname)
                    print('Now switching to new log file:')
                    print(os.path.join(log_directory, log_filename))
                    reset = True

            except AttributeError:
                pass

            if reset:
                root_logger.handlers = []

    if len(root_logger.handlers) == 0:
        log_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(process)d - %(message)s")
        root_logger.setLevel(logging.INFO)

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        file_handler = logging.FileHandler(
            os.path.join(log_directory, log_filename))
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(logging.WARNING)

        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    return root_logger


def format_function_call(func_name, file, *args, **kwargs):
    """
    Formats a function of a PipelineStage or Dataset object to ensure proper
    recording of the function and its arguments. args and kwargs should be
    exactly those passed to the function.

    Parameters
    ----------
    func_name : str
        Name of the stage

    Returns
    -------
    str
        Formatted function call
    """
    # out_str = func_name + '(' + file + ", "
    # out_str = func_name + "(%s)" % file

    # return out_str

    out_str = func_name + " on %s" % (str)(file) + '('

    if len(args) != 0:
        for a in args:
            if type(a) == np.ndarray:
                out_str += (str)([np.size(a), np.sum(a)]) + ', '
            else:
                out_str += (str)(a) + ', '
            
    if len(kwargs.keys()) != 0:
        # print(type(kwargs), "\n", kwargs)
        for key in kwargs.keys():
            if type(kwargs[key]) == np.ndarray:
                out_str += ((str)(key) + '=' + (str)([np.size(kwargs[key]), np.sum(kwargs[key])]) + ', ')
            elif type(kwargs[key]) is dict:
                pass
            else:
                out_str += ((str)(key) + '=' + (str)(kwargs[key]) + ', ')
    # if len(kwargs.keys()) != 0:
    #     print(type(kwargs), "\n", kwargs)
    #     for key, value in kwargs.items():
    #         if type(value) == np.ndarray:
    #             out_str += ((str)(key) + '=' + (str)([np.size(a), np.sum(a)]) + ', ')
    #         else:
    #             out_str += ((str)(key) + '=' + (str)(value) + ', ')

    if out_str[-2] == ',':
        out_str = out_str[:-2]
    out_str += ')'

    return out_str


def log(msg, level='INFO'):
    """
    Actually logs a message. Ensures the logger has been set up first.

    Parameters
    ----------
    msg : str
        Log message
    level : str, optional
        DEBUG, INFO, WARNING or ERROR, by default 'INFO'
    """
    root_logger = logging.getLogger()
    if len(root_logger.handlers) == 0:
        setup_logger()

    if level == 'ERROR':
        root_logger.error(msg)
    elif level == 'WARNING':
        root_logger.warning(msg)
    elif level == 'DEBUG':
        root_logger.debug(msg)
    else:
        root_logger.info(msg)

def log_for_queue(msg, queue, level='INFO'):
    """
    Actually logs a message. Ensures the logger has been set up first.

    Parameters
    ----------
    msg : str
        Log message
    level : str, optional
        DEBUG, INFO, WARNING or ERROR, by default 'INFO'
    """
    root_logger = logging.getLogger()
    if len(root_logger.handlers) == 0:
        worker_configurer(queue)

    if level == 'ERROR':
        root_logger.error(msg)
    elif level == 'WARNING':
        root_logger.warning(msg)
    elif level == 'DEBUG':
        root_logger.debug(msg)
    else:
        root_logger.info(msg)


def check_if_inputs_same(class_name, file, local_variables):
    """
    Reads the log to check if this function has already been called with the
    same arguments (this may still result in the function being rerun if the
    input data has changed).

    Parameters
    ----------
    class_name : str
        Name of PipelineStage
    local_variables : dict
        List of all local variables.

    Returns
    -------
    args_same, bool
        True if the function was last called with the same arguments.
    checksum, int
        Reads the checksum stored in the log file and returns it.
    """
    for key, value in local_variables.items():
        if type(value) == np.ndarray:
            local_variables[key] = [np.size(value), np.sum(value)]

    if "queue" in local_variables.keys():
        del local_variables["queue"]

    hdlrs = logging.getLogger().handlers
    # Try to be somewhat generic allowing for other handlers but this will
    # only return the filename of the first FileHandler object it finds.
    # This should be ok except for weird logging edge cases.
    flname = ''
    for h in hdlrs:
        try:
            flname = h.baseFilename
            break
        except AttributeError:
            pass

    if len(flname) == 0 or not os.path.exists(flname):
        # Log file doesn't exist yet
        return False

    else:
        fl = open(flname)
        func_args = {}
        args_same = False
        for ln in fl.readlines()[::-1]:
            # if class_name + '(' in ln:
            if class_name + " on %s" % (str)(file) + '(' in ln:
                # To be completely general, the string manipulation has to
                # be a little complicated
                stripped_ln = ln.split('-')[-2].split(')')[0].split('(')[-1]
                the_list = stripped_ln.split('=')
                kwarg_list = []

                if len(the_list) > 1:
                    for l in the_list:
                        if ',' not in l:
                            kwarg_list.append(l)
                        else:
                            s = l.split(',')
                            if len(s) > 2:
                                kwarg_list.append(','.join(s[:-1]))
                            else:
                                kwarg_list.append(s[0])
                            kwarg_list.append(s[-1])

                    if len(kwarg_list) != 0:
                        for k in range(0, len(kwarg_list), 2):
                            try:

                                key = kwarg_list[k]
                                value = kwarg_list[k + 1]
                                func_args[key.strip()] = value.strip()
                            except ValueError:
                                # This happens when there are no arguments
                                pass

                args_same = True
                if "queue" in func_args.keys():
                	del func_args["queue"]
                	
                # print("\n\n\n参数比较：")
                # print("-"*30)
                # print(func_args)
                # print(local_variables)
                # print("-"*30, "\n\n\n")

                for k in func_args.keys():
                    if k not in local_variables.keys():
                        args_same = False
                        break
                    else:
                        if k != "force_rerun" and\
                                func_args[k] != (str)(local_variables[k]):
                            args_same = False
                            break

                # if file not in ln:
                #     args_same = False
                #     break
                break

        return args_same

# This is the listener process top-level loop: wait for logging events
# (LogRecords)on the queue and handle them, quit when you get a None for a
# LogRecord.
def listener_process(queue):
    setup_logger()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            import sys, traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

# The worker configuration is done at the start of the worker process run.
# Note that on Windows you can't rely on fork semantics, so each process
# will run the logging configuration code when it starts.
def worker_configurer(queue):
    h = logging.handlers.QueueHandler(queue)  # Just the one handler needed
    root = logging.getLogger()
    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(process)d - %(message)s")
    root.setLevel(logging.INFO)
    root.addHandler(h)
    # send all messages, for demo; no other level or filter logic applied.
