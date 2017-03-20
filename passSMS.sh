#!/bin/sh
from=$SMS_1_NUMBER
message=$SMS_1_TEXT
reply=""

if test "$message" = "FHR"; then
    echo "Pong!"

else
    echo "Something Else!"