import requests
from xml.etree import ElementTree as ET
import sys

print("Script Starting...")
print("")

# Set the following constants specific to Salesforce Environment
username = sys.argv[1]
password = sys.argv[2]
url = "https://login.salesforce.com/services/Soap/c/42.0"
security_token = "YOURTOKENHERE"

# No changes required below
headers = {'content-type': 'text/xml;charset=UTF-8', 'SOAPAction': 'login'}
body = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:enterprise.soap.sforce.com">
   <soapenv:Body>
      <urn:login>
         <urn:username>""" + username + """</urn:username>
         <urn:password>""" + password + security_token + """</urn:password>
      </urn:login>
   </soapenv:Body>
</soapenv:Envelope>"""

# Call the login method
response = requests.post(url, data=body, headers=headers)
xml = response.content

# Parse the response
root = ET.fromstring(xml)

# Print the complete response
print("Salesforce Response ==> ")
ET.dump(root)
print("")

# Print few attributes
print("User Name ==> " + root.find('.//{urn:enterprise.soap.sforce.com}userFullName').text)
print("User Email ==> " + root.find('.//{urn:enterprise.soap.sforce.com}userEmail').text)
print("")

print("Script Completed")
