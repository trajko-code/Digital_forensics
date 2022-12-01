#!/bin/bash

CURRENT_PATH=$(pwd)
SCRIPT_PATH=$(dirname $(realpath ${BASH_SOURCE:-$0}))
CONTENT_PROVIDER_PATH="$SCRIPT_PATH/../ContentProviderApp"

cd "$CONTENT_PROVIDER_PATH"

./gradlew assembleDebug

cd $CURRENT_PATH
