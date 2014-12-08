#!/usr/bin/python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Downloads the appengine SDK from WebRTC storage and unpacks it.

Requires that depot_tools is installed and in the PATH. This script expects
to run with Chrome's base dir as the working directory, e.g. where the .gclient
file is. This is what should happen if this script is invoked as a hook action.
"""

import glob
import os
import sys
import subprocess

import utils

def _DownloadResources(webrtc_deps_path):
  print 'Downloading files in %s...' % webrtc_deps_path

  extension = 'bat' if 'win32' in sys.platform else 'py'
  cmd = ['download_from_google_storage.%s' % extension,
         '--bucket=chromium-webrtc-resources',
         '--directory', webrtc_deps_path]
  subprocess.check_call(cmd)


def _StripVersionNumberFromMercurialFolder():
  unpacked_name = glob.glob('mercurial*')
  assert len(unpacked_name) == 1, 'Should have precisely one mercurial!'
  os.rename(unpacked_name[0], 'mercurial')


def main(argv):
  if len(argv) == 1:
    return 'Usage: %s <path to webrtc.DEPS>' % argv[0]

  webrtc_deps_path = argv[1]
  appengine_zip_path = os.path.join(webrtc_deps_path, 'google-appengine.zip')
  old_appengine_sha1 = utils.ComputeSHA1(appengine_zip_path)

  mercurial_tar_path = os.path.join(webrtc_deps_path, 'mercurial-src.tar.gz')
  old_mercurial_sha1 = utils.ComputeSHA1(mercurial_tar_path)

  _DownloadResources(webrtc_deps_path)

  if old_appengine_sha1 != utils.ComputeSHA1(appengine_zip_path):
    utils.DeleteDirNextToGclient('google_appengine')
    utils.UnpackToWorkingDir(appengine_zip_path)

  if old_mercurial_sha1 != utils.ComputeSHA1(mercurial_tar_path):
    utils.DeleteDirNextToGclient('mercurial')
    utils.UnpackToWorkingDir(mercurial_tar_path)
    _StripVersionNumberFromMercurialFolder()

if __name__ == '__main__':
  sys.exit(main(sys.argv))
