#!/usr/bin/python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Builds a local mercurial (hg) copy.

This is used by the go toolchain.
"""

import os
import shutil
import subprocess
import sys

import utils


def main():
  if not os.path.exists('mercurial'):
    return 'Expected mercurial at %s.' % os.path.abspath('mercurial')

  os.chdir('mercurial')

  if utils.GetPlatform() == 'win':
    subprocess.check_call(['python', 'setup.py', '--pure', 'build_py', '-c',
                           '-d', '.', 'build_ext',
                           '-i', 'build_mo', '--force'])
    with open('hg.bat', 'w') as put_hg_in_path:
      # Write a hg.bat since the go toolchain expects to find something called
      # 'hg' in the path, but Windows only recognizes executables ending with
      # an extension in PATHEXT. Writing hg.bat effectively makes 'hg' callable
      # if the mercurial folder is in PATH.
      mercurial_path = os.path.abspath('hg')
      put_hg_in_path.write('python %s %%*' % mercurial_path)
  else:
    subprocess.check_call(['make', 'local'])

if __name__ == '__main__':
  sys.exit(main())
