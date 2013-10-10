# DEPS file that pulls down dependencies that are needed to build and 
# execute WebRTC Android tests from a Chromium checkout.

vars = {
  # Use this googlecode_url variable only if there is an internal mirror for it.
  # If you do not know, use the full path while defining your new deps entry.
  "googlecode_url": "http://%s.googlecode.com/svn",
}

deps = {
  "src/third_party/webrtc_apprtc":
    "https://webrtc.googlecode.com/svn/trunk/samples/js",
}

deps_os = {
  "android": {
    "src/data": 
      (Var("googlecode_url") % "webrtc") + "/trunk/data",
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
]
