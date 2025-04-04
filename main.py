import requests
import hashlib
import colorama
from colorama import init, Fore, Style

init(autoreset=True)

def api(query_char):
    url = f"https://api.pwnedpasswords.com/range/{query_char}"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Błąd ze wczytaniem {res.status_code}, sprawdź poprawność API")
    return res

def leaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0

def api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = api(first5_char)
    return leaks(response, tail)

def main():
    password = input('Wpisz hasło, które chcesz użytkować ')
    count = api_check(password)
    if count:
        print(Fore.RED + f"⚠️ Twoje hasło zostało znalezione w bazie wycieków haseł: {count} razy! Zmień hasło, użyj znaków specjalnych #@$%/+ itp. oraz dużych/małych liter i cyfr")
    else:
        print(Fore.GREEN + "✅ Twoje hasło nie wyciekło ani razu, jest w miare bezpieczne.")

if __name__ == '__main__':
    main()
