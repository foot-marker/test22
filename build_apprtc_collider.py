#!/usr/bin/python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Builds the AppRTC collider using the golang toolchain.

The golang toolchain is downloaded by download_golang.py. We use that here
to build the AppRTC collider server.
"""

import os
import shutil
import subprocess
import sys
import time

import utils


# Code partially copied from
# https://cs.chromium.org#chromium/build/scripts/common/chromium_utils.py
def RemoveDirectory(*path):
  """Recursively removes a directory, even if it's marked read-only.

  Remove the directory located at *path, if it exists.

  shutil.rmtree() doesn't work on Windows if any of the files or directories
  are read-only, which svn repositories and some .svn files are.  We need to
  be able to force the files to be writable (i.e., deletable) as we traverse
  the tree.

  Even with all this, Windows still sometimes fails to delete a file, citing
  a permission error (maybe something to do with antivirus scans or disk
  indexing).  The best suggestion any of the user forums had was to wait a
  bit and try again, so we do that too.  It's hand-waving, but sometimes it
  works. :/
  """
  file_path = os.path.join(*path)
  if not os.path.exists(file_path):
    return

  if sys.platform == 'win32':
    # Give up and use cmd.exe's rd command.
    file_path = os.path.normcase(file_path)
    for _ in xrange(3):
      print 'RemoveDirectory running %s' % (' '.join(
          ['cmd.exe', '/c', 'rd', '/q', '/s', file_path]))
      if not subprocess.call(['cmd.exe', '/c', 'rd', '/q', '/s', file_path]):
        break
      print '  Failed'
      time.sleep(3)
    return
  else:
    shutil.rmtree(file_path, ignore_errors=True)


def main():
  apprtc_dir = os.path.join('apprtc', 'src')
  golang_workspace = os.path.join('src', 'out', 'go-workspace')
  RemoveDirectory(golang_workspace)

  golang_workspace_src = os.path.join(golang_workspace, 'src')

  collider_dir = os.path.join(apprtc_dir, 'collider')
  shutil.copytree(collider_dir, golang_workspace_src,
                  ignore=shutil.ignore_patterns('.svn', '.git'))

  golang_binary = 'go%s' % ('.exe' if utils.GetPlatform() == 'win' else '')
  golang_path = os.path.join('go', 'bin', golang_binary)

  golang_env = os.environ.copy()
  golang_env['GOROOT'] = os.path.abspath('go')
  golang_env['GOPATH'] = os.path.abspath(golang_workspace)
  golang_env['PATH'] += os.pathsep + os.path.abspath('mercurial')
  subprocess.check_call([golang_path, 'get', 'collidermain'],
                        env=golang_env)
  subprocess.check_call([golang_path, 'build', 'collidermain'],
                        env=golang_env)

if __name__ == '__main__':
  sys.exit(main())

