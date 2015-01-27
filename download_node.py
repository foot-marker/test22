#!/usr/bin/python
# Copyright 2015 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Downloads the node binaries from WebRTC storage and unpacks it.

Requires that depot_tools is installed and in the PATH. This script expects
to run with Chrome's base dir as the working directory, e.g. where the .gclient
file is. This is what should happen if this script is invoked as a hook action.
"""

import glob
import os
import sys
import tarfile
import zipfile

import utils


def _GetNodeArchivePathForPlatform():
  archive_extension = 'zip' if utils.GetPlatform() == 'win' else 'tar.gz'
  return os.path.join(utils.GetPlatform(), 'node.%s' % archive_extension)


def _StripVersionNumberFromNodeDir():
  # The node dir will be called node-x-x-x.tar.gz, rename to just node.
  unpacked_name = glob.glob('node*')
  assert len(unpacked_name) == 1, 'Should have precisely one node!'
  os.rename(unpacked_name[0], 'node')


def main(argv):
  if len(argv) == 1:
    return 'Usage: %s <path to webrtc.DEPS>' % argv[0]
  if not os.path.exists('.gclient'):
    return 'Invoked from wrong dir; invoke from dir with .gclient'

  webrtc_deps_path = argv[1]
  node_path = os.path.join(webrtc_deps_path, 'node')
  archive_path = os.path.join(node_path, _GetNodeArchivePathForPlatform())
  old_archive_sha1 = utils.ComputeSHA1(archive_path)

  utils.DownloadFilesFromGoogleStorage(node_path)

  if (old_archive_sha1 != utils.ComputeSHA1(archive_path)
      or not os.path.exists('node')):
    utils.DeleteDirNextToGclient('node')
    utils.UnpackToWorkingDir(archive_path)
    _StripVersionNumberFromNodeDir()


if __name__ == '__main__':
  sys.exit(main(sys.argv))
