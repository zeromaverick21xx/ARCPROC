cd /fromARCS/cycle1
for i in `find . -mindepth 1 -maxdepth 1 -type d  -exec test -e "{}/exitoso.txt" ';' -print | sed 's|./||'`;do rm -rf /fromARCS/cycle1/$i;done
cd /fromARCS/cycle2
for i in `find . -mindepth 1 -maxdepth 1 -type d  -exec test -e "{}/exitoso.txt" ';' -print | sed 's|./||'`;do rm -rf /fromARCS/cycle2/$i;done
cd /fromARCS/cycle3
for i in `find . -mindepth 1 -maxdepth 1 -type d  -exec test -e "{}/exitoso.txt" ';' -print | sed 's|./||'`;do rm -rf /fromARCS/cycle3/$i;done
cd /fromARCS/cycle4
for i in `find . -mindepth 1 -maxdepth 1 -type d  -exec test -e "{}/exitoso.txt" ';' -print | sed 's|./||'`;do rm -rf /fromARCS/cycle4/$i;done


