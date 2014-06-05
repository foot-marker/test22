# DEPS file that pulls down dependencies that are needed to build and
# execute WebRTC Android tests from a Chromium checkout.

vars = {
  "chromium_git": "https://chromium.googlesource.com",
  # Use this googlecode_url variable only if there is an internal mirror for it.
  # If you do not know, use the full path while defining your new deps entry.
  "googlecode_url": "http://%s.googlecode.com/svn",
}

deps = {
  "webrtc-samples":
    Var("chromium_git") + "/external/webrtc-samples.git",
  "webrtc.DEPS/third_party/manifestdestiny":
    "/trunk/deps/third_party/manifestdestiny@240893",
  "webrtc.DEPS/third_party/mozdownload":
    "/trunk/deps/third_party/mozdownload@240893",
  "webrtc.DEPS/third_party/mozinfo":
    "/trunk/deps/third_party/mozinfo@240893",
  "webrtc.DEPS/third_party/mozprocess":
    "/trunk/deps/third_party/mozprocess@240893",
  "webrtc.DEPS/third_party/mozprofile":
    "/trunk/deps/third_party/mozprofile@240893",
  "webrtc.DEPS/third_party/mozrunner":
    "/trunk/deps/third_party/mozrunner@240893",
}

deps_os = {
  "android": {
    "src/data":
      (Var("googlecode_url") % "webrtc") + "/trunk/data",
    "src/resources":
      (Var("googlecode_url") % "webrtc") + "/trunk/resources",
    "src/third_party/gflags":
      (Var("googlecode_url") % "webrtc") + "/trunk/third_party/gflags",
    "src/third_party/gflags/src":
      "http://gflags.googlecode.com/svn/trunk/src@84",
  },
}

hooks = [
  {
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_appengine_sdk.py",
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
    # Download test resources, i.e. video and audio files from Google Storage.
    # These resources are used by the Android bots.
    "pattern": "\\.sha1",
    "action": ["download_from_google_storage",
               "--directory",
               "--recursive",
               "--num_threads=10",
               "--bucket", "chromium-webrtc-resources",
               "src/resources"],
  },
  {
    # Download media files and tools used by the webrtc quality browser tests,
    # chrome/browser/media/chrome_webrtc_audio_quality_browsertest.cc and
    # chrome/browser/media/chrome_webrtc_video_quality_browsertest.cc.
    "pattern": "\\.sha1",
    "action": ["download_from_google_storage",
               "--directory",
               "--recursive",
               "--num_threads=10",
               "--bucket", "chromium-webrtc-resources",
               "src/chrome/test/data/webrtc/resources"],
  },
  {
    # Download firefox for the Firefox AppRTC test.
    "pattern": ".",
    "action" : ["python",
                "webrtc.DEPS/download_firefox_nightly.py",
                "-t",
                "firefox-nightly"],
  },
]
