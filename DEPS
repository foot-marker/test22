# DEPS file that pulls down dependencies that are needed to build and
# execute WebRTC specific tests from a Chromium checkout.

vars = {
  'git_url':
     'https://chromium.googlesource.com'
}

deps = {
  # TODO(kjellander): Replace the AppRTC location with a GoB mirror as soon as
  # crbug.com/455758 is resolved.
  'apprtc':
    'https://github.com/webrtc/apprtc.git',
  'webrtc.DEPS/third_party/manifestdestiny':
    Var('git_url') + '/chromium/deps/manifestdestiny.git@46ae53ac463e23bfefec374a81806355ea598ac4',
  'webrtc.DEPS/third_party/mozdownload':
    Var('git_url') + '/chromium/deps/mozdownload.git@dcb2344c8f16caae7762c4557d08f2eca536a40a',
  'webrtc.DEPS/third_party/mozinfo':
    Var('git_url') + '/chromium/deps/mozinfo.git@f4cc257e21c48bc33dc1d12123d934a4dcaa120c',
  'webrtc.DEPS/third_party/mozprocess':
    Var('git_url') + '/chromium/deps/mozprocess.git@11d11bebc8517dcedec71f377cbec07fb91a3b1f',
  'webrtc.DEPS/third_party/mozprofile':
    Var('git_url') + '/chromium/deps/mozprofile.git@313295a0d9e1687dafa58e12f1f01b093a136446',
  'webrtc.DEPS/third_party/mozrunner':
    Var('git_url') + '/chromium/deps/mozrunner.git@efb11330692424f7aa5533839b0ae728bc5f30d1',
}

hooks = [
  {
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_appengine_and_mercurial.py",
                "webrtc.DEPS"],
  },
  {
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_golang.py",
                "webrtc.DEPS"],
  },
  {
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_node.py",
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
    # Build the AppRTC App Engine Application.
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/build_apprtc_appengine_app.py"],
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
               "src/chrome/test/data/webrtc/resources/tools"],
  },
  {
    # Download firefox for the Firefox AppRTC test.
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_firefox_nightly.py",
                "--clean-old-firefox-archives",
                "--target-dir",
                "firefox-nightly"],
  },
]
