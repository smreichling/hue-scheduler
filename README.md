# hue-scheduler

Quick-and-dirty script that uses the Philips Hue API to make the lights in my kitchen twinkle!

## Dev Setup
 1. Install Python 3.7
 2. Install Pipenv

## To Run
```
pipenv run python -m scheduler 
```
If the lights currently are not twinkling, the script will start them twinkling. If they are twinkling, it will stop the twinkling.
