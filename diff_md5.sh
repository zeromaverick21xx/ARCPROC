#Developed by Bernardo Malet 2014

diff <(cat *.md5sum | awk '{ print $1 }') <(md5sum *.tar | awk '{ print $1 }');echo $?
