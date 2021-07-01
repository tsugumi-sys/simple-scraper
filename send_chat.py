import requests

def send_chatwork(body):
    headers = {'X-ChatWorkToken' : '*********************'}
    room_id = '***********'
    url = "https://api.chatwork.com/v2/rooms/" + room_id + "/messages"
    params = {'body': body}
    res = requests.post(url, headers=headers, params=params)
    return res.status_code

if __name__ == '__main__':
    send_chatwork('Test Chat')