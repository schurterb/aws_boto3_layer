#!/usr/bin/env python
# coding: utf-8

import json
import boto3
import os

"""
@param functionName  name of the lambda function to invoke
@param eventData     data to pass to the lambda function
"""
def invokeLambdaFunction(functionName, eventData):
    
    #Write data to a text file
    with open("tmp.txt", 'w') as wf:
        json.dump(eventData, wf)
    
    with open("tmp.txt", 'rb') as rbf:
        lambda_client = boto3.client('lambda')
        invoke_response = lambda_client.invoke(FunctionName=functionName,
                                               LogType='Tail',
                                               Payload=rbf,
                                               InvocationType='RequestResponse')
                                               
    os.remove("tmp.txt")
    return invoke_response

"""
"""
def createLambdaFunction(name, zipfile, **kwargs):
    
    lambda_client = boto3.client('lambda')
    with open(zipfile, 'rb') as f:
        create_response = lambda_client.create_function(
            FunctionName=name,
            Runtime=kwargs.get('runtime', 'python3.6'),
            Role=kwargs.get('role', 'arn:aws:iam::353290830413:role/lambda_test_role'),
            Handler=kwargs.get('handler', 'main.handler'),
            Code=dict( ZipFile=f.read(), ),
            Description=kwargs.get('description', name),
            Timeout=kwargs.get('timeout', 300),
            Layers=kwargs.get("layers",[])
            )

    return create_response
                        

"""
"""
def updateLambdaFunction(name, zipfile, **kwargs):
    
    lambda_client = boto3.client('lambda')
    with open(zipfile, 'rb') as f:
        update_response = lambda_client.update_function_code(
            FunctionName=name,
            ZipFile=f.read(),
            Publish=kwargs.get('publish', True),
            DryRun=kwargs.get('dry_run', False)
            )
                        
    return update_response

"""
"""
def createOrUpdateLambdaLayer(name, zipfile, **kwargs):
    
    lambda_client = boto3.client('lambda')
    with open(zipfile, 'rb') as f:
        response = lambda_client.publish_layer_version(
            LayerName=name,
            Description=kwargs.get('description', name),
            Content=dict( ZipFile=f.read() ),
            CompatibleRuntimes=kwargs.get('runtimes', []),
            LicenseInfo=kwargs.get('license', "")
            )
    return response