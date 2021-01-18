
 * CloudWatch Logs 에 저장된 로그를 S3로 이동한느 log export 작업을 생성하는 람다함수.

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
aws cloudformation deploy --template-file template-generated.yaml --stack-name CloudWatchLogsToS3 --capabilities CAPABILITY_IAM
```
 * 참고
   * sam deploy ... 형식의 명령으로도 실행 가능

# debugging deploy failure
```
aws cloudformation describe-stack-events --stack-name CloudWatchLogsToS3
```

# application delete
```
aws cloudformation delete-stack --stack-name CloudWatchLogsToS3
```
  * 참고 
    * --capabilities <= make available to create IAM

# local execute
```
sam local invoke cbtestapi -e event.json
sam local invoke cbtestapi
```
 * 참고 
   * -e JSON file containing event data passed to the Lambda function.
   *  This command will run our HelloWorldFunction function code inside hello-world/app.js, pass the content of the event.json into it and give the following output at the end:


# local debug
```
sam local invoke -d 9999 CloudWatchLogsToS3APILog
```
 * 참고 
   * -d debug port


# export task를 확인
```
aws logs describe-export-tasks --task-id 11a80538-3cd9-40b0-ae88-f1da9b912f33
```
