#!/usr/bin/python

import shutil
import glob
import os
import sys
from patch_prj import patch_prj

origin_prj = "../configs/CLCL_N_64.PRJ"
latest_prj = "../configs/CLCL_N_64_patch.PRJ"
bak_prj = "../configs/CLCL_N_64_bak.PRJ"

class DontPrint(object):
    def write(*args): pass

def find_spx(data, spx):
  for idx in range(len(data)):
    if spx in data[idx]:
      return idx
  return -1

def main(argv):
  if not os.path.isfile(origin_prj):
    print "Can not find '%s'"
    exit()

  if not os.path.isfile(latest_prj):
    print "Can not find '%s' \nPlease create latest PRJ or change latest PRJ path."
    exit()  

  oldstdout = sys.stdout
  
  sys.stdout = DontPrint()
  patch_prj(origin_prj, bak_prj)
  sys.stdout = oldstdout

  origin_prj_file = open(bak_prj, "r")
  origin_prj_data = origin_prj_file.readlines()
  origin_prj_file.close()
  os.remove(bak_prj)

  latest_prj_file = open(latest_prj, "r")
  latest_prj_data = latest_prj_file.readlines()
  latest_prj_file.close()
  
  deselect = [];
  for idx in range(len(origin_prj_data)):
    if "CONFIG_SPX_" in origin_prj_data[idx]:
      spx = origin_prj_data[idx].split('\n')
      spx = spx[0].split('\t')
      flag = 0
      for idx2 in range(len(latest_prj_data)):
        if spx[0] in latest_prj_data[idx2]:
          flag = 1
          break
      if flag != 1:
        deselect.append(spx[0]);
        print "deselect on latest:" + spx[0]
  
  select = [];
  for idx in range(len(latest_prj_data)):
    if "CONFIG_SPX_" in latest_prj_data[idx]:
      spx = latest_prj_data[idx].split('\n')
      spx = spx[0].split('\t')
      flag = 0 
      for idx2 in range(len(origin_prj_data)):
        if spx[0] in origin_prj_data[idx2]:
          flag = 1
          break
      if flag != 1:
        select.append(spx[0]);
        print "select on latest:" + spx[0]

  '''
  patch_files = glob.glob("../configs/patch/*")
  for idx in range(len(patch_files)):
    patch_file = open(patch_files[idx], "r")
    patch_data = patch_file.readlines()
    patch_file.close()
    for idx2 in range(len(patch_data)):
      patch_line = patch_data[idx2]
      if patch_line[:1] == "+":
        idx3 = find_spx(select, patch_line[1:-1])
        if idx3 != -1:
          print "It's aready patch select:" + patch_line[1:-1]
          del select[idx3]
      if patch_line[:1] == "-":
        idx3 = find_spx(deselect, patch_line[1:-1])
        if idx3 != -1:
          print "It's aready patch deselect:" + patch_line[1:-1]
          del deselect[idx3]
  '''
  
  num = 0
  target_path = "../configs/patch/" + str(num).zfill(2)
  while os.path.isfile(target_path) :
    num = num +1   
    target_path = "../configs/patch/" + str(num).zfill(2)
  
  flag = 0
  if not select:
    if not deselect:
      flag = 1
      print "nothing need to patch"
  
  if flag == 0:
    print "Create patch:" + target_path
    patch_file = open(target_path, "w")
    for idx in range(len(select)):
      patch_file.write("+" + select[idx] + "\n")
    for idx in range(len(deselect)):
      patch_file.write("-" + deselect[idx] + "\n")
    patch_file.close()

if __name__ == "__main__":
    main(sys.argv)
