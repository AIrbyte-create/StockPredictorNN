import webbrowser

# öffne die datei mit dem vollständigen pfad und modifizierten filennamen
with open("C:\\Users\\Gabriel Schwarzbauer\\Desktop\\Aktien_Trainer\\Vorhersage\\Eingabe_Daten.txt", "r") as f:
    for line in f:
        print(line.strip())
        
# öffne das browser plugin und öffne die url http://localhost:3000/
webbrowser.open("http://localhost:3000/")

# klicke auf den button im browser
from urllib.parse import parse_qs, urlparse

url = "http://localhost:3000/"
response = parse_qs(url)
path = urlparse(url).path

if path == '/':
    # falls der Pfad leer ist, setze es auf '/'
    from webbrowser import open_new
    target = open_new(f"{url}{path}/button")
else:
    from webbrowser import open_new
    target = open_new(f"{url}{path}/button")

target.click()