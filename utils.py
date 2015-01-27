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
import zipfile


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


def DeleteDirNextToGclient(directory):
  # Sanity check to avoid nuking the wrong dirs.
  if not os.path.exists('.gclient'):
    raise Exception('Invoked from wrong dir; invoke from dir with .gclient')
  print 'Deleting %s in %s...' % (directory, os.getcwd())
  shutil.rmtree(directory, ignore_errors=True)


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

