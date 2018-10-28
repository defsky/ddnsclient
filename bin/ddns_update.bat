@echo off

rem echo 'login_token=44299,c41b81bd9c4c09ec9c83d4396e517dc9&format=json&domain=afkplayer.com&record_id=341238720&sub_domain=login&value=%1&record_type=A&record_line_id=0'

curl.exe -X POST https://dnsapi.cn/Record.Modify -d 'login_token=44299,c41b81bd9c4c09ec9c83d4396e517dc9&format=json&domain=afkplayer.com&record_id=341238720&sub_domain=login&value=%1&record_type=A&record_line_id=0'
