#!/usr/bin/env python
# coding: utf-8

import os
from zipfile import ZipFile
from sh import mkdir, cp, rm, ls

from buildtools import createOrUpdateLambdaLayer

lambdaLayers = {}
resourceZipDirectories = {}


#Create a lambda layer for boto3
name = "boto3"
sourceDir = "aws_boto3_layer/lib/python3.6/site-packages/"

#TODO: find smoother way to do this
sources = str(ls(sourceDir)).split()
elementsToRemove = ["__pycache__", "docutils"]
for source in sources:
    if "-info" in source:
        elementsToRemove.append(source)
for element in elementsToRemove:
    sources.remove(element)

resourceZipDirectory = "python/"

print("Creating lambda layer for "+name+" with "+str(sources))

#Create a place to put the resources while zipping them.
mkdir("-p", resourceZipDirectory)
for source in sources:
    cp("-rf", sourceDir+source, resourceZipDirectory)
    
with ZipFile(name+".zip", 'w') as ziph:
    for root, dirs, files in os.walk(resourceZipDirectory):
        for file in files:
            ziph.write(os.path.join(root, file))
            
response = createOrUpdateLambdaLayer(name, name+".zip", runtimes=['python3.6','python3.7'])
print(response)

print("Finished creating lambda layer")

rm("-rf", resourceZipDirectory)
