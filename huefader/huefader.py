import random
import time
from phue import Bridge, Light, PhueRegistrationException
from typing import Tuple, TextIO, List, Optional, Dict, MutableSet
from .exceptions import InvalidBridgeAddressException, InvalidGroupNameException, InvalidColorException, InitializationException
from .colors import Color, KnownColors

DEFAULT_COLORS = (KnownColors['red'], KnownColors['green'])

MIN_INTERVAL_SECS = 7
MAX_INTERVAL_SECS = 10
TRANSITION_TIME = 8

class ColorLightSet():
	color: Color
	lights: MutableSet[Light]

	def __init__(self, color: Color) -> None:
		self.color = color
		self.lights = set()

	def add(self, bridge: Bridge, light: Light) -> None:
		self._change_color(bridge, light)
		self.lights.add(light)

	def pop(self) -> Light:
		return self.lights.pop()

	def light_count(self) -> int:
		return len(self.lights)

	def _change_color(
		self,
		bridge: Bridge,
		light: Light, 
	) -> None:

		result = bridge.set_light(light.light_id, {
			'on': True,
			'xy': [self.color.x, self.color.y],
			'bri': 254,
			'transitiontime': TRANSITION_TIME
		})

		if 'error' in result[0]:
			raise Exception("ERROR: could not update light %s: %s" % (light.name, result[0]['error']['description']))

	def __repr__(self) -> str:
		return "%s: %s" % (self.color.name, ", ".join([l.name for l in self.lights]))

class HueFader():
	_log_out: TextIO
	_bridge: Bridge
	_lights: Tuple[Light]
	_colors: Tuple[Color]
	def __init__(
		self,
		log_out: TextIO,
		bridge_address: str,
		group: str,
		colors: Optional[List[str]],
	) -> None:
		self._log_out = log_out

		self._log(colors)
		if colors is not None and len(colors) > 0:
			try:
				self._colors = tuple((KnownColors[c] for c in colors))
			except KeyError as e:
				raise InvalidColorException(str(e))
		else:
			self._log("No colors specified, so using default colors")
			self._colors = DEFAULT_COLORS

		try:
			self._bridge = Bridge(bridge_address, config_file_path='/root/.phue/config.json')
			self._bridge.connect()
		except PhueRegistrationException as e:
			raise InvalidBridgeAddressException(e.message)

		group_id = self._bridge.get_group_id_by_name(group)
		if group_id is False:
			raise InvalidGroupNameException(group)

		light_ids = self._bridge.get_group(group_id, 'lights')
		if len(light_ids) == 0:
			raise InitializationException("Room or Zone %s has no lights in it", group)
		self._lights = (l for l in self._bridge.lights if str(l.light_id) in light_ids)


	def run(self) -> None:
		color_light_sets = [ ColorLightSet(c) for c in self._colors ]

		self._log("Initializing lights")
		for i, light in enumerate(self._lights):
			cls = color_light_sets[i % len(color_light_sets)]
			cls.add(self._bridge, light)
			self._log("Light %s initialized to %s" % (light.name, cls.color.name))

		color_light_sets = sorted(color_light_sets, key=lambda cls: cls.light_count())

		self._log("Running updates")
		while True:
			# Wait an arbitrary amount of time
			sleep_time = MIN_INTERVAL_SECS + ((MAX_INTERVAL_SECS - MIN_INTERVAL_SECS) * random.random())
			time.sleep(sleep_time)

			# Pop a light from the largest color set
			light = color_light_sets[-1].pop()

			# Add it to the smallest color set
			try:
				color_light_sets[0].add(self._bridge, light)
			except Exception as e:
				self._log(str(e))
				# Assume light is unchanged and add it back to its original set
				color_light_sets[-1].lights.add(light)
				continue

			self._log("Light %s changed to %s" % (light.name, color_light_sets[0].color.name))

			# Re-sort the sets
			color_light_sets = sorted(color_light_sets, key=lambda cls: cls.light_count())

	def _log(self, msg: str) -> None:
		print(msg, file=self._log_out)


