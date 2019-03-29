import os, subprocess, datetime

def release():
    #make sure git is clean
    en = input("Please Make sure your git repository in clean(y/n)")
    if en.upper == 'Y':
        input("Please enter your")
    else:
        print("Exit release process")

    #TODO: clean PRJ patch

    gen_SHA256('release.py')

    edit_releaseNode()


def gen_SHA256(filepath):
    #generate SHA256
    return subprocess.check_output(['sha256sum', filepath], shell=True)
    
def get_versionNum(PRJpath):


#clean config/patch and update PRJ(include FW version)


def edit_releaseNode():
    #edit release node
    filename = os.path.join('..', 'ReleaseNode')
    with open(filename, 'a') as f:
        f.write('==========================================================================\n')
        f.write('Version number: ' + )
        f.write('Release Date: ' + datetime.datetime.now().strftime('%Y-%m-%d') + '\n')
        f.write('SHA256 checksum:\n' + str(gen_SHA256('rom.ima'), 'utf-8'))

#create HPM

#git add

#git add tag

#push to git

if __name__ == '__main__':
    release()