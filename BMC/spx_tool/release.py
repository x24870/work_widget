import os, subprocess, datetime, sys, glob

if 'linux' in subprocess.check_output(['uname']).lower():
    call_py = 'python'
else:
    call_py = 'python2'

class Releaser():
    def __init__(self):
        self.FW_ver = {'major': None, 'minor': None, 'aux': None}
        self.SHA256 = ''

    def release(self, HPMfolder_path):
        #Check list
        en = raw_input('''
        Please check following items:
        1. Make sure your git repository is clean
        2. Update FW version in PRJ file
        3. Copy rom.ima, private.pem to CreateHPM folder
        
        I finished all items above (y/n):
        ''')
        if en.upper() != 'Y':
            print("Exit release process")
            exit()

        #get PRJ name
        patch_PRJ, PRJ = self.get_PRJ_name()

        #clean PRJ patch
        self.clear_PRJ_patch(patch_PRJ, PRJ)

        #Get FW version
        self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux'] = self.get_cur_FW_ver(PRJ)
        print("\nFW version: ${}$.${}$.${}$".format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux']))

        #edit .conf for create HPM
        #self.edit_HPM_conf(HPMfolder_path)

        #create HPM
        #self.create_HPM()

        #generate SHA256 code
        self.SHA256 = self.gen_SHA256(os.path.join(HPMfolder_path, 'rom.ima'))#TODO: make sure returned string is specified
        print('SHA256: {}'.format(self.SHA256))

        #edit ReleasNode
        self.edit_releaseNode()

        #git commit
        self.git_commit()

        #git add tag
        self.git_add_tag()

        #finish
        print('Finish!\nNow you can edit ReleaseNode and push to remote Git')
        
    def clear_PRJ_patch(self, patch_PRJ, PRJ):
        #update PRJ
        subprocess.call([call_py, 'patch_prj.py'])

        #clean config/patch
        for f in glob.glob(os.path.join('..', 'configs', 'patch', '*')):
            os.remove(f)

        #replate origin .PRJ file to patched .PRJ file
        subprocess.call(['mv', patch_PRJ, PRJ])

    def get_PRJ_name(self):
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

    def get_cur_FW_ver(self, PRJ_path):
        major, minor, aux = '', '', ''
        with open(PRJ_path, 'r') as f:
            for line in f.readlines():
                if 'CONFIG_SPX_MAP_WOLFPASS_ATTR_Major' in line:
                    major = line.split('=')[1].replace('"', '').replace('\n', '').replace(' ', '').replace('\t', '')
                    major = major.split('#')[0]#prevent patch_prj.py tag
                elif 'CONFIG_SPX_MAP_WOLFPASS_ATTR_Minor' in line:
                    minor = line.split('=')[1].replace('"', '').replace('\n', '').replace(' ', '').replace('\t', '')
                    minor = minor.split('#')[0]#prevent patch_prj.py tag
                elif 'CONFIG_SPX_MAP_WOLFPASS_ATTR_Aux' in line:
                    aux = line.split('=')[1].replace('"', '').replace('\n', '').replace(' ', '').replace('\t', '')
                    aux = aux.split('#')[0]#prevent patch_prj.py tag
        return major, minor, aux

    def edit_releaseNode(self):
        if len(self.FW_ver['major']) == 1:
            self.FW_ver['major'] = '0' + self.FW_ver['major']
        if len(self.FW_ver['minor']) == 1:
            self.FW_ver['minor'] = '0' + self.FW_ver['minor']
        if len(self.FW_ver['aux']) == 1:
            self.FW_ver['aux'] = '0' + self.FW_ver['aux']
        filename = os.path.join('..', 'ReleaseNode')

        ori_node = None
        with open(filename, 'r') as f:
            ori_node = f.readlines()

        with open(filename, 'a') as f:
            #firset line
            f.write(ori_node[0])

            #new releasNode content
            f.write('==========================================================================\n')
            f.write('Release Date: {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
            f.write('Version number: {}.{}.{}\n'.format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux']))
            f.write('SHA256 checksum: {}\n'.format(self.SHA256))
            f.write('''Note:

Add feature list:

Fix bug:\n\n''')

            #old releaseNode content
            for line in ori_node[1:]:
                f.write(line)

    def edit_HPM_conf(self, HPMfolder_path):
        #TODO: use correct conf filename
        HPMconf = 'signedImage.conf'
        if HPMconf not in os.listdir(HPMfolder_path):
            print("Error: Can't find '{}' in '{}'".format(HPMconf, HPMfolder_path))

        with open(HPMconf, 'w') as f:
            #TODO: edit HPMconf
            pass
                   
    def create_HPM(self):
        subprocess.call(['./CreateHPMImage', 'create', 'signedHPM.conf'])#TODO: use correct file name

    def gen_SHA256(self, filepath):
        #generate SHA256
        print(filepath)
        return subprocess.check_output(['sha256sum', filepath])

    def git_commit(self):
        subprocess.call(['git', 'rm', os.path.join('..', 'configs', 'patch', '*')])
        subprocess.call(['git', 'add', os.path.join('..', 'ReleaseNode')])
        subprocess.call(['git', 'commit', '-m', 
        '"Release Firmware version: {}.{}.{}"'.format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux'])])

    def git_add_tag(self):
        subprocess.call([
            'git', 
            'tag',
            'Release_ver_{}.{}.{}'.format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux']),
            'HEAD'
            ])

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
        rlsr = Releaser()
        rlsr.release(sys.argv[1])