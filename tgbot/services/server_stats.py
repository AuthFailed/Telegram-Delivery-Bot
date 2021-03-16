import operator
from datetime import datetime

import psutil


async def stats():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boottime = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    time_diff = f"Онлайн: %.1f Часов" % (((now - boottime).total_seconds()) / 3600)
    mem_total = f"Всего памяти: %.2f GB " % (memory.total / 1000000000)
    mem_available = f"Доступно памяти: %.2f GB" % (memory.available / 1000000000)
    mem_use_perc = f"Использовано памяти: {memory.percent}%"
    disk_used = f"Использовано места на диске: {disk.percent}%"
    pids = psutil.pids()
    pidsreply = ''
    procs = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            pmem = p.memory_percent()
            if pmem > 0.5:
                if p.name() in procs:
                    procs[p.name()] += pmem
                else:
                    procs[p.name()] = pmem
        except:
            print("Hm")
    sortedprocs = sorted(procs.items(), key=operator.itemgetter(1), reverse=True)
    for proc in sortedprocs:
        pidsreply += proc[0] + " " + ("%.2f" % proc[1]) + " %\n"
    reply = f"""💻 Ресурсы сервера:
🕛 {time_diff}
💭 {mem_total}
💭 {mem_available}
💭 {mem_use_perc}
💾 {disk_used}

🏭 Запущенные процессы:
{pidsreply}"""

    return reply
