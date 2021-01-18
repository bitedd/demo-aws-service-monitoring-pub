

 * AWS에서 발생하는 전체적인 이벤트들을 수신해서 가시성을 높이기 위한 CloudFormation + Lambda

# Libraries
```
mkdir packages
python -m pip install -r requirements.txt -t ./packages/
```


# Packaging
```
aws cloudformation package  --s3-bucket  bucket-name --template-file template.yaml --output-template-file template-generated.yaml
```

# Create ChangeSet
```
aws cloudformation create-change-set --stack-name arn:aws:cloudformation:ap-northeast-2:xxxxxxxxxxxx:stack/AwsEvent/06240770-dae2-11ea-834a-061aa88a6b90 --change-set-name ChangeSet200819-1 --use-previous-template --parameters $(cat template-parameter.json | jq -r '.[] | .ParameterKey + \"=\" + .ParameterValue') 

$(cat template-parameter.json | jq -r '.[] | \"ParameterKey=\" + .ParameterKey + \",\"  + \"ParameterValue=\" + .ParameterValue')
```

# Listing ChnageSets
```
aws cloudformation list-change-sets --stack-name arn:aws:cloudformation:ap-northeast-2:xxxxxxxxxxxx:stack/AwsEvent/06240770-dae2-11ea-834a-061aa88a6b90
```

# Describe ChangeSets
```
aws cloudformation describe-change-set --change-set-name arn:aws:cloudformation:us-east-1:123456789012:changeSet/SampleChangeSet/1a2345b6-0000-00a0-a123-00abc0abc000
```

# Executing ChangeSets
```
aws cloudformation execute-change-set --change-set-name arn:aws:cloudformation:us-east-1:123456789012:changeSet/SampleChangeSet/1a2345b6-0000-00a0-a123-00abc0abc000
```

# Deploy
```
aws cloudformation deploy --template-file template-generated.yaml --stack-name AwsEvent --parameter-overrides $(cat template-parameter.json | jq -r '.[] | .ParameterKey + \"=\" + .ParameterValue')  --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND
```


# local execute (lambda)
```
sam local invoke LambdaSendNotificationToSlack -e event/event-01.json
sam local invoke LambdaSendNotificationToSlack
```
 * 참고 
   * -e JSON file containing event data passed to the Lambda function.
   *  This command will run our HelloWorldFunction function code inside hello-world/app.js, pass the content of the event.json into it and give the following output at the end:

# local execute (all)
 * use start-api like this
```
sam local invoke start-api --parameter-overrides ParameterKey=Key1,ParameterValue=value1 ParameterKey=Key2,ParameterValue=value2 ??
```

# Deletion
```
aws cloudformation delete --stack-name AwsEvent
```

