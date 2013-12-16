#!/usr/bin/env python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Downloads a Firefox Nightly build for the current platform."""

import os
import shutil
import sys
import subprocess
import tarfile
import zipfile

from optparse import OptionParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THIRD_PARTY_DIR = os.path.abspath(os.path.join(BASE_DIR, 'third_party'))

sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozdownload'))
sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozinfo'))

from mozdownload import scraper


def main():
  usage = 'usage: %prog -t <target_dir>'
  parser = OptionParser(usage)
  parser.add_option('-t', '--target-dir',
                    help=('Target directory to put the downloaded and extracted'
                          ' folder with the Firefox Nightly build in.'))
  parser.add_option('-f', '--force', action='store_true',
                    help=('Force download even if the current nightly is '
                          'already downloaded.'))
  options, _args = parser.parse_args()
  if not options.target_dir:
    parser.error('You must specify the target directory.')

  target_dir = options.target_dir
  if not os.path.isdir(target_dir):
    os.mkdir(target_dir)

  downloader = scraper.DailyScraper(directory=target_dir, version=None)
  firefox_archive = os.path.join(target_dir,
                                 downloader.build_filename(downloader.binary))

  if os.path.exists(firefox_archive) and not options.force:
    print 'Skipping download as %s is already downloaded.' % firefox_archive
    return 0

  downloader.download()
  print 'Downloaded %s' % firefox_archive

  # Extract the archive.
  if sys.platform == 'darwin':
    volume = '/Volumes/Nightly'
    firefox_executable = '%s/FirefoxNightly.app' % target_dir

    # Unmount any previous downloads.
    subprocess.call(['hdiutil', 'detach', volume])

    subprocess.check_call(['hdiutil', 'attach', firefox_archive])
    shutil.copytree('%s/FirefoxNightly.app' % volume, firefox_executable)
    subprocess.check_call(['hdiutil', 'detach', volume])
  elif sys.platform == 'linux2':
    tar_archive = tarfile.open(firefox_archive, 'r:bz2')
    tar_archive.extractall(path=target_dir)
  elif sys.platform == 'win32':
    zip_archive = zipfile.ZipFile(firefox_archive)
    zip_archive.extractall(path=target_dir)
  else:
    print >> sys.stderr, 'Unsupported platform: %s' % sys.platform
    return 1
  
  print 'Extracted %s' % firefox_archive
  return 0

if __name__ == '__main__':
  sys.exit(main())
