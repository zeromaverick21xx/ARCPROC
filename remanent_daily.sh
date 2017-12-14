#Developed by Bernardo Malet 2015

cd /home/jao/
echo '' > remanent.txt
echo "CYCLE 1 remanents at /fromARCS/cycle1/" >> remanent.txt
echo "======================================" >> remanent.txt
echo '' >> remanent.txt
ls -p /fromARCS/cycle1/ | grep -v / | grep .tar$ >> remanent.txt
echo '' >> remanent.txt
echo '--------------------------------------' >> remanent.txt
echo '' >> remanent.txt
echo "CYCLE 2 remanents at /fromARCS/cycle2/" >> remanent.txt
echo "======================================" >> remanent.txt
echo '' >> remanent.txt
ls -p /fromARCS/cycle2/ | grep -v / | grep .tar$>> remanent.txt
echo '' >> remanent.txt
echo '--------------------------------------' >> remanent.txt
echo '' >> remanent.txt
echo "CYCLE 3 remanents at /fromARCS/cycle3/" >> remanent.txt
echo "======================================" >> remanent.txt
echo '' >> remanent.txt
ls -p /fromARCS/cycle3/ | grep -v / | grep .tar$>> remanent.txt
echo '' >> remanent.txt
echo '--------------------------------------' >> remanent.txt
echo '' >> remanent.txt
echo "CYCLE 4 remanents at /fromARCS/cycle4/" >> remanent.txt
echo "======================================" >> remanent.txt
echo '' >> remanent.txt
ls -p /fromARCS/cycle4/ | grep -v / | grep .tar$>> remanent.txt
echo '' >> remanent.txt




mail -s 'REMNANT' adc-apoas@alma.cl <remanent.txt
mail -s 'REMNANT' gallardo@alma.cl <remanent.txt
mail -s 'REMNANT' hfrancke@alma.cl <remanent.txt

rm -rf remanent.txt
