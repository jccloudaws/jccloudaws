
sam build
sam local invoke Function  --event events/event.json

sam package --output-template-file taller02-template.yaml --s3-bucket rpa-cfn-artifacts-40888866-us-east-1
sam deploy --template-file taller02-template.yaml --stack-name rpa-capacitacion-cloud-aws-taller-lambda-02  --parameter-overrides ParameterKey=team,ParameterValue=rpa ParameterKey=stack,ParameterValue=lambda ParameterKey=environment,ParameterValue=dev ParameterKey=application,ParameterValue=taller02 --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM CAPABILITY_IAM