#!/bin/bash
echo Scrip automatico para Reconocimiento de activos
whois $1  > infoWhois
grep 'Email' infoWhois | cut -d ':' -f 2 | sed 's/ //g' > correosMX


#informacion general del dominio
echo "----------------------------------"
echo "---------Info del dominio---------"
echo "----------------------------------"

cat infoWhois


#comprobar si el host esta online y analizar TOP 10 puertos
echo "----------------------------------"
echo "---------Estado del dominio---------"
echo "----------------------------------"


nmap -sn $1

echo "----------------------------------"
echo "---------Analisis Top 10---------"
echo "----------------------------------"

nmap $1 -v -sV --top-ports=10 -oN puertos

echo "----------------------------------"
echo "---------Puertos abiertos---------"
echo "----------------------------------"

grep open puertos

echo "----------------------------------"
echo "---------NS y MX Server---------"
echo "----------------------------------"
grep 'Name Server' infoWhois
nslookup -query=mx $1 | grep 'mail'



#Amass
echo "----------------------------------"
echo "------------Amass-----------------"
echo "----------------------------------"


amass enum -d $1 -dir /home/kali/herramientaciber
awk -F, '{print $5 $6}' amass.json | sort -u | sed 1d > asn.txt



#Massdns
echo "----------------------------------"
echo "------------Massdns-----------------"
echo "----------------------------------"

./massdns/bin/massdns -r massdns/lists/resolvers.txt -t AAAA amass.txt -w massdns$2.txt


#CrossLinked
echo "----------------------------------"
echo "------------CrossLinked-----------------"
echo "----------------------------------"

python3 crosslinked/crosslinked.py -f {f}{last}@$1  $2 -o nombrescorreo$2.txt

mkdir -p $2

mv infoWhois $2/
mv amass.* $2/
mv asn.txt $2/
mv correosMX $2/
mv nombrescorreo$2.txt $2/
mv puertos $2/
mv massdns$2.txt $2/

cat $2/infoWhois >> $2/info$2
echo "**********************************************" >> $2/info$2
echo "*****************SUBDOMINIOS******************" >> $2/info$2
echo "**********************************************" >> $2/info$2

cat $2/amass.txt >> $2/info$2
echo "**********************************************" >> $2/info$2
echo "*****************CORREOS MX NX******************" >> $2/info$2
echo "**********************************************" >> $2/info$2

cat $2/correosMX >> $2/info$2
echo "**********************************************" >> $2/info$2
echo "*****************CORREOS CORPORATIVOS******************" >> $2/info$2
echo "**********************************************" >> $2/info$2

cat $2/nombrescorreo$2.txt >> $2/info$2
echo "**********************************************" >> $2/info$2
echo "*****************PUERTOS******************" >> $2/info$2
echo "**********************************************" >> $2/info$2

cat $2/puertos >> $2/info$2
echo "**********************************************" >> $2/info$2
echo "*****************INFORMACION DE SUBDOMINIOS******************" >> $2/info$2
echo "**********************************************" >> $2/info$2
cat $2/massdns$2.txt >> $2/info$2



#parte de pwndb
echo "----------------------------------"
echo "------------Pwndb-----------------"
echo "----------------------------------"

service tor start

#cd /home/kali/pwndb/venv/
#source /home/kali/pwndb/venv/bin/activate
while IFS= read -r line
do
 python3 pwndb/pwndb.py --target $line
done < $2/nombrescorreo$2.txt


 
