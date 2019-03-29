#! /bin/bash

echo "Customer Name: ABC"
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/computers | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p' 
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/mobiledevices | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p'

echo "Customer Name: 123"
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/computers | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p' 
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/mobiledevices | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p'

echo "Customer Name: XYZ"
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/computers | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p' 
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/mobiledevices | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p'

echo "Customer Name: 789"
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/computers | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p' 
curl -s -u myuser:mypassword https://myserver.jamfcloud.com/JSSResource/mobiledevices | sed -n -e 's/.*<size>\(.*\)<\/size>.*/\1/p'


