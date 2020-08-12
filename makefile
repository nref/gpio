COMMAND = python3 -u main.py
LOG = main.log

MAIN_PID := $(shell pgrep -x -f '$(COMMAND)')
HOT_PID := $(shell pgrep -f 'hott.sh $(COMMAND)')

HOST = zerow2
PORT = 8001

run:
	$(COMMAND) >> $(LOG) 2>&1 &
	tail -n 0 -f $(LOG)

stop:
ifneq ($(MAIN_PID),)
	kill $(MAIN_PID)
endif

ifneq ($(HOT_PID),)
	kill $(HOT_PID)
endif

hot:
	./hott.sh "$(COMMAND)" ">> $(LOG) 2>&1 &" *.py &
	touch $(LOG)
	tail -n 0 -f $(LOG)

test:

	# test pins
	curl http://$(HOST):$(PORT)/pins
	curl --request POST http://$(HOST):$(PORT)/pin/1/on
	curl --request POST http://$(HOST):$(PORT)/pin/2/on

	curl http://$(HOST):$(PORT)/pin/1
	curl http://$(HOST):$(PORT)/pin/2
	curl http://$(HOST):$(PORT)/pins

	curl --request POST http://$(HOST):$(PORT)/pin/1/off
	curl --request POST http://$(HOST):$(PORT)/pin/2/off
	curl http://$(HOST):$(PORT)/pin/1
	curl http://$(HOST):$(PORT)/pin/2
	curl http://$(HOST):$(PORT)/pins

	curl http://$(HOST):$(PORT)/pin/3
	curl http://$(HOST):$(PORT)/pins

	# test heartbeat
	curl --request POST http://$(HOST):$(PORT)/heartbeat/enable
	curl --request POST http://$(HOST):$(PORT)/heartbeat
	curl --request POST http://$(HOST):$(PORT)/heartbeat
	curl --request POST http://$(HOST):$(PORT)/heartbeat
	curl --request POST http://$(HOST):$(PORT)/heartbeat
	curl --request POST http://$(HOST):$(PORT)/pin/1/on
	# Should be 1
	curl http://$(HOST):$(PORT)/pin/1
	sleep 3
	# Should be 0
	curl http://$(HOST):$(PORT)/pin/1

	curl --request POST http://$(HOST):$(PORT)/heartbeat/disable
	curl --request POST http://$(HOST):$(PORT)/pin/1/on
	# Should be 1
	curl http://$(HOST):$(PORT)/pin/1
	sleep 3
	# Should be 1
	curl http://$(HOST):$(PORT)/pin/1