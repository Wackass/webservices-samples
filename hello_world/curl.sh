#!/bin/bash

curl -X GET --header 'Accept: application/json' \
 'http://rw:rw@mpstack.wic.openenglab.netapp.com:8081/devmgr/v2/storage-systems' | \
  python -m json.tool











