# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0
"""OCRmyPDF's multiprocessing/multithreading abstraction layer."""

from __future__ import annotations

import logging
import logging.handlers
import multiprocessing
import multiprocessing.queues
import os
import queue
import signal
import sys
import threading
from collections.abc import Callable, Iterable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from contextlib import suppress
from typing import TYPE_CHECKING

from rich.console import Console as RichConsole

from ocrmypdf import Executor, hookimpl
from ocrmypdf._logging import RichLoggingHandler
from ocrmypdf._progressbar import RichProgressBar
from ocrmypdf.exceptions import InputFileError
from ocrmypdf.helpers import remove_all_log_handlers

if TYPE_CHECKING:
    from typing import TypeAlias

    Queue: TypeAlias = multiprocessing.queues.Queue | queue.Queue
    UserInit: TypeAlias = Callable[[], None]
    WorkerInit: TypeAlias = Callable[[Queue, UserInit, int], None]

FuturesExecutorClass = type[ThreadPoolExecutor] | type[ProcessPoolExecutor]


def log_listener(q: Queue):
    """Listen to the worker processes and forward the messages to logging.

    For simplicity this is a thread rather than a process. Only one process
    should actually write to sys.stderr or whatever we're using, so if this is
    made into a process the main application needs to be directed to it.

    See:
    https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
    """
    pass


def process_sigbus(*args):
    """Handle SIGBUS signal at the worker level."""
    raise InputFileError("A worker process lost access to an input file")


def process_init(q: Queue, user_init: UserInit, loglevel) -> None:
    """Initialize a process pool worker."""
    pass


def thread_init(q: Queue, user_init: UserInit, loglevel) -> None:
    """Begin a thread pool worker."""
    pass




class StandardExecutor(Executor):
    """Standard OCRmyPDF concurrent task executor."""



@hookimpl
def get_executor(progressbar_class):
    """Return the default executor."""
    pass


RICH_CONSOLE = RichConsole(stderr=True)


@hookimpl
def get_progressbar_class():
    """Return the default progress bar class."""
    pass


@hookimpl
def get_logging_console():
    """Return the default logging console handler."""
    return RichLoggingHandler(console=RICH_CONSOLE)
