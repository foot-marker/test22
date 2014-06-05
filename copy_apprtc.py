#!/usr/bin/python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Moves Apprtc to the out/ directory, where the browser test can find it.

This copy will resolve symlinks on all platforms, which is useful for Apprtc
since it uses symlinks for its common javascript files (and Windows does not
understand those symlinks).
"""

import shutil


if __name__ == '__main__':
  web_samples_dir = 'webrtc-samples/samples/web'
  shutil.rmtree('src/out/apprtc', ignore_errors=True)
  shutil.copytree(web_samples_dir + '/content/apprtc',
                  'src/out/apprtc', ignore=shutil.ignore_patterns('.svn'))
  shutil.copyfile(web_samples_dir + '/js/adapter.js',
		  'src/out/apprtc/js/adapter.js')
