"""!cp see checkpoint in Asia/Jakarta timezone"""
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import time
import re


# Ingress game constants; do not change
sclen = 175 * 60 * 60  # 175 hours = 630000
cplen = 5 * 60 * 60  # 5 hours = 18000

# Time constants; do not change
def day(n): return n * 24 * 60 * 60
def hour(n): return n * 60 * 60
def minute(n): return n * 60

# Internal constants; do not change
T_CHECKPOINT = 1
T_SEPTICYCLE = 2

def roundN(n, N):
    '''round to the nearest N'''
    return int(N * round(float(n) / float(N)))

def fmttime(t):
	'''format s seconds in days/hours/mins/secs'''
	d, h, m, s = 0, 0, 0, 0
	s = t % 60
	t /= 60
	m = t % 60
	t /= 60
	h = t % 24
	t /= 24
	d = t

	r = [
		[d, 'd'],
		[h, 'h'],
		[m, 'm'],
		[s, 's'],
	]

	while r and r[0][0] == 0:
		r = r[1:]

	while r and r[-1][0] == 0:
		r = r[:-1]

	return ' '.join(['%d%s' % (n, u) for n, u in r])



def cp(zone="Asia/Jakarta"):
    utc = pytz.utc
    id_tz = timezone(zone)
    
    now = time.time()
    now = roundN(now, 60)
    untilcp = cplen - (now % cplen)
    untilsc = sclen - (now % sclen)
    date = time.ctime(now)
    
    if untilcp == cplen:
        untilcp = 0
    if untilsc == sclen:
        untilsc = 0
    
    def fmtdate(s):
        utc_dt = utc.localize(datetime.utcfromtimestamp(s))
        id_dt = id_tz.normalize(utc_dt.astimezone(id_tz))
        return id_dt.strftime('%A, %d %b at %l:%M %P').replace('  ', ' ')
    
    msg = []
    
    if untilcp == 0:
        msg += ['Checkpoint is *NOW*.']
    else:
        msg += ['Checkpoint: %s (*%s*)' % (fmtdate(now + untilcp), fmttime(untilcp))]
	
	if untilsc == 0:
	    msg += ['Septicycle ends *NOW*.']
	else:
	    msg += ['Septicycle ends: %s (*%s*)' % (fmtdate(now + untilsc), fmttime(untilsc))]
	
	msg += ["Upcoming checkpoints: %s | %s | %s | %s" % 
        (fmtdate(now + untilcp + cplen), fmtdate(now + untilcp + 2*cplen),
        fmtdate(now + untilcp + 3*cplen), fmtdate(now + untilcp + 4*cplen))]

    return '\n'.join(msg)


def on_message(msg, server):
    text = msg.get("text", "")
    match = "!cp" == text
    if not match:
        return

    return cp()
