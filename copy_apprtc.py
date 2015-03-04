#!/usr/bin/python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Moves Apprtc to the out/ directory, where the browser test can find it."""

import fileinput
import os
import shutil
import sys

import utils


def _ConfigureApprtcServerToDeveloperMode(app_yaml_path):
  if not os.path.exists(app_yaml_path):
    return 'Expected app.yaml at %s.' % os.path.abspath(app_yaml_path)

  for line in fileinput.input(app_yaml_path, inplace=True):
    # We can't click past these in the firefox interop test, so
    # disable them.
    line = line.replace('BYPASS_JOIN_CONFIRMATION: false',
                        'BYPASS_JOIN_CONFIRMATION: true')
    sys.stdout.write(line)


def main():
  target_dir = os.path.join('src', 'out', 'apprtc')
  if utils.GetPlatform() is 'win':
    # Windows shutil can't handle the long node.js paths when deleting;
    # work around the problem.
    os.system('rmdir /s /q %s' % target_dir)
  else:
    shutil.rmtree(target_dir, ignore_errors=True)
  shutil.copytree('apprtc',
                  target_dir, ignore=shutil.ignore_patterns('.svn', '.git'))

  app_yaml_path = os.path.join(target_dir, 'src', 'app_engine', 'app.yaml')
  _ConfigureApprtcServerToDeveloperMode(app_yaml_path)


if __name__ == '__main__':
  sys.exit(main())

