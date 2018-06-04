# Import the modules
import subprocess, os, sys, base64, requests, json

class Consul():
    def seed(self):
        print("init")
        # Variables, likely to be set as env variable in chart
        #CONSUL_HOST = os.environ.get('KEY_THAT_MIGHT_EXIST')
        RELEASE_NAME = os.environ.get('RELEASE')
        RELEASE_NAME = RELEASE_NAME.upper()
        CONSUL_ENV_VAR = RELEASE_NAME + "_CONSUL_UI_SERVICE_HOST"
        CONSUL_HOST = os.environ.get(CONSUL_ENV_VAR)
        CONSUL_PORT = "8500"
        print(CONSUL_HOST)
        base_url = 'http://' + CONSUL_HOST + ':' + CONSUL_PORT
        search_params = '/v1/health/node/test'
        print(base_url + search_params)

        try:
            r = requests.get(base_url + search_params, timeout=0.5)
        except:
            print("exception: ", sys.exc_info()[0])
            sys.exit(1)

        if r.status_code == 200:
            # Read the Consul keys in array for iterating
            d = json.load(open('consul_keys.json', 'r'))
            # Create each key in the array
            for the_key, the_value in d.items():
                args = 'curl -X PUT -d @- http://'+CONSUL_HOST+':'+CONSUL_PORT+'/v1/kv/'+the_key+' <<< '+the_value
                subprocess.call(args, shell=True, executable='/bin/bash')
        else:
            print("I could not reach consul/vault")
            sys.exit(1)
