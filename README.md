# huefader

Quick-and-dirty script that uses the Philips Hue API to make the lights in my kitchen fade through Christmas colors!

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
