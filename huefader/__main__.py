import argparse
import sys
import os
from .huefader import HueFader, InvalidBridgeAddressException, InvalidGroupNameException

parser = argparse.ArgumentParser(description='Fade Hue lights through colors')
parser.add_argument(
	'bridge',
	type=str,
	help='IP address or hostname of Hue Bridge',
)
parser.add_argument(
	'group',
	type=str,
	help='Room or Zone to control',
)
parser.add_argument(
	'--debug',
	action='store_true',
	help='Print debug logging'
)

def error_and_exit(e: Exception) -> None:
	print(str(e), file=sys.stderr)
	sys.exit(1)

if __name__ == '__main__':
	args = parser.parse_args()

	if args.debug:
		log_out = sys.stderr
	else:
		log_out = open(os.devnull, 'w')

	try:
		hue_fader = HueFader(log_out, args.bridge, args.group)
	except InvalidBridgeAddressException as e:
		error_and_exit(e)
	except InvalidGroupNameException as e:
		error_and_exit(e)

	hue_fader.run()