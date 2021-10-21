import schedule, os, requests, time
from urllib import request, parse

EETLIJST_USERNAME = os.environ['EETLIJST_USERNAME']
EETLIJST_PASSWORD = os.environ['EETLIJST_PASSWORD']

# Open a session on eetlijst.nl
def get_session_id():
    payload = {'login': EETLIJST_USERNAME, 'pass': EETLIJST_PASSWORD}
    url = 'http://eetlijst.nl/login.php'
    data = parse.urlencode(payload).encode()
    req = request.Request(url, data=data)
    return request.urlopen(req).geturl().split('=')[1]

def create_backup():
    session_id = get_session_id()
    url = f'http://eetlijst.nl/kosten2xls.php?session_id={session_id}'
    r = requests.get(url)
    filename = r.headers['Content-Disposition'][21:-1]
    with open(f'backups/{filename}', 'wb') as f:
        f.write(r.content)


schedule.every().hour.do(create_backup)

while True:
    schedule.run_pending()
    time.sleep(1)
