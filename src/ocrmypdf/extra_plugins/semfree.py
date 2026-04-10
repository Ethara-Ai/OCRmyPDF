# SPDX-FileCopyrightText: 2022 James R. Barlow
# SPDX-License-Identifier: MPL-2.0
"""Semaphore-free alternate executor.

There are two popular environments that do not fully support the standard Python
multiprocessing module: AWS Lambda, and Termux (a terminal emulator for Android).

This alternate executor divvies up work among worker processes before processing,
rather than having each worker consume work from a shared queue when they finish
their task. This means workers have no need to coordinate with each other. Each
worker communicates only with the main process.

This is not without drawbacks. If the tasks are not "even" in size, which cannot
be guaranteed, some workers may end up with too much work while others are idle.
It is less efficient than the standard implementation, so not the default.

This module is deprecated and will be removed in a future release. The standard
executor will fall back to threads in these environments.
"""

from __future__ import annotations

import logging
import logging.handlers
import signal
import warnings
from collections.abc import Callable, Iterable, Iterator
from contextlib import suppress
from enum import Enum, auto
from itertools import islice, repeat, takewhile, zip_longest
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection, wait

from ocrmypdf import Executor, hookimpl
from ocrmypdf._concurrent import NullProgressBar
from ocrmypdf.exceptions import InputFileError
from ocrmypdf.helpers import remove_all_log_handlers

warnings.warn(
    "semfree.py is deprecated and will be removed in a future release.",
    DeprecationWarning,
)


class MessageType(Enum):
    """Implement basic IPC messaging."""

    exception = auto()  # pylint: disable=invalid-name
    result = auto()  # pylint: disable=invalid-name
    complete = auto()  # pylint: disable=invalid-name


def split_every(n: int, iterable: Iterable) -> Iterator:
    """Split iterable into groups of n.

    >>> list(split_every(4, range(10)))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    https://stackoverflow.com/a/22919323
    """
    pass


def process_sigbus(*args):
    """Handle SIGBUS signal at the worker level."""
    raise InputFileError("A worker process lost access to an input file")


class ConnectionLogHandler(logging.handlers.QueueHandler):
    """Handler used by child processes to forward log messages to parent."""

    def __init__(self, conn: Connection) -> None:
        """Initialize the handler."""
        # sets the parent's queue to None - parent only touches queue
        # in enqueue() which we override
        super().__init__(None)  # type: ignore
        self.conn = conn

    def enqueue(self, record):
        """Enqueue a log message."""
        pass


def process_loop(
    conn: Connection, user_init: Callable[[], None], loglevel, task, task_args
):
    """Initialize a process pool worker."""
    pass


class LambdaExecutor(Executor):
    """Executor for AWS Lambda or similar environments that lack semaphores."""



@hookimpl
def get_executor(progressbar_class):
    """Return a LambdaExecutor instance."""
    pass


@hookimpl
def get_logging_console():
    """Return a logging.StreamHandler instance."""
    return logging.StreamHandler()


@hookimpl
def get_progressbar_class():
    """Return a NullProgressBar instance.

    This executor cannot use a progress bar.
    """
    pass
