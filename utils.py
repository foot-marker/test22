#!/usr/bin/python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Utilities for all our deps-management stuff."""

import hashlib
import os
import shutil
import sys
import subprocess
import tarfile
import time
import zipfile


def RunSubprocessWithRetry(cmd):
  """Invokes the subprocess and backs off exponentially on fail."""
  for i in range(5):
    try:
      subprocess.check_call(cmd)
      return
    except subprocess.CalledProcessError as exception:
      backoff = pow(2, i)
      print 'Got %s, retrying in %d seconds...' % (exception, backoff)
      time.sleep(backoff)

  print 'Giving up.'
  raise exception


def DownloadFilesFromGoogleStorage(path):
  print 'Downloading files in %s...' % path

  extension = 'bat' if 'win32' in sys.platform else 'py'
  cmd = ['download_from_google_storage.%s' % extension,
         '--bucket=chromium-webrtc-resources',
         '--auto_platform',
         '--recursive',
         '--directory', path]
  subprocess.check_call(cmd)


def ComputeSHA1(path):
  if not os.path.exists(path):
    return 0

  sha1 = hashlib.sha1()
  file_to_hash = open(path, 'rb')
  try:
    sha1.update(file_to_hash.read())
  finally:
    file_to_hash.close()

  return sha1.hexdigest()


# Code partially copied from
# https://cs.chromium.org#chromium/build/scripts/common/chromium_utils.py
def RemoveDirectory(*path):
  """Recursively removes a directory, even if it's marked read-only.

  Remove the directory located at *path, if it exists.

  shutil.rmtree() doesn't work on Windows if any of the files or directories
  are read-only, which svn repositories and some .svn files are.  We need to
  be able to force the files to be writable (i.e., deletable) as we traverse
  the tree.

  Even with all this, Windows still sometimes fails to delete a file, citing
  a permission error (maybe something to do with antivirus scans or disk
  indexing).  The best suggestion any of the user forums had was to wait a
  bit and try again, so we do that too.  It's hand-waving, but sometimes it
  works. :/
  """
  file_path = os.path.join(*path)
  if not os.path.exists(file_path):
    return

  if sys.platform == 'win32':
    # Give up and use cmd.exe's rd command.
    file_path = os.path.normcase(file_path)
    for _ in xrange(3):
      print 'RemoveDirectory running %s' % (' '.join(
          ['cmd.exe', '/c', 'rd', '/q', '/s', file_path]))
      if not subprocess.call(['cmd.exe', '/c', 'rd', '/q', '/s', file_path]):
        break
      print '  Failed'
      time.sleep(3)
    return
  else:
    shutil.rmtree(file_path, ignore_errors=True)


def DeleteDirNextToGclient(directory):
  # Sanity check to avoid nuking the wrong dirs.
  if not os.path.exists('.gclient'):
    raise Exception('Invoked from wrong dir; invoke from dir with .gclient')
  print 'Deleting %s in %s...' % (directory, os.getcwd())
  RemoveDirectory(directory)


def UnpackToWorkingDir(archive_path):
  extension = os.path.splitext(archive_path)[1]
  if extension == '.zip':
    _Unzip(archive_path)
  else:
    _Untar(archive_path)


def _Unzip(path):
  print 'Unzipping %s in %s...' % (path, os.getcwd())
  zip_file = zipfile.ZipFile(path)
  try:
    zip_file.extractall()
  finally:
    zip_file.close()


def _Untar(path):
  print 'Untarring %s in %s...' % (path, os.getcwd())
  tar_file = tarfile.open(path, 'r:gz')
  try:
    tar_file.extractall()
  finally:
    tar_file.close()


def GetPlatform():
  if sys.platform.startswith('win'):
    return 'win'
  if sys.platform.startswith('linux'):
    return 'linux'
  if sys.platform.startswith('darwin'):
    return 'mac'
  raise Exception("Can't run on platform %s." % sys.platform)

