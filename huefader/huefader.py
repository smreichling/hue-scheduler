import itertools
import os
import random
import sys
import json
import time
from phue import Bridge

BRIDGE_IP_FILE = os.path.join(os.path.expanduser('~'), '.bridge_ip')
LIGHT_SET = 'Kitchen'
HUES = [
	('red', 65479),
	('green', 23917)
]

MIN_INTERVAL_SECS = 7
MAX_INTERVAL_SECS = 10
TRANSITION_TIME = 8

def run():
	bridge = _get_bridge()
	all_lights = get_light_set(bridge)

	lights_by_hue = {}
	for _, hue in HUES:
		lights_by_hue[hue] = set()

	print("Initializing lights")
	for i, light in enumerate(all_lights):
		color_name, color_hue = HUES[i % len(HUES)]
		change_color(bridge, light, color_hue, color_name)
		lights_by_hue[color_hue].add(light)


	print("Running updates")
	while True:
		# Wait an arbitrary amount of time
		sleep_time = MIN_INTERVAL_SECS + ((MAX_INTERVAL_SECS - MIN_INTERVAL_SECS) * random.random())
		time.sleep(sleep_time)

		# Find the largest color group
		larget_hue = -1
		largest_group = set()
		for hue, lights in lights_by_hue.items():
			if len(lights) > len(largest_group) or (len(lights) == len(largest_group) and random.choice([True, False])):
				largest_hue = hue
				largest_group = lights

		# Pick a light from that group
		light = largest_group.pop()

		# Pick next color
		color_candidates = [ h for h in HUES if h[1] != largest_hue]
		color_name, color_hue = color_candidates[random.randint(0, len(color_candidates) - 1)]

		# Update the color
		change_color(bridge, light, color_hue, color_name)
		lights_by_hue[color_hue].add(light)

def get_light_set(bridge):
	light_ids = bridge.get_group(LIGHT_SET,'lights')
	return [l for l in bridge.lights if str(l.light_id) in light_ids]

def change_color(bridge, light, hue, hue_name):

	result = bridge.set_light(light.light_id, {
		'on': True,
		'sat': 254,
		'bri': 254,
		'hue': hue,
		'transitiontime': TRANSITION_TIME
	})

	if 'error' in result[0]:
		print("ERROR: could not update light %s: %s" % (light.name, result[0]['error']['description']))
	else:
		print("Light %s set to %s" % (light.name, hue_name))


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
