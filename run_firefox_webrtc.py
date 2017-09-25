#!/usr/bin/env python
# Copyright 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Launches Firefox and browses to an URL."""

import os
import signal
import sys

from optparse import OptionParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
THIRD_PARTY_DIR = os.path.abspath(os.path.join(BASE_DIR, 'third_party'))

sys.path.append(os.path.join(THIRD_PARTY_DIR, 'manifestdestiny'))
sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozinfo'))
sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozprocess'))
sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozprofile'))
sys.path.append(os.path.join(THIRD_PARTY_DIR, 'mozrunner'))

from mozprofile import profile
import mozrunner

WEBRTC_PREFERENCES = {
    # Automatically gives permission to access the camera/microphone and
    # bypasses the permission/selection dialog.
    'media.navigator.permission.disabled': True,
}

def main():
  usage = 'usage: %prog --binary <firefox_executable> --webpage <url>'
  parser = OptionParser(usage)
  parser.add_option('-b', '--binary',
                    help=('Firefox executable to run.'))
  parser.add_option('-w', '--webpage',
                    help=('Web page to browse to.'))
  options, _args = parser.parse_args()
  if not options.binary:
    parser.error('You must specify the Firefox browser executable.')
  if not options.webpage:
    parser.error('You must specify the web page to browse to.')

  firefox_profile = profile.FirefoxProfile(preferences=WEBRTC_PREFERENCES)
  firefox_runner = mozrunner.FirefoxRunner(profile=firefox_profile,
                                           binary=options.binary,
                                           cmdargs=[options.webpage])
  def KillFirefox(signum, frame):
    firefox_runner.stop()
  signal.signal(signal.SIGTERM, KillFirefox)

  firefox_runner.start()

  # Run until Chrome kills us.
  firefox_runner.process_handler.wait(timeout=600)
  return 0

if __name__ == '__main__':
  sys.exit(main())
