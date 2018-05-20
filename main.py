import ntptime, usocket as socket
from machine import Timer
from config import OLED, PUMP, top_tank, bot_tank, display_timer, f1, f2, f3
from utils import log

status = {}

def allstop(unused=None):
    global status
    status = {'JOB': 'IDLE'}
    top_tank.stop()
    bot_tank.stop()
    display_timer.init(


def pump_top(unused=None, target_level=100):
    global status
    status = {'JOB': 'TOP TANK'}
    top_tank.pump(target_level)
    init_timers()

def pump_bot(unused=None, target_level=100):
    global status
    status = {'JOB': 'BOTTOM TANK'}
    bot_tank.pump(target_level)
    init_timers()

def display_update(timer):
    global status, addr
    tank = top_tank if top_tank.valve_pin.value() else bot_tank
    OLED.fb.fill(0)
    row = 0
    for k, v in status.items():
        OLED.fb.text('{} :- {}'.format(k, v), 0, row, 1)
        row += 10
    OLED.update()

# Convenience wrapper
def init_timers():
    display_timer.init(
        period=3000, mode=Timer.PERIODIC, callback=display_update
    )

# WEB API served by simplistic http
def run_api()
    global status
    s = socket.socket()
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    http_response = "HTTP/1.0 200 OK\r\n\r\n{}"

    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        req = client_s.recv(4096)
        request = req.split('GET /')[1].split(' HTTP/')[0]
        client_s.send(
            {
                "pump/top": pump_top,
                "pump/bot": pump_bot,
                "pump/top/": pump_top,
                "pump/bot/": pump_bot,
                "stop": allstop,
                "status": lambda unused: str(status)
            }.get(request)(level)
        )
        client_s.close()

# Stahp!
allstop()

# Tie above fn buttons to tank fill functions
f1.irq(trigger=f1.IRQ_FALLING, handler=pump_top)
f2.irq(trigger=f2.IRQ_FALLING, handler=pump_bot)
f3.irq(trigger=f3.IRQ_FALLING, handler=allstop)

try:
    ntptime.settime()
    run_api()
except
