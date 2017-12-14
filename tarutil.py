#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tarutil.py
#  
#  Copyright 2012 Alma Observatory <hyperion@Neptune>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#        /\/\  
#       ( 00 ) Neptuno 2014
#       /  ¯ \ 
#     (((/  \)))

import os
import sys
import fnmatch
import tarfile
import itertools


def main():
    
    
    if len(sys.argv) < 2:
        sys.exit('Usage: tarutil.py <Project Code>')
    else:
        code = sys.argv[1]
    
    working_dir = '.'
    
    dir_list = os.listdir(working_dir)
    
    project_list = []
    
    for d in dir_list:
        if not fnmatch.fnmatch(d, code + '*.tar'):
            print 'Skiping file [%s]' % d
            continue
        project_list.append(d)
    
    if project_list is 0:
        sys.exit('ERROR: No tars with code [%s] files in directory' % code)
    
    lines = []
    file_names_tar = []
    for p in project_list:
        tar = tarfile.open(os.path.join(working_dir, p))
        file_names = [name.split('/') for name in tar.getnames()] #<--- 00
        readme_file = [f for f in file_names if 'README' in f]
        if readme_file:
            readme_path = '/'.join(readme_file[0])
            tar.extract(readme_path) #<--- 00
            f = open(readme_path, 'r')
            for l in f:
                if l[0] == '|':
                    lines.append(l)
            f.close()
        file_names_tar = file_names_tar + file_names
    
    if len(lines) == 0:
        sys.exit('ERROR: README file has not directory data in project [%s]' % code)
    
    #Save a list of files in tars----------------------------------------+
    lines_out = [('/').join(line) + '\n' for line in file_names_tar]
    file_name = '%s_files_tar.out' % code
    f = open(file_name, 'w')
    f.writelines(lines_out)
    f.write('Total ' + str(len(file_names_tar)))
    f.close()
    
    #Parser the README tree ---------------------------------------------+
    file_names_readme = []
    dnode = 0
    n = []
    for i in lines:
        l = i.strip(' \n').split('|')
        path_element = l[len(l)-1][3:]
        if '/' in path_element:
            path_element = path_element.replace('/','')
        if dnode < len(l):
            n.append(path_element)
        if dnode == len(l):
            file_names_readme.append(n)
            n = n[:-1]
            n.append(path_element)
        if dnode > len(l):
            file_names_readme.append(n)
            diff = len(l) - dnode
            n = n[:diff - 1]
            n.append(path_element)
        if lines.index(i) == (len(lines) - 1): #Last line!
            file_names_readme.append(n)
        dnode = len(l)
    #Save a list of files/directories in README file----------------------------------+
    file_name = '%s_files_readme.out' % code
    lines_out = ['/'.join(line) + '\n' for line in file_names_readme]
    f = open(file_name, 'w')
    f.writelines(lines_out)
    f.close()
    
    flatlist_readme = itertools.chain(*file_names_readme)
    flatlist_tar = itertools.chain(*file_names_tar)
    
    not_found = list(set(flatlist_readme) - set(flatlist_tar))
    
    if len(not_found) > 0:
        print '======================================================================================='
        print 'Warning: Some files were not found in tars files in project [%s]' % code
        print '======================================================================================='
        file_diff = '%s_files.diff' % code
        f = open(file_diff, 'w')
        for l in not_found:
            print 'Files/Directories not found: ' + l
            f.write(l + '\n')
        f.close()
        print '\n'
    else:
        print '======================================================================================='
        print 'README file OK in project [%s]' % code
        print '======================================================================================='
        
if __name__ == '__main__':
    main()
