# supervisor-event-listener
另一种supervisor事件监听方案

在config配置中添加你的邮箱即可

#### supervisor的配置例子如下
```
[eventlistener:listener]
command=python /yourpath/listener.py
events=PROCESS_STATE
stdout_logfile = /yourpath/log/listener.log
buffer_size=102400
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
autorestart=true
```