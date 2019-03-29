#!/usr/bin/python

import shutil
import glob
import os
import sys
import hashlib

#package_path="../../Apache"
old_prj_path="../configs/CLCL_N_64.PRJ"
new_prj_path="../configs/CLCL_N_64_patch.PRJ"

def find_spx(data, spx):
  for idx in range(len(data)):
    if spx in data[idx]:
      return idx
  return -1

def file_as_bytes(file):
  with file:
    return file.read()

def patch_prj(old_prj, new_prj):
  if not os.path.isfile(old_prj):
    print "Can not find '%s'" % old_prj
    exit()

  #if not os.path.isdir(package_path):
    #print("Please pack Package or change Package path. Default:../../Apache")
  
  prj_file = open(old_prj, "r")
  prj_data = prj_file.readlines()
  prj_file.close()
  
  patch_files = sorted(glob.glob("../configs/patch/*"))
  for idx in range(len(patch_files)):
    patch_file = open(patch_files[idx], "r")
    patch_data = patch_file.readlines()
    patch_file.close()
    for idx2 in range(len(patch_data)):
      patch_line = patch_data[idx2]
      if patch_line[:1] == "+":
        if find_spx(prj_data, patch_line[1:-1]) != -1:
          print "It's aready select spx:" , patch_line[1:-1]
        else:
          print "Select   ", patch_line[1:-1]
          add = "\n" + patch_line[1:-1] + "			#PATCH_SELECTED"
          prj_data.append(add)
      if patch_line[:1] == "-":
        del_idx = find_spx(prj_data, patch_line[1:-1])
        if del_idx == -1:
          print "It's aready deselect spx:" , patch_line[1:-1]
        else:
          del prj_data[del_idx]
          print "deselect ", patch_line[1:-1]
  
  new_prj_file = open(new_prj, "w")
  for idx in range(len(prj_data)):
    if idx != 0:
      new_prj_file.write(prj_data[idx])
  new_prj_file.close()

  md5sum = hashlib.md5(file_as_bytes(open(new_prj, 'rb'))).hexdigest()
  prj_data[0] = "# Created and Signed by MDS : " + md5sum + "\n"
  
  new_prj_file = open(new_prj, "w")
  for idx in range(len(prj_data)):
    new_prj_file.write(prj_data[idx])
  new_prj_file.close()

def main(argv):
  patch_prj(old_prj_path, new_prj_path);

if __name__ == "__main__":
    main(sys.argv)


