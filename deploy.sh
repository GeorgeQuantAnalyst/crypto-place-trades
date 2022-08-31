#!/bin/bash

# Constants
VERSION=$1
PACKAGE_NAME="phemex-futures-place-trades-$VERSION.tar.gz"
APP_PACKAGE_FOLDER="dist"
APP_FOLDER="$HOME/App/phemex-futures-place-trades/"

echo "Start deploy app: $PACKAGE_NAME to $APP_FOLDER"
mkdir -p $APP_FOLDER
cp "$APP_PACKAGE_FOLDER/$PACKAGE_NAME" "$APP_FOLDER"
cd "$APP_FOLDER" || exit 1
tar -xvzf "$PACKAGE_NAME"
echo "Finished deploy app"
