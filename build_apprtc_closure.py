#!/usr/bin/python
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Invokes the AppRTC closure compiler.

The AppRTC javascript code must be closure-compiled. This script uses
the node toolchain we downloaded earlier.
"""

import os
import shutil
import subprocess
import sys

import utils


def main():
  node_path = os.path.abspath('node')
  if not os.path.exists(node_path):
    return 'Expected node at %s.' % node_path
  samples_path = os.path.join('src', 'out', 'webrtc-samples')
  if not os.path.exists(samples_path):
    return 'Expected webrtc-samples at %s.' % os.path.abspath(samples_path)

  os.chdir(samples_path)
  
  if utils.GetPlatform() is 'win':
    npm_bin = os.path.join(node_path, 'npm.cmd')
    node_bin = os.path.join(node_path, 'node.exe')
  else:
    npm_bin = os.path.join(node_path, 'bin', 'npm')
    node_bin = os.path.join(node_path, 'bin', 'node')

  subprocess.check_call([npm_bin, 'install'])
  local_grunt_bin = os.path.join('node_modules', 'grunt-cli', 'bin', 'grunt')

  if not os.path.exists(local_grunt_bin):
    return ('Missing grunt-cli in the webrtc-samples checkout; did '
            'npm install fail?')

  subprocess.check_call([node_bin, local_grunt_bin, 'closurecompiler:debug'])


if __name__ == '__main__':
  sys.exit(main())
