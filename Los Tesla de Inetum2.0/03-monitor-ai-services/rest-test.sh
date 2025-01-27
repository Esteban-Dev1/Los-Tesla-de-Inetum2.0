#!/bin/bash

# URL and headers for cUrl
URL="https://azure-ai-lab-02.cognitiveservices.azure.com/language/:analyze-text?api-version=2023-04-01"
CONTENT_TYPE="Content-Type: application/json"
SUBSCRIPTION_KEY="Ocp-Apim-Subscription-Key: 9558abbec17d4d17a211260a1b2c92d4"
DATA="{'analysisInput':{'documents':[{'id':1,'text':'hello'}]}, 'kind': 'LanguageDetection'}"

# loop to run curl 20 times
for i in {1..20}
do
  echo "Executing request $i..."
  curl -X POST "$URL" -H "$CONTENT_TYPE" -H "$SUBSCRIPTION_KEY" --data-ascii "$DATA"
done