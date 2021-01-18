
 * S3에 exported된 로그파일을 일자별로 관리하기 위한 람다함수.

# create an s3 bucket
```
aws s3 mb s3://sam-deploy
```

# package cloudformation 
```
aws cloudformation package  --s3-bucket sam-deploy --template-file template.yaml --output-template-file template-generated.yaml
```

 * 참고
   * sam package ... 형식의 명령으로도 실행 가능


# deploy 
```
aws cloudformation deploy --template-file template-generated.yaml --stack-name RotateDailyExportedLog --capabilities CAPABILITY_IAM
```

 * 참고
   * sam deploy ... 형식의 명령으로도 실행 가능


# debugging deploy failure
```
aws cloudformation describe-stack-events --stack-name RotateDailyExportedLog
```


# application delete
```
aws cloudformation delete-stack --stack-name RotateDailyExportedLog
```

  * 참고 
    * --capabilities <= make available to create IAM


# local execute
```
sam local invoke RotateLogTask1 -e event.json
sam local invoke RotateLogTask1
```

 * 참고 
   * -e JSON file containing event data passed to the Lambda function.
   *  This command will run our HelloWorldFunction function code inside hello-world/app.js, pass the content of the event.json into it and give the following output at the end:


# local debug
```
sam local invoke -d 9999 RotateLogTask1
```
 * 참고 
   * -d debug port


# export task를 확인
```
aws logs describe-export-tasks --task-id 11a80538-3cd9-40b0-ae88-f1da9b912f33
```


