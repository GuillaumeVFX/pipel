#
# Copyright (C) 2009 - 2019 Isotropix SAS. All rights reserved.
#
# The information in this file is provided for the exclusive use of
# the software licensees of Isotropix. Contents of this file may not
# be distributed, copied or duplicated in any form, in whole or in
# part, without the prior written permission of Isotropix SAS.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

## @package pyqt_clarisse
# This module defines helper methods to integrate PyQt/PySide functionalities
# into Clarisse.
#
# @note
#     This module must be imported **AFTER** having imported PyQt or PySide,
#     and only one of those must be imported. This is due to the code
#     detecting which version of Qt is currently loaded.
#
# @code{python}
#     from PySide import QtGui
#     import pyqt_clarisse
#     
#     # ... the rest of the code ...
# @endcode
#
# or:
#
# @code{python}
#     from PyQt4 import Qt
#     import pyqt_clarisse
#     
#     # ... the rest of the code ...
# @endcode
#

import ix
import sys

## Runs the specified QApplication without blocking Clarisse main-loop
#
# @param app
#     The QApplication to run.
#
def exec_(application):
    is_history_enabled = ix.application.get_command_manager().is_history_enabled()
    PyQtAppClarisseHelper(application).exec_()
    while are_windows_visible():
        if is_history_enabled == False: ix.enable_command_history()
        ix.application.check_for_events()
        if is_history_enabled == False: ix.disable_command_history()

def are_windows_visible():
    # return if any top window is visible
    return any(w.isVisible() for w in _qt_gui.QApplication.topLevelWidgets())

class PyQtAppClarisseHelper:
    def __init__(self, app):
        self.app = app
        self.event_loop = _qt_core.QEventLoop()

    def exec_(self):
        # add the callback to Clarisse main loop
        ix.application.add_to_event_loop_single(self.process_events)

    def process_events(self):
        if are_windows_visible():
            # call Qt main loop
            self.event_loop.processEvents()
            # flush stacked events
            self.app.sendPostedEvents(None, 0)
            # add the callback to Clarisse main loop
            ix.application.add_to_event_loop_single(self.process_events)

## This function will check loaded modules to try and guess which version was
# loaded. In case no version or multiple ones were loaded, it will log an error
# and return nothing.
#
# @note
#     This function is "private" and shouldn't be used directly by anthing
#     other than the pyqt_clarisse module.
#
# @returns
#     A pair containing the QtCore and QtGui modules in that order.
#     Both modules can be None in case of errors.
#
def _get_qt():
    # check which versions of Qt are loaded
    pyqt4 = 1 if sys.modules.has_key("PyQt4") else 0
    pyside = 1 if sys.modules.has_key("PySide") else 0

    # get the number of loaded versions
    loaded_qt_versions = pyqt4 + pyside

    # if no version of Qt is loaded, or if multiple ones are,
    # throw an exception
    if loaded_qt_versions == 0:
        raise Exception("pyqt_clarisse - no known Qt module found. Try importing PyQt4 or PySide **before** importing pyqt_clarisse")
    elif loaded_qt_versions > 1:
        raise Exception("pyqt_clarisse - more than one Qt module loaded ! Load only one of PyQt4 or PySide before importing pyqt_clarisse")

    # here we can actually load the correct version of Qt and
    # return its QtCore and QtGui parts.
    if pyqt4 == 1:
        from PyQt4 import QtCore, QtGui
        return QtCore, QtGui
    elif pyside == 1:
        from PySide import QtCore, QtGui
        return QtCore, QtGui


# load QtCore and QtGui (or QtWidgets in case Qt5 is used)
_qt_core, _qt_gui = _get_qt()
