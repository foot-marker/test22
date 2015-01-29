#!/usr/bin/python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Moves Apprtc to the out/ directory, where the browser test can find it.

This copy will resolve symlinks on all platforms, which is useful for Apprtc
since it uses symlinks for its common javascript files (and Windows does not
understand those symlinks).
"""

import fileinput
import os
import shutil
import sys

import utils


def _ConfigureApprtcServerToDeveloperMode(apprtc_dir):
  app_yaml_path = os.path.join(apprtc_dir, 'app.yaml')
  if not os.path.exists(app_yaml_path):
    return 'Expected app.yaml at %s.' % os.path.abspath(app_yaml_path)

  for line in fileinput.input(app_yaml_path, inplace=True):
    # We can't click past these in the firefox interop test, so
    # disable them.
    line = line.replace('BYPASS_JOIN_CONFIRMATION: false',
                        'BYPASS_JOIN_CONFIRMATION: true')
    sys.stdout.write(line)


def _CopyApprtcToTargetDir(target_dir, apprtc_subdir):
  shutil.rmtree(target_dir, ignore_errors=True)
  shutil.copytree('webrtc-samples',
                  target_dir, ignore=shutil.ignore_patterns('.svn', '.git'))

  # This file is symlinked on windows, so copy it since win doesn't understand
  # symlinks.
  shutil.copyfile(os.path.join('webrtc-samples', 'samples', 'web',
                               'js', 'adapter.js'),
                  os.path.join(target_dir, apprtc_subdir, 'js', 'adapter.js'))


def main():
  target_dir = os.path.join('src', 'out', 'webrtc-samples')
  apprtc_subdir = os.path.join('samples', 'web', 'content', 'apprtc')
  _CopyApprtcToTargetDir(target_dir, apprtc_subdir)
  _ConfigureApprtcServerToDeveloperMode(os.path.join(target_dir, apprtc_subdir))

if __name__ == '__main__':
  sys.exit(main())

