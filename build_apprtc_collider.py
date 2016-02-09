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
import tempfile

import utils


def main():
  apprtc_dir = os.path.join('apprtc', 'src')
  golang_workspace = os.path.join('src', 'out', 'go-workspace')
  utils.RemoveDirectory(golang_workspace)

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

  # Delete everything in the workspace except the build artifacts.
  go_bin_dir = os.path.join(golang_workspace, 'bin')
  tmp_dir = tempfile.mkdtemp()
  shutil.move(go_bin_dir, tmp_dir)
  shutil.rmtree(golang_workspace)
  shutil.move(os.path.join(tmp_dir, 'bin'), go_bin_dir)
  os.rmdir(tmp_dir)

if __name__ == '__main__':
  sys.exit(main())

