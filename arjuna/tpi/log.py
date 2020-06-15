# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Log module contains helper functions for easy and pwoerful logging with Arjuna.

All log messages are directed to console as well as arjuna.log file which is generated on a per run basis and is placed in **<project_root>/report/run_dir/log** directory.

Messages generated by the test project as well as Arjuna go to the same log for easy checking of flow.

6 levels of logging are available:

    #. TRACE
    #. DEBUG
    #. INFO
    #. WARNING
    #. ERROR
    #. FATAL

These are represented by six different log_* functions.

**TRACE** has the lowest priority and **FATAL** has the highest priority amongst message levels.

Following Arjuna Options are related to logging:
    * LOG_CONSOLE_LEVEL: Minimum level of logging for a run for displaying log messages on console.
    * LOG_CONSOLE_LEVEL: Minimum level of logging for a run for displaying log messages in arjuna.log.
    * LOG_ALLOWED_CONTEXTS: The context strings which determine log messages belonging to which contexts can be displayed and logged.
'''

import sys

from arjuna.tpi.helper.audit import _Stack
from arjuna.tpi.arjuna_types import *

def __log(invoker, level, msg, contexts=None):
    from arjuna import Arjuna, ArjunaOption
    if type(contexts) is str:
        contexts = (contexts,)
    elif contexts is None:
        contexts = ("default",)
    contexts = set(contexts)
    try:
        getattr(Arjuna.get_logger(), level)(msg.replace('\n', ' ').replace('\r', ''), extra={'invoker': invoker, 'contexts':contexts})
    except AttributeError:
        # In case the logging is called before the logger is set.
        # In future versions, see if there can be a fallabck logger.
        pass
    except OSError:
        ## On Windows 10, random handle related bugs happen.
        if level.lower() in {"info", "debug", "trace"} :
            sys.stdout.write(msg+ "\n")
        else :
            sys.stderr.write(msg+"\n")

def log_trace(msg: str, *, contexts: ListOrTupleOrStr=None):
    '''
        Log a message with **TRACE** level.

        Args: 
            msg: Log message
            contexts: (Optional) Context strings for this log message.
    '''
    __log(_Stack.get_invoker(), "trace", msg, contexts=contexts)

def log_debug(msg: str, *, contexts: ListOrTupleOrStr=None) -> None:
    '''
        Log a message with **DEBUG** level.

        Args: 
            msg: Log message
            contexts: (Optional) Context strings for this log message.
    '''
    __log(_Stack.get_invoker(), "debug", msg, contexts=contexts)

def log_info(msg: str, *, contexts: ListOrTupleOrStr=None) -> None:
    '''
        Log a message with **INFO** level.

        Args: 
            msg: Log message
            contexts: (Optional) Context strings for this log message.
    '''
    __log(_Stack.get_invoker(), "info", msg, contexts=contexts)

def log_warning(msg: str, *, contexts: ListOrTupleOrStr=None) -> None:
    '''
        Log a message with **WARNING** level.

        Args: 
            msg: Log message
            contexts: (Optional) Context strings for this log message.
    '''
    __log(_Stack.get_invoker(), "warning", msg, contexts=contexts)

def log_error(msg: str, *, contexts: ListOrTupleOrStr=None) -> None:
    '''
        Log a message with **ERROR** level.

        Args: 
            msg: Log message
            contexts: (Optional) Context strings for this log message.
    '''
    __log(_Stack.get_invoker(), "error", msg, contexts=contexts)

def log_fatal(msg: str, *, contexts: ListOrTupleOrStr=None) -> None:
    '''
        Log a message with **FATAL** level.

        Args: 
            msg: Log message
            contexts: (Optional) Context strings for this log message.
    '''
    __log(_Stack.get_invoker(), "fatal", msg, contexts=contexts)