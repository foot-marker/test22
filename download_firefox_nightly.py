#!/usr/bin/env python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Downloads a Firefox Nightly build for the current platform."""

import datetime
import glob
import os
import shutil
import sys
import subprocess
import tarfile
import time
import zipfile

from optparse import OptionParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THIRD_PARTY_DIR = os.path.abspath(os.path.join(BASE_DIR, 'third_party'))

sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozdownload'))
sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozinfo'))

from mozdownload import scraper


def _Touch(a_file):
  with open(a_file, 'a'):
    os.utime(a_file, None)


def _GetFirefoxArchivesSortedOnModifiedDate(target_dir):
  firefox_archives = glob.glob(os.path.join(target_dir, '*tar.bz2'))
  if not firefox_archives:
    return None

  firefox_archives.sort(key=os.path.getmtime, reverse=True)
  return firefox_archives


def _CleanOldFirefoxArchives(target_dir): 
  firefox_archives = _GetFirefoxArchivesSortedOnModifiedDate(target_dir)
  if not firefox_archives or len(firefox_archives) < 2:
    return

  # Keep the newest archive around as a fallback build and delete the rest.
  rest = firefox_archives[1:]
  print 'About to delete old Firefox archives %s.' % rest
  for old_archive in rest:
    try:
      os.remove(old_archive)
    except OSError:
      pass


def _FindFallbackFirefoxBuild(target_dir):
  firefox_archives = _GetFirefoxArchivesSortedOnModifiedDate(target_dir)
  if not firefox_archives:
    return None

  newest_build = firefox_archives[0]
  build_age_seconds = time.time() - os.path.getmtime(newest_build)
  build_age_days = datetime.timedelta(seconds=build_age_seconds).days

  return newest_build, build_age_days


def _MaybeDownload(target_dir, force):
  try:
    downloader = scraper.DailyScraper(directory=target_dir, version=None)
    filename = downloader.build_filename(downloader.binary)
    firefox_archive = os.path.join(target_dir, filename)

    if os.path.exists(firefox_archive) and not force:
      # Touch the file anyway since we were 'successful', so we can accurately
      # compute the age of the most recent download attempt and act accordingly
      # when a download fails later.
      _Touch(firefox_archive)
      print 'Skipping download as %s is already downloaded.' % firefox_archive
      return None

    downloader.download()
    print 'Downloaded %s' % firefox_archive
    return firefox_archive
  except scraper.NotFoundException as exception:
    print 'Failed to download firefox: %s.' % exception
    fallback_build, age_days = _FindFallbackFirefoxBuild(target_dir)

    if not fallback_build:
      raise Exception('We failed to download Firefox and we have no builds to '
                      'fall back on; failing...')
    if age_days > 3:
      raise Exception('We have failed to download firefox builds for more '
                      'than 3 days now: failing so someone looks at it. The '
                      'most recent build we have is %d days old.' % age_days)

    print 'Using %s instead; it is %d days old.' % (fallback_build, age_days)
    return fallback_build


def _ExtractArchive(firefox_archive, target_dir):
  # TODO(phoglund): implement on win/mac. See http://crbug.com/454303.
  if sys.platform == 'darwin':
    print "Disabled on mac..."
    return 0
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
    print "Disabled on win..."
    return 0
    zip_archive = zipfile.ZipFile(firefox_archive)
    zip_archive.extractall(path=target_dir)
  else:
    print >> sys.stderr, 'Unsupported platform: %s' % sys.platform
    return 1

  print 'Extracted %s' % firefox_archive
  return 0


def main():
  usage = 'usage: %prog -t <target_dir>'
  parser = OptionParser(usage)
  parser.add_option('-t', '--target-dir',
                    help=('Target directory to put the downloaded and extracted'
                          ' folder with the Firefox Nightly build in.'))
  parser.add_option('-f', '--force', action='store_true',
                    help=('Force download even if the current nightly is '
                          'already downloaded.'))
  parser.add_option('-c', '--clean-old-firefox-archives', action='store_true',
                    help=('Clean old firefox archives; one will always be '
                          'kept as a fallback.'))
  options, _args = parser.parse_args()
  if not options.target_dir:
    parser.error('You must specify the target directory.')

  target_dir = options.target_dir
  if not os.path.isdir(target_dir):
    os.mkdir(target_dir)

  firefox_archive = _MaybeDownload(target_dir, options.force)
  if firefox_archive:
    return _ExtractArchive(firefox_archive, target_dir)

  if options.clean_old_firefox_archives:
    _CleanOldFirefoxArchives(target_dir)

if __name__ == '__main__':
  sys.exit(main())
