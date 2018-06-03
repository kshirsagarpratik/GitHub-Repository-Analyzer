import os
import re
import subprocess
import generateJson
import json
import requests


def clone(clone_path, url):
    try:
        p = subprocess.call(['git', 'clone', url], cwd=clone_path, shell=True) # clone repo
    # p.wait()
    except Exception as e:
        print("Something went wrong in cloning")


def checkout(dir, sha):
    print(dir, sha)
    try:
        p = subprocess.call(['git', 'checkout', 'master'], cwd=dir, shell=True) # checkout master
        # p.wait()
        p = subprocess.call(['git', 'checkout', sha], cwd=dir, shell=True) # checkout commit other than HEAD.
    # p.wait()
    except Exception as e:
        print("Something went wrong in Checking out.")


def iterate():
    try:
        output = []
        for oldindex, newindex in zip(range(0, len(reversedsha) - 1), range(1, len(reversedsha))):
            checkout(futureold, reversedsha[oldindex])
            checkout(futurenew, reversedsha[newindex])
            os.system('und create -db new.udb -languages java')  # create understand database for newer version
            os.system('und create -db old.udb -languages java')  # create understand database for older version

            os.system('und -db new.udb add ' + os.path.join(os.getcwd(), 'new', 'java'))  # add/update newer version
            os.system('und -db old.udb add ' + os.path.join(os.getcwd(), 'old', 'java'))  # add/update older version

            try:
                os.system('und -quiet analyze new.udb')  # analyze udb to add files into the udb object.
                os.system('und -quiet analyze old.udb')
            except Exception as e:
                print("Cannot analyze data!")

            olddb_path = os.path.join(os.getcwd(), 'old.udb') # paths of new and old understand db's.
            newdb_path = os.path.join(os.getcwd(), 'new.udb')
            try:
                json_data = generateJson.generatejson(newdb_path, olddb_path) # generate json file containing modifications from old version to new version.
                output.append(json_data)
            except Exception as e:
                print("Cannot generate json")

        json_pretty = json.dumps(output, indent=4) # attempt to make JSON structure more readable.
        with open('output.txt', 'w') as outfile:
            outfile.write(json_pretty)



        # return (olddb, newdb)	# causing function to quit.
        # print(reversedsha[oldindex], "old")
        # create old udb by checkout, add & analyse
        # print(os.getcwd())
        # print(reversedsha[newindex], "new")
        # create new udb by checkout, add & analyse
    except Exception as e:
        print("Something went wrong with Versioning the source code.")


payload = {'state': 'closed'}    # to get only those pull requests which are closed.
r = requests.get('https://api.github.com/repos/structurizr/java/pulls', auth=('', ''), params=payload) # GitHub REST API for getting pull requests.
shafile = open('sha.txt', 'w+')
os.system('mkdir patches') # making new directories for versions and patch files.
os.system('mkdir old')
os.system('mkdir new')

repo_url = ''
for pr in r.json():
    if pr['merged_at'] is None:     # Taking only those PRs which have been Closed and Merged too.
        continue
    patch_number = pr['number']     # The PR Number
    patch_url = pr['patch_url']     # The Patch URL
    patch_HEAD_SHA = pr['head']['sha']      # SHA of the commit/merge
    shafile.write(patch_HEAD_SHA)
    shafile.write('\n')
    print('Number = '+str(patch_number),'URL = '+patch_url,'HEAD SHA = '+patch_HEAD_SHA)
    patch = requests.get(patch_url, auth=('', '')) # Take input here from user.
    file = open(os.path.join(os.getcwd(), 'patches', str(patch_number)+'.patch'), 'w+')
    file.write(patch.text)
    file.close()

    # get repo url from r.json
    if not repo_url:
        repo_url = pr['base']['repo']['clone_url']

shafile.close()
shafile = open('sha.txt', 'r')  # list of commit SHAs stored in sha.txt
readsha = shafile.readlines()
reversedsha = readsha[::-1]
# sorting SHAs in ascending order of Pull Requests
for sha in reversedsha:
    sha = re.sub('\n', '', sha)  # removing newline char

oldindex = range(0, len(reversedsha) - 1)
newindex = range(1, len(reversedsha))

# clone the repo
clone(os.path.join(os.getcwd(), 'new'), repo_url)
clone(os.path.join(os.getcwd(), 'old'), repo_url)

try:
    current = os.getcwd()  # current working directory
    futurenew = os.path.join(current, 'new', 'java')
    # print(futurenew)
    futureold = os.path.join(current, 'old', 'java')
except Exception as e:
    print("Could not set versions of src.")

iterate()
