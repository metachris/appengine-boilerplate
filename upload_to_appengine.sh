#!/bin/bash

DIR=$( pwd )

function static_revert {
  # Set /static back to dev environment
  set -e
  echo "Setting /static back to /static_dev"
  cd app
  rm static
  ln -s static_dev static
  cd "$DIR"
  set +e
}

function static_toprod {
  # Set build script results as /static
  set -e
  echo "Setting /static to /static_dev/publish"
  cd app
  rm static
  ln -s static_dev/publish static
  cd "$DIR"
  set +e
}

function upload {
  # Upload to appengine
  ~/Tools/google_appengine/appcfg.py update app
}

function build {
  cd app/static_dev/build
  ant minify
  cd "$DIR"
}

read -p "Build the project with 'ant minify' now? [yN]" yn
  case $yn in
    [Yy]* ) build;;
    [Nn]* ) ;;
esac

static_toprod

read -p "You can now test the latest build. Do you wish to upload this version? [yN]" yn
  case $yn in
    [Yy]* ) upload;;
    [Nn]* ) ;;
esac

static_revert


