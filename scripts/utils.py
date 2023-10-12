import json
import subprocess

def getCredsString(region, secret):
    cmd = "/usr/local/bin/aws --region %s secretsmanager get-secret-value --secret-id %s" % (region, secret)
    s = json.loads(subprocess.Popen([cmd], shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode())
    credsjson = s["SecretString"]
    creds = json.loads(cjson)

    return creds

def getInfluxUser(region, secret):
    creds = getCredsString(region, secret)
    user = creds.value().split(":")[0]

    return user

def getInfluxPass(region, secret):
    creds = getCredsString(region, secret)
    password = creds.value().split(":")[1]

    return password
