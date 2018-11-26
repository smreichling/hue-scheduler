import os
import sys
import json
import time
from phue import Bridge

BRIDGE_IP_FILE = os.path.join(os.path.expanduser('~'), '.bridge_ip')

def run():
	bridge = _get_bridge()
	twinkle_schedules = [int(i) for i, s in bridge.get_schedule().items() if "Twinkle" in s['name']]
	if len(twinkle_schedules) > 0:
		print("Deleting schedules...")
		delete_schedules(bridge, twinkle_schedules)
	else:
		print("Creating schedules...")
		create_schedules(bridge)


	print('Done!')

def create_schedules(bridge):
	kitchen_lights = [l for l in bridge.lights if 'Kitchen' in l.name]

	for kitchen_light in kitchen_lights:
		result = bridge.create_schedule(
			'Twinkle %s' % kitchen_light.name,
			'R/PT00:00:10A00:00:05',
			kitchen_light.light_id,
			{ 'alert': 'select' }
		)

		if _is_success(result):
			print("Created schedule %d for %s" % (int(result[0]['success']['id']), kitchen_light.name))
		else:
			print("Error creating schedule for %s: %s" % (kitchen_light.name, result[0]['error']['description']))

		time.sleep(1)

def delete_schedules(bridge, schedule_ids):
	for schedule_id in schedule_ids:
		result = bridge.delete_schedule(schedule_id)
		if _is_success(result):
			print("Deleted schedule %d" % schedule_id)
		else:
			print("Error deleting schedule %d: %s" % (schedule_id, result[0]['error']['description']))

def _get_bridge():
	if not os.path.isfile(BRIDGE_IP_FILE):
		print(
			"No bridge IP file found. Create a file at %s that contains the IP address of your Philips Hue Bridge and try again" % BRIDGE_IP_FILE,
			file=sys.stderr
		)
		sys.exit(1)

	with open(BRIDGE_IP_FILE, 'r') as bridge_ip_file:
		bridge_ip = bridge_ip_file.read().strip()

	bridge = Bridge(bridge_ip)
	bridge.connect()

	return bridge


def _is_success(result):
	if 'success' in result[0]:
		return True
	elif 'error' in result[0]:
		return False

	raise Exception("Got unexpected API response: %s" % result)