#!/bin/bash

CURRENT_PATH=$(pwd)
SCRIPT_PATH=$(dirname $(realpath ${BASH_SOURCE:-$0}))
CONTENT_PROVIDER_APK_PATH="$SCRIPT_PATH/../ContentProviderApp/app/build/outputs/apk/debug/app-debug.apk"

adb install $CONTENT_PROVIDER_APK_PATH
