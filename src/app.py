import schedule, os, requests, time
from urllib import request, parse
from datetime import datetime

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
    # Download new
    session_id = get_session_id()
    url = f'http://eetlijst.nl/kosten2xls.php?session_id={session_id}'
    r = requests.get(url)
    filename = datetime.now().isoformat()[0:-10].replace('T', '_') + '.xls'
    if len(r.content) < 75000:
        print(f'Backup {filename} failed, received only {len(r.content)} bytes. Skipping cleanup.')
        return
    
    # Write backup
    with open(f'backups/{filename}', 'wb') as f:
        f.write(r.content)
        print(f'Downloaded {filename}')
    
    # Cleanup
    files_to_delete = sorted(os.listdir('backups'))[0:-96]

    for file in files_to_delete:
        os.remove(f'backups/{file}')
        print(f'Removed {file}')

create_backup()

schedule.every().hour.do(create_backup)


while True:
    schedule.run_pending()
    time.sleep(1)
