import os, subprocess, datetime, sys

if 'linux' in subprocess.check_output(['uname']).lower():
    call_py = 'python'
else:
    call_py = 'python2'


def release(HPMfolder_path):
    #make sure git is clean
    en = raw_input("Please Make sure your git repository in clean(y/n)")
    if en.upper() != 'Y':
        print("Exit release process")
        exit()

    #get PRJ name
    patch_PRJ, PRJ = get_PRJ_name()

    #clean PRJ patch
    #clear_PRJ_patch(patch_PRJ, PRJ)

    #update FW version
    cur_FW_ver = get_cur_FW_ver(PRJ)
    print(cur_FW_ver)

    #gen_SHA256('release.py')

    #edit_releaseNode()


def gen_SHA256(filepath):
    #generate SHA256
    return subprocess.check_output(['sha256sum', filepath], shell=True)
    
def clear_PRJ_patch(patch_PRJ, PRJ):
    #update PRJ
    subprocess.call([call_py, 'patch_prj.py'])

    #clean config/patch
    subprocess.call(['rm', os.path.join('..', 'configs', 'patch', '*')])

    #replate origin .PRJ file to patched .PRJ file
    subprocess.call(['mv', patch_PRJ, PRJ])

def get_PRJ_name():
    PRJ = ''
    patch_PRJ = ''
    confing_folder = os.path.join('..', 'configs')
    for filename in os.listdir(confing_folder):
        if filename.endswith('_patch.PRJ'):
            patch_PRJ = os.path.join(confing_folder, filename)
            PRJ = os.path.join(confing_folder, filename[:-10] + '.PRJ') 
    if not patch_PRJ:
        print("Error: can't find patched .PRJ file")
        exit()
    return patch_PRJ, PRJ 

def get_cur_FW_ver(PRJ_path):
    FW_ver = ''
    with open(PRJ_path, 'r') as f:
        for line in f.readlines():
            if 'CONFIG_SPX_MAP_WOLFPASS_ATTR_Major' in line:
                FW_ver += line.split('=')[1].replace('"', '').replace('\n', '') + '.'
            elif 'CONFIG_SPX_MAP_WOLFPASS_ATTR_Minor' in line:
                FW_ver += line.split('=')[1].replace('"', '').replace('\n', '') + '.'
            elif 'CONFIG_SPX_MAP_WOLFPASS_ATTR_Aux' in line:
                FW_ver += line.split('=')[1].replace('"', '').replace('\n', '')
    return FW_ver

def edit_releaseNode():
    #edit release node
    filename = os.path.join('..', 'ReleaseNode')
    with open(filename, 'a') as f:
        f.write('==========================================================================\n')
        f.write('Version number: ')
        f.write('Release Date: ' + datetime.datetime.now().strftime('%Y-%m-%d') + '\n')
        f.write('SHA256 checksum:\n' + str(gen_SHA256('rom.ima')))

#create HPM

#git add

#git add tag

#push to git

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''
        * Usage: use following command and change 'PATH' to your CreateHPM folder path
        python rlease.py PATH
        ''')
    elif not os.path.isdir(sys.argv[1]):
        print('Error: Invalud path')
    elif 'private.pem' not in os.listdir(sys.argv[1]) or 'rom.ima' not in os.listdir(sys.argv[1]):
        print("Error: Can't find 'private.pem' or 'rom.ima' in provided folder path")
    else:
        release(sys.argv[1])