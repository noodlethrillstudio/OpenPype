# -*- coding: utf-8 -*-
"""Utility functions used for Avalon - Harmony integration."""
import subprocess
import threading
import os
import random
import zipfile
import sys
import filecmp
import shutil
import logging
import contextlib
import json
import signal
import time
from uuid import uuid4
from qtpy import QtWidgets, QtCore, QtGui
import collections

from .server import Server

from openpype.tools.stdout_broker.app import StdOutBroker
from openpype.tools.utils import host_tools
from openpype import style
from openpype.lib.applications import get_non_python_host_kwargs

# Setup logging.
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def main(*subprocess_args):
    # coloring in StdOutBroker
    os.environ["OPENPYPE_LOG_NO_COLORS"] = "False"
    app = QtWidgets.QApplication([])
    app.setQuitOnLastWindowClosed(False)
    icon = QtGui.QIcon(style.get_app_icon_path())
    app.setWindowIcon(icon)

    ProcessContext.stdout_broker = StdOutBroker('harmony')
    ProcessContext.stdout_broker.start()
    launch(*subprocess_args)

    loop_timer = QtCore.QTimer()
    loop_timer.setInterval(20)

    loop_timer.timeout.connect(ProcessContext.main_thread_listen)
    loop_timer.start()

    sys.exit(app.exec_())


def launch(application_path, *args):
    """Set Harmony for launch.

    Launches Harmony and the server, then starts listening on the main thread
    for callbacks from the server. This is to have Qt applications run in the
    main thread.

    Args:
        application_path (str): Path to Harmony.

    """
    from openpype.pipeline import install_host
    from openpype.hosts.storyboardpro import api as storyboardpro

    install_host(storyboardpro)
