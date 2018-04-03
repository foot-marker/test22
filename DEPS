# DEPS file that pulls down dependencies that are needed to build and
# execute WebRTC specific tests from a Chromium checkout.

hooks = [
  {
    "pattern": ".",
    "action" : ["python",
                "src/third_party/webrtc/rtc_tools/testing/setup_apprtc.py",
                "src/out"],
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
