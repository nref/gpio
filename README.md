# gpio
A web service for Raspberry Pi GPIO

## Features

- Access GPIO pins via GET and POST
  - Using BCM (Broadcom) GPIO pin identifiers. 
    - *not* using board identifiers 
    - See http://pinout.xyz/
  
- Optional heartbeat fail-safe
  - Turns all pins OFF if it is not called within 2 seconds.

## Requirements

- A Raspberry Pi
- Python3
- [gpiozero](https://gpiozero.readthedocs.io/en/stable/) 

## Running

``` 
> git clone https://github.com/slater1/gpio
> cd gpio
> make run
python3 -u main.py >> main.log 2>&1 &
tail -n 0 -f main.log
Server up at :8001
```

## Stopping

```
> cd gpio
> make stop
kill 23028
```

## Configuration

See ```HOST``` and ```PORT``` in the [makefile](https://github.com/slater1/gpio/blob/master/makefile)

## Routes

### GET

#### /pin/{id}
Get the value of the given BCM (Broadcom) GPIO pin identifier. 0 means OFF, 1 means ON.

Examples:
```
curl http://raspberrypi:8001/pin/1
0
```
```
curl http://raspberrypi:8001/pin/2
1
```

#### /pins
Return all set GPIOs

Example:
``` 
GET http://raspberrypi:8001/pins
[(1, 0), (2, 1), (3, 0)] # GPIOs 1 and 3 are off, 2 is on
```

#### /
Same as ```/pins```

### POST

#### /heartbeat/enable
Enable the heartbeat check.

When the heartbeat check is enabled, the ```/heartbeat``` endpoint must be POSTed to at least once every 2 seconds. 
If not, all previously accessed pins are turned OFF.

Example:
```
curl --request POST http://zerow2:8001/heartbeat/enable
ok
```

#### /heartbeat/disable
Disable the heartbeat check.

Example:
```
curl --request POST http://zerow2:8001/heartbeat/disable
ok
```

#### /heartbeat
Update the heartbeat.

When the heartbeat check is enabled, this endpoint must be POSTed to at least once every 2 seconds. 
If not, all previously accessed pins are turned OFF.

Example:
```
curl --request POST http://zerow2:8001/heartbeat
ok
```

#### /pin/{id}/on
Turn the given pin ON

#### /pin/{id}/off
Turn the given pin OFF

## Debugging (hot-reload):

``` 
> cd gpio
> make hot
./hott.sh "python3 -u main.py" ">> main.log 2>&1 &" *.py &
touch main.log
tail -n 0 -f main.log
python3 -u main.py >> main.log 2>&1 &
Server up at :8001
```

## Testing: 
With service running (via ```make run``` or ```make hot```:

```
> cd gpio
> make test

# test pins
curl http://raspberrypi:8001/pins
[]
curl --request POST http://raspberrypi:8001/pin/1/on
ok
curl --request POST http://raspberrypi:8001/pin/2/on
ok
curl http://raspberrypi:8001/pin/1
1
curl http://raspberrypi:8001/pin/2
1
curl http://raspberrypi:8001/pins
[(1, 1), (2, 1)]
curl --request POST http://raspberrypi:8001/pin/1/off
ok
curl --request POST http://raspberrypi:8001/pin/2/off
ok
curl http://raspberrypi:8001/pin/1
0
curl http://raspberrypi:8001/pin/2
0
curl http://raspberrypi:8001/pins
[(1, 0), (2, 0)]
curl http://raspberrypi:8001/pin/3
0
curl http://raspberrypi:8001/pins
[(1, 0), (2, 0), (3, 0)]
# test heartbeat
curl --request POST http://raspberrypi:8001/heartbeat/enable
ok
curl --request POST http://raspberrypi:8001/heartbeat
ok
curl --request POST http://raspberrypi:8001/heartbeat
ok
curl --request POST http://raspberrypi:8001/heartbeat
ok
curl --request POST http://raspberrypi:8001/heartbeat
ok
curl --request POST http://raspberrypi:8001/pin/1/on
ok
# Should be 1
curl http://raspberrypi:8001/pin/1
1
sleep 3
# Should be 0
curl http://raspberrypi:8001/pin/1
0
curl --request POST http://raspberrypi:8001/heartbeat/disable
ok
curl --request POST http://raspberrypi:8001/pin/1/on
ok
# Should be 1
curl http://raspberrypi:8001/pin/1
1
sleep 3
# Should be 1
curl http://raspberrypi:8001/pin/1
1
```
