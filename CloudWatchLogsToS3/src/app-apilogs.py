import boto3
import collections
from datetime import datetime, timedelta
import math
import time
import os
import dateutil.tz


timeZoneSeoul = dateutil.tz.gettz('Asia/Seoul')

region = 'ap-northeast-2'
def lambda_handler(event, context):
    log_file = boto3.client('logs')
    nDays = 4

    #print(datetime.now(timeZoneSeoul))
    saveLogDate = datetime.now(timeZoneSeoul) - timedelta(days=nDays)
    #print(datetime.now(timeZoneSeoul) - timedelta(days=nDays))

    startHourOfDay = saveLogDate.replace(hour=0, minute=0, second=0, microsecond=0)
    endHourOfDay = saveLogDate.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    print (saveLogDate)
    print (startHourOfDay)
    print (endHourOfDay)
    
    group_name = ['svcpeaking']
    for x in group_name:
        response = log_file.create_export_task(
         taskName='export_task_CloudWatchLogsToS3APILog',
         logGroupName=x,
         fromTime=math.floor(startHourOfDay.timestamp() * 1000), 
         to=math.floor(endHourOfDay.timestamp() * 1000), 
         destination='logs.servicename',
         destinationPrefix='log-export'
        )
