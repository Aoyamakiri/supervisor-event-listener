import time


def processing_payload(payload):
    try:
        payload = payload.split(' ')
        processname = payload[0].split(':')[1]
        groupname = payload[1].split(':')[1]
        from_state = payload[2].split(':')[1]
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        return '进程名: ' + processname + '\n进程组名: ' + groupname + '\n当前进程状态: ' + from_state + '\n时间: ' + now
    except:
        return payload


def processing_header(header):
    event_name = header['eventname']
    if event_name == 'PROCESS_STATE_EXITED':  # 进程已从RUNNING状态转移到EXITED状态 即被kill
        explanation = '进程已从 「正在运行」 状态转移到 「退出」 状态'
    elif event_name == 'PROCESS_STATE_STARTING':  # 进程已转移到STARTING状态
        explanation = '进程已从之前的任何状态转移到 「正在启动」 状态'
    elif event_name == 'PROCESS_STATE_RUNNING':  # 进程已从STARTING状态转移到RUNNING状态 即成功启动
        explanation = '进程已从 「正在启动」 状态转移到 「启动完成」 状态'
    elif event_name == 'PROCESS_STATE_BACKOFF':  # 进程已从STARTING状态转移到BACKOFF状态
        explanation = '进程已从 「正在启动」 状态转移到 「启动失败」 状态'
    elif event_name == 'PROCESS_STATE_FATAL':  # 进程已从BACKOFF状态移动到FATAL状态 即多次未成功启动进程 并放弃尝试重新启动它
        explanation = '进程多次未能成功启动 已放弃尝试重新启动它'
    else:
        explanation = '事件名称: ' + event_name

    return explanation
