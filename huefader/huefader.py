import itertools
import os
import random
import sys
import json
import time
from phue import Bridge, Light, PhueRegistrationException
from typing import Tuple, TextIO
from .exceptions import InvalidBridgeAddressException, InvalidGroupNameException

HUES = [
	('red', 65479),
	('green', 23917)
]

MIN_INTERVAL_SECS = 7
MAX_INTERVAL_SECS = 10
TRANSITION_TIME = 8

class HueFader():
	_log_out: TextIO
	_bridge: Bridge
	_lights: Tuple[Light]
	def __init__(
		self,
		log_out: TextIO,
		bridge_address: str,
		group: str,
	) -> None:
		self._log_out = log_out

		try:
			self._bridge = Bridge(bridge_address, config_file_path='/root/.phue/config.json')
			self._bridge.connect()
		except PhueRegistrationException as e:
			raise InvalidBridgeAddressException(e.message)

		group_id = self._bridge.get_group_id_by_name(group)
		if group_id is False:
			raise InvalidGroupNameException(group)

		light_ids = self._bridge.get_group(group_id, 'lights')         
		self._lights = (l for l in self._bridge.lights if str(l.light_id) in light_ids)


	def run(self) -> None:
		lights_by_hue = {}
		for _, hue in HUES:
			lights_by_hue[hue] = set()

		self._log("Initializing lights")
		for i, light in enumerate(self._lights):
			color_name, color_hue = HUES[i % len(HUES)]
			self._change_color(light, color_hue, color_name)
			lights_by_hue[color_hue].add(light)


		self._log("Running updates")
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
			self._change_color(light, color_hue, color_name)
			lights_by_hue[color_hue].add(light)

	def _change_color(
		self, 
		light: Light, 
		hue: int, 
		hue_name: str,
	) -> None:

		result = self._bridge.set_light(light.light_id, {
			'on': True,
			'sat': 254,
			'bri': 254,
			'hue': hue,
			'transitiontime': TRANSITION_TIME
		})

		if 'error' in result[0]:
			self._log("ERROR: could not update light %s: %s" % (light.name, result[0]['error']['description']))
		else:
			self._log("Light %s set to %s" % (light.name, hue_name))


	def _log(self, msg: str) -> None:
		print(msg, file=self._log_out)


