import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


s = Serializer('secret', 5)
token = s.dumps({'user_id': 1}).decode('utf-8')
print(token)

print(s.loads(token))
print('Waiting 10 secs', 'token expiring in 5')
time.sleep(10)
print(s.loads(token))
