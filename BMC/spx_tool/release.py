import os, subprocess, datetime, sys, glob

REQUIRE_FILES = set(['private.pem', 'rom.ima', 'signimage.conf', 'CreateHPMImage'])

if 'linux' in subprocess.check_output(['uname']).lower():
    call_py = 'python'
else:
    call_py = 'python2'

class Releaser():
    def __init__(self):
        self.FW_ver = {'major': None, 'minor': None, 'aux': None}
        self.SHA256 = ''
        self.PRJName = ''

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

        #check if required files in specified folder
        self.check_required_files(HPMfolder_path)

        #get PRJ name
        patch_PRJ, PRJ = self.get_PRJ_name()
        self.PRJName = os.path.basename(PRJ)
        self.PRJName = self.PRJName.replace('_64.PRJ', '')
        self.PRJName = self.PRJName.replace('.PRJ', '')
        print(self.PRJName)

        #clean PRJ patch
        #self.clear_PRJ_patch(patch_PRJ, PRJ)

        #Get FW version
        self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux'] = self.get_cur_FW_ver(PRJ)
        print("\nFW version: {}.{}.{}".format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux']))

        #edit signimage.conf
        self.edit_HPM_conf(HPMfolder_path)

        #excute CreateHPMImage
        self.create_HPM(HPMfolder_path)

        #generate SHA256 code
        self.SHA256 = self.gen_SHA256(os.path.join(HPMfolder_path, 'rom.ima'))
        print('SHA256: {}'.format(self.SHA256))

        #edit ReleasNode
        self.edit_releaseNode()

        #git commit
        #self.git_commit(PRJ)

        #git add tag
        #self.git_add_tag()

        #finish
        print('Finish!\nNow you can edit ReleaseNode and push to remote Git')
        
    def clear_PRJ_patch(self, patch_PRJ, PRJ):
        #update PRJ
        subprocess.call([call_py, 'patch_prj.py'])

        #clean config/patch
        for f in glob.glob(os.path.join('..', 'configs', 'patch', '*')):
            os.remove(f)

        #replate origin .PRJ file to patched .PRJ file
        subprocess.call(['cp', patch_PRJ, PRJ])

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
                #TODO: use regex is better solution
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

        with open(filename, 'w') as f:
            #firset line
            f.write(ori_node[0])

            #new releasNode content
            f.write('==========================================================================\n')
            f.write('Release Date: {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
            f.write('Version number: {}.{}.{}\n'.format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux']))
            f.write('SHA256 checksum: {}\n'.format(self.SHA256))
            f.write('''Add feature list:

Fix bug:

Known issue:\n\n''')

            #old releaseNode content
            for line in ori_node[1:]:
                f.write(line)

    def edit_HPM_conf(self, HPMfolder_path):
        HPMconf = 'signimage.conf'
        if HPMconf not in os.listdir(HPMfolder_path):
            print("Error: Can't find '{}' in '{}'".format(HPMconf, HPMfolder_path))
            exit()

        new_context = []
        with open(os.path.join(HPMfolder_path, HPMconf), 'r') as f:
            for line in f.readlines():
                if line.strip().startswith('HPMImage'):
                    str1 = line.split('=')[0]
                    str2 = ('= ' + './' + self.PRJName + '_BMC_' + self.FW_ver['major'] + '_' + self.FW_ver['minor'] + '_' + 
                    datetime.datetime.now().strftime('%Y%m%d') + '.hpm' + '          ; Path & Filename of final output HPM Image\n')
                    line = str1 + str2
                elif line.strip().startswith('FwVersionMajor'):
                    str1 = line.split('=')[0]
                    str2 = '= ' + '0x' + self.FW_ver['major'] + "                              ; 1B This component's Major Version\n"
                    line = str1 + str2
                elif line.strip().startswith('FwVersionMinor'):
                    str1 = line.split('=')[0]
                    str2 = '= ' + '0x' + self.FW_ver['minor'] + "                              ; 1B This component's Major Version\n"
                    line = str1 + str2
                new_context.append(line)

        with open(os.path.join(HPMfolder_path, HPMconf), 'w') as f:
            for line in new_context:
                f.write(line)

                   
    def create_HPM(self, HPMfolder_path):
        excute_file = os.path.join(HPMfolder_path, './CreateHPMImage')
        conf_file = os.path.join(HPMfolder_path, 'signimage.conf')
        subprocess.call([excute_file, 'create', conf_file])

    def gen_SHA256(self, filepath):
        #generate SHA256
        print(filepath)
        sha256_str = subprocess.check_output(['sha256sum', filepath])
        sha256_str = ' '.join(sha256_str.split()[:-1]) + '    rom.ima\n'
        return sha256_str

    def git_commit(self, PRJ):
        subprocess.call(['git', 'rm', os.path.join('..', 'configs', 'patch', '*')])
        subprocess.call(['git', 'add', os.path.join('..', 'ReleaseNode')])
        subprocess.call(['git', 'add', os.path.join('..', 'configs', PRJ)])
        subprocess.call(['git', 'commit', '-m', 
        '"Release Firmware version: {}.{}.{}"'.format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux'])])

    def git_add_tag(self):
        subprocess.call([
            'git', 
            'tag',
            'Release_ver_{}.{}.{}'.format(self.FW_ver['major'], self.FW_ver['minor'], self.FW_ver['aux']),
            'HEAD'
            ])

    def check_required_files(self, path):
        files_in_folder = set(os.listdir(path))
        if REQUIRE_FILES & files_in_folder != REQUIRE_FILES:
            lacked_files = REQUIRE_FILES - files_in_folder
            print("Error: Can't find following files: {}".format(', '.join(lacked_files)))
            exit()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('''
        * Usage: use following command and change 'PATH' to your CreateHPM folder path
        python rlease.py PATH
        ''')
    elif not os.path.isdir(sys.argv[1]):
        print('Error: Invalud path')
    else:
        rlsr = Releaser()
        rlsr.release(sys.argv[1])
