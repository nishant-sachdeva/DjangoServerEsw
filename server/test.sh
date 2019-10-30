#! /bin/bash


curl http://127.0.0.1:8000/reading/ \
 -X POST \
 -H "Content-Type: application/json" \
 -H "Accept: text/html,application/json" \
 -H "X-CSRFToken: af5iRIkWvOejjvZk4U3gTvGFWJ4tpkDiaFaBt85iftdVEOCEKeJGuIDk4GzvqeSS" \
 -H "Cookie: csrftoken=af5iRIkWvOejjvZk4U3gTvGFWJ4tpkDiaFaBt85iftdVEOCEKeJGuIDk4GzvqeSS" \
 -d '{"value":45979791 , "status":0}'


