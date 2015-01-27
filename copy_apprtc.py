#!/usr/bin/python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Moves Apprtc to the out/ directory, where the browser test can find it.

This copy will resolve symlinks on all platforms, which is useful for Apprtc
since it uses symlinks for its common javascript files (and Windows does not
understand those symlinks).
"""

import os
import shutil

import utils

if __name__ == '__main__':
  target_dir = os.path.join('src', 'out', 'webrtc-samples')
  if utils.GetPlatform() is 'win':
    # Work around the fact that node_modules create ridiculously long paths.
    # Unfortunately shutil will choke on those on Windows, but not rmdir.
    os.system('rmdir /s /q %s' % target_dir)
  else:
    shutil.rmtree(target_dir, ignore_errors=True)
  shutil.copytree('webrtc-samples',
                  target_dir, ignore=shutil.ignore_patterns('.svn', '.git'))
  apprtc_subdir = os.path.join('samples', 'web', 'content', 'apprtc')

  # This file is symlinked on windows, so copy it since win doesn't understand
  # symlinks.
  shutil.copyfile(os.path.join('webrtc-samples', 'samples', 'web',
                               'js', 'adapter.js'),
                  os.path.join(target_dir, apprtc_subdir, 'js', 'adapter.js'))
