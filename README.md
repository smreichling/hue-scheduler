# huefader

Quick-and-dirty script that uses the Philips Hue API to make a group of lights fade through multiple colors!

## Dev Setup
 1. Install Docker

## To Build
```
docker build -t huefader .
```

## To Run
```
docker run --rm huefader:latest BRIDGE_IP ROOM_OR_ZONE_NAME
```

Note that each time the container is run as above, it will attempt to authenticate with the bridge as a new user. For this to succeed, the button on the bridge will need to have been pressed within the last 30 seconds.

To reuse a bridge user across multiple container runs (and not have to press the button each time this container is run), mount a local directory within the container file system at `/root/.phue`. The script will then store the user credentials it creates into a file called `config.json` in that directory for future reuse. This can be done like so:

```
 docker run --rm -v /some/path:/root/.phue huefader:latest BRIDGE_IP ROOM_OR_ZONE_NAME
```
