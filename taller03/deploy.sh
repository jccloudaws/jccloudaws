#!/bin/bash

ENV=$1

S3_BUCKET="rpa-cfn-artifacts-40888866-us-east-1"

aws s3 mb s3://rpa-cfn-artifacts-40888866-us-east-1

STACK_NAME="rpa-capacitacion-cloud-aws-taller-lambda-03"
REGION="us-east-1"
DIRNAME=$(dirname "$0")
PREFIX=RPA-TALLER-LAMBDA-03
#pip install -r requirements.txt -t ./src
#pip  install -q -r requirements.txt  -t src/python

mkdir ./output
aws cloudformation package \
 --template-file $DIRNAME/template.yaml \
 --s3-bucket ${S3_BUCKET} \
 --s3-prefix $PREFIX \
 --output-template-file $DIRNAME/output/packaged-template.yaml

out=$(aws cloudformation describe-stacks --region $REGION --stack-name $STACK_NAME)
echo $out
if [ -z "$out" ]; then
   echo -e "Stack not exist, creating ...!!"
   aws cloudformation create-stack \
        --stack-name ${STACK_NAME} \
        --parameters file://parameters-${ENV}.json \
        --template-body file://$DIRNAME/output/packaged-template.yaml \
        --tags file://tags-${ENV}.json \
        --capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"
        
   echo "Waiting for stack to be created ..."
   aws cloudformation wait stack-create-complete --stack-name ${STACK_NAME};
else
   echo -e "Stack exists, attempting update ..."
   set +e
   aws cloudformation update-stack \
      --stack-name $STACK_NAME \
      --parameters file://$DIRNAME/parameters-${ENV}.json \
      --template-body file://$DIRNAME/output/packaged-template.yaml \
      --tags file://$DIRNAME/tags-${ENV}.json \
      --capabilities "CAPABILITY_NAMED_IAM" "CAPABILITY_AUTO_EXPAND"
      
   set -e
   echo "Waiting for stack update to complete ..."
   aws cloudformation wait stack-update-complete --stack-name ${STACK_NAME};
   echo "Finished create/update successfully!"
fi
exit 0;