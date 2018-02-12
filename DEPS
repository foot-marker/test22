# DEPS file that pulls down dependencies that are needed to build and
# execute WebRTC specific tests from a Chromium checkout.

vars = {
  'git_url':
     'https://chromium.googlesource.com'
}

deps = {
  'webrtc.DEPS/third_party/requests/':
    Var('git_url') + '/external/github.com/kennethreitz/requests.git@2128321b85dfd969498e5d1636dcc3c4a27917ba'
}

hooks = [
  {
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_apprtc_appengine_and_mercurial.py",
                "webrtc.DEPS"],
  },
  {
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_golang.py",
                "webrtc.DEPS"],
  },
  {
    # "Build" AppRTC, i.e. move it to the out/ dir where the browser test
    # can find it. This is only done on runhooks.
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/copy_apprtc.py"],
  },
  {
    # Build Mercurial which is needed by the golang toolchain.
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/build_mercurial_local.py"],
  },
  {
    # Build AppRTC Collider using the golang toolchain.
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/build_apprtc_collider.py"],
  },
  {
    # Download media files and tools used by the webrtc quality browser tests,
    # chrome/browser/media/chrome_webrtc_audio_quality_browsertest.cc and
    # chrome/browser/media/chrome_webrtc_video_quality_browsertest.cc.
    "pattern": "\\.sha1",
    "action": ["download_from_google_storage",
               "--directory",
               "--num_threads=10",
               "--bucket", "chromium-webrtc-resources",
               "src/chrome/test/data/webrtc/resources"],
  },
  {
    # Download tools. If you're not a googler, you need to comment this out
    # and install the required tools yourself in the tools folder.
    "pattern": "\\.sha1",
    "action": ["download_from_google_storage",
               "--directory",
               "--num_threads=10",
               "--bucket", "chrome-webrtc-resources",
               "--auto_platform",
               "--recursive",
               "src/chrome/test/data/webrtc/resources/tools"],
  },
]
