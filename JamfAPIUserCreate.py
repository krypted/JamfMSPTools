import requests
import sys
import base64

sys.argv = sys.argv[1:]

args_check = ["-username", "-password", "-URL", "-MSPpassword"]
args_n = 0

for arg in args_check:
      if(arg in sys.argv):
            args_n = args_n + 1

if(args_n != len(args_check)):
      print("You're missing argument(s)")
else:
      if(len(sys.argv) != len(args_check) * 2):
            print("You're missing argument(s) value")
      else:
            args = {
                  "username": sys.argv[sys.argv.index("-username") + 1],
                  "password": sys.argv[sys.argv.index("-password") + 1],
                  "url": sys.argv[sys.argv.index("-URL") + 1] + "/accounts/userid/0",
                  "MSPpassword": sys.argv[sys.argv.index("-MSPpassword") + 1]
            }

            xml = '''
                  <?xml version="1.0" encoding="UTF-8"?>
                  <account>
                        <name>JamfMSP</name>
                        <directory_user>false</directory_user>
                        <password>''' + args["MSPpassword"] + '''</password>
                        <enabled>Enabled</enabled>
                        <force_password_change>false</force_password_change>
                        <access_level>Full Access</access_level>
                        <privilege_set>Custom</privilege_set>
                        <privileges>
                        <jss_objects>
                        <privilege>Read Computers</privilege>
                        <privilege>Read Mobile Devices</privilege>
                        </jss_objects>
                        <jss_settings/>
                        <jss_actions/>
                        <recon/>
                        <casper_admin/>
                        <casper_remote/>
                        <casper_imaging/>
                        </privileges>
                  </account>'''
            headers = {
                  'Content-Type': 'application/xml',
                  "Authorization": "Basic {}".format(base64.b64encode(('{}:{}'.format(args["username"], args["password"]).encode("utf-8"))))
            }
            r = requests.post(args["url"], data=xml, headers=headers, auth=(args["username"], args["password"]))
            print(r)
