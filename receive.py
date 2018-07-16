import Receiver
import platform
import subprocess

osys = platform.system()

osysDic = {
	'Windows' : {
		'start' : 'schtasks /create /tn CloudBaseSMS /tr run.bat /sc MINUTE /RU "SYSTEM"',
		'stop' : 'schtasks /delete /tn CloudBaseSMS /F'
		},
}

def process(body):
	bodyList = body.split(' ')
	if bodyList[0] in ['start', 'stop']:

		if len(bodyList) > 1:
			t = int(float(bodyList[1]))
		else:
			t = 1

		if bodyList[0] == 'start':
			subprocess.call(osysDic[osys][bodyList[0]] + ' /mo ' + str(t))
		elif bodyList[0] == 'stop':
			subprocess.call(osysDic[osys][bodyList[0]])



r = Receiver.Receiver(howToProcess = process)
r.receive('default')	#change default with channel wanted

