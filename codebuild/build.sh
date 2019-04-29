#!/bin/bash

#To simplify dealing with codebuild and codepipeline quirks, this script is executed in the build segment of code build.

echo "project_name="$project_name
source $project_name/bin/activate

echo "Building Layer"
python3 build-layer.py
echo "Finished building Layer"

deactivate