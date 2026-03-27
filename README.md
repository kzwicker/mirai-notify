Usage:
```
python3 mirai-notify.py <stationID> <35|70> <smtp_host> <smtp_user> <smtp_password> <email1> [email2] ...
```

Station IDs can be found by inspecting element on https://m.h2fcp.org/

For instance, Mission Hills has the ID 575

To use with GMail, set `smtp_host` to `smtp.gmail.com`, set `smtp_user` to your full gmail address, and generate an app password at https://myaccount.google.com/apppasswords

Then populate the email arguments with the addresses of people you want to notify, like your boomer parents who bought the stupid car. Chuck it on a raspberry pi and you're golden.
