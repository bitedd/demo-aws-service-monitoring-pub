
 * 이 리포에 AWS 운영관련한 여러가지 도구를 커밋할 예정

 * bitedd/AWS/SAM 에 등록된 여러가지 유틸리티들을 정리하는 리포지토리.

```
_____AWSEvent
  |  AWS에서 발생하는 이벤트를 처리해서 Slack에 전송 처리하는 SAM 어플리케이션
  |__CloudWatchLogsToS3
  |  생성한 로그를 S3로 export하는 SAM 어플리케이션
  |__RotateDailyExpretedLogs
  |  Exported된 로그를 일별 로그로 로테이트 하는 SAM 어플리케이션
  |__SlackNotifier
     Slack에 발생한 이벤트 정보를 송신하는 SAM 어플리케이션
```
