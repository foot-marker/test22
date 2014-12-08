#!/usr/bin/python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Downloads the golang SDK from WebRTC storage and unpacks it.

Requires that depot_tools is installed and in the PATH. This script expects
to run with Chrome's base dir as the working directory, e.g. where the .gclient
file is. This is what should happen if this script is invoked as a hook action.
"""

import os
import subprocess
import sys
import tarfile
import zipfile

import utils


def _DownloadFilesFromGoogleStorage(webrtc_deps_path):
  print 'Downloading files in %s...' % webrtc_deps_path

  extension = 'bat' if 'win32' in sys.platform else 'py'
  cmd = ['download_from_google_storage.%s' % extension,
         '--bucket=chromium-webrtc-resources',
         '--auto_platform',
         '--recursive',
         '--directory', webrtc_deps_path]
  subprocess.check_call(cmd)


def _GetGoArchivePathForPlatform():
  archive_extension = 'zip' if utils.GetPlatform() == 'win' else 'tar.gz'
  return os.path.join(utils.GetPlatform(), 'go.%s' % archive_extension)


def main(argv):
  if len(argv) == 1:
    return 'Usage: %s <path to webrtc.DEPS>' % argv[0]
  if not os.path.exists('.gclient'):
    return 'Invoked from wrong dir; invoke from dir with .gclient'

  webrtc_deps_path = argv[1]
  golang_path = os.path.join(webrtc_deps_path, 'golang')
  archive_path = os.path.join(golang_path, _GetGoArchivePathForPlatform())
  old_archive_sha1 = utils.ComputeSHA1(archive_path)

  _DownloadFilesFromGoogleStorage(golang_path)

  if old_archive_sha1 != utils.ComputeSHA1(archive_path):
    utils.DeleteDirNextToGclient('go')
    utils.UnpackToWorkingDir(archive_path)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
