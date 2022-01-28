#!/bin/bash
DIRNAME=$(pwd)

TEAM_NAME=$(sed -e 's/^"//' -e 's/"$//' <<<"$(jq '.[] | select(.ParameterKey=="team") | .ParameterValue' ${DIRNAME}/parameters.json)")
APPLICATION=$(sed -e 's/^"//' -e 's/"$//' <<<"$(jq '.[] | select(.ParameterKey=="application") | .ParameterValue' ${DIRNAME}/parameters.json)")
STACK=$(sed -e 's/^"//' -e 's/"$//' <<<"$(jq '.[] | select(.ParameterKey=="stack") | .ParameterValue' ${DIRNAME}/parameters.json)")
CHILD_ACCOUNT=$(sed -e 's/^"//' -e 's/"$//' <<<"$(aws ssm get-parameter --name /IBK/${APPLICATION}/${ENV}/AccountId --query "Parameter.Value")")

declare -A S3_BUCKET

S3_BUCKET[dev]="sdlf-cfn-artifacts-pipeline-us-east-1-058528764918-bucket"
S3_BUCKET[test]="sdlf-cfn-artifacts-pipeline-us-east-1-204453042683-bucket"
S3_BUCKET[prod]="sdlf-cfn-artifacts-pipeline-us-east-1-195034049652-bucket"

PREFIX=IBK-${TEAM_NAME}-${APPLICATION}-${STACK}


mkdir ./output
aws cloudformation package \
 --template-file $DIRNAME/template.yaml \
 --s3-bucket  ${S3_BUCKET[$ENV]} \
 --s3-prefix $PREFIX \
 --output-template-file $DIRNAME/output/packaged-template.yaml --no-verify-ssl
 
echo "Checking if stack exists ..."
STACK_NAME=IBK-${TEAM_NAME}-${APPLICATION}-cross-${ENV}
if ! aws cloudformation describe-stacks --stack-name ${STACK_NAME}; then
  echo -e "Stack does not exist, creating ..."
  aws cloudformation create-stack \
    --stack-name ${STACK_NAME} \
    --parameters \
        ParameterKey=childAccountId,ParameterValue="${CHILD_ACCOUNT}" \
        ParameterKey=enviroment,ParameterValue="${ENV}" \
        ParameterKey=team,ParameterValue="${TEAM_NAME}" \
        ParameterKey=application,ParameterValue="${APPLICATION}" \
        ParameterKey=stack,ParameterValue="${STACK}" \
    --template-body file://${DIRNAME}/template.yaml \
    --tags file://${DIRNAME}/tags.json \
    --capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"
  echo "Waiting for stack to be created ..."
  aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME}
else
  echo -e "Stack exists, attempting update ..."
  aws cloudformation update-stack \
    --stack-name $STACK_NAME \
    --parameters \
        ParameterKey=childAccountId,ParameterValue="${CHILD_ACCOUNT}" \
        ParameterKey=enviroment,ParameterValue="${ENV}" \
        ParameterKey=team,ParameterValue="${TEAM_NAME}" \
        ParameterKey=application,ParameterValue="${APPLICATION}" \
        ParameterKey=stack,ParameterValue="${STACK}" \
    --template-body file://${DIRNAME}/template.yaml \
    --tags file://${DIRNAME}/tags.json \
    --capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"
  set -e
  echo "Waiting for stack update to complete ..."
  aws cloudformation wait stack-update-complete \
    --stack-name $STACK_NAME
  echo "Finished create/update successfully!"
fi
