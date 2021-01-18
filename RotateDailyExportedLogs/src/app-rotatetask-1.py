import boto3
import collections
from datetime import datetime, timedelta
import math
import time
import os
import dateutil.tz
import re


timeZoneSeoul = dateutil.tz.gettz('Asia/Seoul')

LOG_BUCKET_NAME='logs.servicename'
LOG_BUCKET_PREFIX_NAME='log-export'
region = 'ap-northeast-2'
def lambda_handler(event, context):
    exportTaskIDs = set({})
    taskIDHashs = {}
    log_file = boto3.client('logs')

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(LOG_BUCKET_NAME)

    exportTaskPattern = '\w{8}-\w{4}-\w{4}-\w{4}-\w{12}'
    exportTaskPatternCompiled = re.compile(exportTaskPattern)

    exported_log_filenames = get_file_list_s3(LOG_BUCKET_NAME, LOG_BUCKET_PREFIX_NAME)
    for keys in exported_log_filenames:
        strTok = keys.split("/")
        if len(strTok) <= 1:
            continue

        taskID = strTok[1]
        matchedAddr = exportTaskPatternCompiled.match(taskID)
        if matchedAddr:
            exportTaskIDs.add(taskID)
        else:
            print('No match', taskID)
        
    for el in exportTaskIDs:
        response = log_file.describe_export_tasks(
                taskId=el,
                statusCode='COMPLETED'
                )

        fromts = math.floor(response['exportTasks'][0]['from'] / 1000)
        tots = math.floor(response['exportTasks'][0]['to'] / 1000)

        dt_object = datetime.fromtimestamp(fromts, timeZoneSeoul)


        dateFormat = dt_object.strftime("%Y%m%d")
        year = dt_object.strftime("%Y")

        print(el, fromts, tots, year, dateFormat)
        taskIDHashs[el] = dateFormat


    #for taskIDhash in taskIDHashs:
    #    print(taskIDHashs[taskIDhash])

    
    for keys in exported_log_filenames:
        #print(keys)
        strTok = keys.split("/")
        if len(strTok) <= 3:
            continue

        taskID = strTok[1]
        logGroupName = strTok[2]
        fileName = strTok[3]
        matchedAddr = exportTaskPatternCompiled.match(taskID)
        if matchedAddr:
            newFileKey = taskIDHashs[taskID][0:4] + '/' + taskIDHashs[taskID] + '/' + logGroupName + fileName
            print(keys + '->' + newFileKey)
            s3.Object(LOG_BUCKET_NAME,  newFileKey).copy_from(CopySource=LOG_BUCKET_NAME + '/' + keys)       
            s3.Object(LOG_BUCKET_NAME,keys).delete()
        else:
            print('No match', taskID)



def get_file_list_s3(bucket, prefix="", file_extension=None):
    """Return the list of all file paths (prefix + file name) with certain type or all
            Parameters
            ----------
            bucket: str
                The name of the bucket. For example, if your bucket is "s3://my_bucket" then it should be "my_bucket"
            prefix: str
                The full path to the the 'folder' of the files (objects). For example, if your files are in 
                s3://my_bucket/recipes/deserts then it should be "recipes/deserts". Default : ""
            file_extension: str
                The type of the files. If you want all, just leave it None. If you only want "json" files then it
                should be "json". Default: None       
            Return
            ------
            file_names: list
                The list of file names including the prefix
            """
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket(bucket)
    file_objs = my_bucket.objects.filter(Prefix=prefix).all()
    #file_names = [file_obj.key for file_obj in file_objs if file_extension is not None and file_obj.key.split(".")[-1] == file_extension]
    file_names = [file_obj.key for file_obj in file_objs ]
    return file_names
