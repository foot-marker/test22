#!/usr/bin/python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Downloads the appengine SDK from WebRTC storage and unpacks it.

Requires that depot_tools is installed and in the PATH. This script expects
to run with Chrome's base dir as the working directory, e.g. where the .gclient
file is. This is what should happen if this script is invoked as a hook action.
"""

import hashlib
import os
import shutil
import sys
import subprocess
import zipfile


def _DownloadAppEngineZipFile(webrtc_deps_path):
  print 'Downloading files in %s...' % webrtc_deps_path

  extension = 'bat' if 'win32' in sys.platform else 'py'
  cmd = ['download_from_google_storage.%s' % extension,
         '--bucket=chromium-webrtc-resources',
         '--directory', webrtc_deps_path]
  subprocess.check_call(cmd)


def _ComputeSHA1(path):
  if not os.path.exists(path):
    return 0

  sha1 = hashlib.sha1()
  file_to_hash = open(path, 'rb')
  try:
    sha1.update(file_to_hash.read())
  finally:
    file_to_hash.close()

  return sha1.hexdigest()


# This is necessary since Windows won't allow us to unzip onto an existing dir.
def _DeleteOldAppEngineDir():
  app_engine_dir = 'google_appengine'
  print 'Deleting %s in %s...' % (app_engine_dir, os.getcwd())
  shutil.rmtree(app_engine_dir, ignore_errors=True)


def _Unzip(path):
  print 'Unzipping %s in %s...' % (path, os.getcwd())
  zip_file = zipfile.ZipFile(path)
  try:
    zip_file.extractall()
  finally:
    zip_file.close()


def main(argv):
  if len(argv) == 1:
    return 'Usage: %s <path to webrtc.DEPS>' % argv[0]

  webrtc_deps_path = argv[1]
  zip_path = os.path.join(webrtc_deps_path, 'google-appengine.zip')
  old_zip_sha1 = _ComputeSHA1(zip_path)

  _DownloadAppEngineZipFile(webrtc_deps_path)

  if old_zip_sha1 != _ComputeSHA1(zip_path):
    _DeleteOldAppEngineDir()
    _Unzip(zip_path)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
