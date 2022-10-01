#!/bin/bash

# Constants
VERSION=$1
PACKAGE_NAME="crypto-place-trades-$VERSION.tar.gz"
APP_PACKAGE_FOLDER="dist"
APP_FOLDER="$HOME/App/crypto-place-trades"

echo "Start deploy app: $PACKAGE_NAME to $APP_FOLDER"
rm -rf "$APP_FOLDER/crypto-place-trades-$VERSION"
mkdir -p $APP_FOLDER
cp "$APP_PACKAGE_FOLDER/$PACKAGE_NAME" "$APP_FOLDER"
cd "$APP_FOLDER" || exit 1
tar -xvzf "$PACKAGE_NAME"
echo "Finished deploy app"
