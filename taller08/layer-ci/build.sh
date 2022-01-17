#!/bin/bash

echo "testing"
ls 

LAYER_NAME="layerpip"
ENV="dev"
PARAMETER_NAME="/RPA/Lambda/Layer-pip/Version"


echo $LAYER_NAME
echo $PARAMETER_NAME

mkdir -p layer/python
pip  install -q -r ./layer-ci/requirements.txt  -t layer/python
cd layer/

zip -r layer.zip python/ -x \*__pycache__\*
#dir_name=$(echo "${dir//.\/}")
echo "Uploading Lambda Layer as ......"
set +e
layer=$(aws lambda publish-layer-version --layer-name $LAYER_NAME --description "Contains the libraries specified in requirements.txt" --compatible-runtimes "python3.6" "python3.7" "python3.9" --zip-file fileb://./layer.zip --no-verify-ssl)
echo "----------------------------" $layer
latest_layer_version=$(echo $layer | jq -r .LayerVersionArn)
aws ssm put-parameter --name $PARAMETER_NAME --value $latest_layer_version --type String --overwrite --no-verify-ssl