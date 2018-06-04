# Import the modules
import subprocess, os, sys, base64, requests, json

class Vault():
    def seed(self):
        print("init")
        # Variables, likely to be set as env variable in chart
        #VAULT_HOST = os.environ.get('KEY_THAT_MIGHT_EXIST')
        RELEASE_NAME = os.environ.get('RELEASE')
        RELEASE_NAME_UCASE = RELEASE_NAME.upper()
        VAULT_ENV_VAR = RELEASE_NAME_UCASE + "_VAULT_UI_SERVICE_HOST"
        print(VAULT_ENV_VAR)
        VAULT_HOST = os.environ.get(VAULT_ENV_VAR)
        VAULT_PORT = "8200"
        print("vault host: " + VAULT_HOST)
        base_url = 'http://' + VAULT_HOST + ':' + VAULT_PORT
        search_params = '/v1/sys/health'
        print(base_url + search_params)
        os.environ["VAULT_ADDR"] = base_url

        try:
            r = requests.get(base_url + search_params, timeout=0.5)
        except:
            print("exception: ", sys.exc_info()[0])
            sys.exit(1)

        if r.status_code == 200:
            #Get Vault ROOT_TOKEN
            print ("getting vault token")
            pod_args = "kubectl get pods | grep "+RELEASE_NAME+"-vault | grep Running | awk '/-vault/ {print $1;exit}'"
            VAULT_POD = subprocess.check_output(pod_args, shell=True).strip().decode('utf-8')
            print(VAULT_POD)
            ROOT_TOKEN_ARGS = "kubectl logs "+VAULT_POD+" -c vault | awk '/Root Token/ { print $3 }'"
            ROOT_TOKEN = subprocess.check_output(ROOT_TOKEN_ARGS, shell=True).strip().decode('utf-8')
            print(ROOT_TOKEN)

            # Auth
            args="vault login "+ROOT_TOKEN
            subprocess.call(args, shell=True, executable='/bin/bash')

            # Read the Vault keys in array for iterating
            v = json.load(open('vault_keys.json', 'r'))
            # Create each key in the array
            for the_key, the_value in v.items():
                args = 'vault kv put '+the_key+' value='+the_value
                subprocess.call(args, shell=True, executable='/bin/bash')

        else:
            print("I could not reach vault")
            sys.exit(1)
