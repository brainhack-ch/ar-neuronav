# ar-neuronav
Screenless AR-guided Neuronavigation for non-invasive brain stimulation

## How to start

```bash
$ pip install -r requirements.txt
```

### Stream to Hololens

There are two scripts, one single threaded and one multi-threaded (the file which ends with 'mt').
The multi-thread script is more advanced and I suggest you extend (or fix) that one.

```bash
$ python Stream_AR_mt.py --help
usage: Stream_AR_mt.py [-h] [--hl-ip ip-address] [--hl-port port]
                       [--my-ip ip-address] [--my-port port] --input-file
                       INPUT_FILE [--debug] [--run-calibration]

Stream coordinates to HL

optional arguments:
  -h, --help            show this help message and exit
  --hl-ip ip-address    Hololens ip-address
  --hl-port port        Hololens port
  --my-ip ip-address    this localhost ip address on the network (listen)
  --my-port port        this localhot port on which to listen
  --input-file INPUT_FILE, -i INPUT_FILE
                        Brain sight exported file
  --debug               enable debug level logging verbosity
  --run-calibration     run calibration (TODO)
```

Test locally that it sends to hololens (check the hololens ip address on the hololens settings menu, the port is your choice in your unity app):

```bash
$ python Stream_AR_mt.py -i test_data/Brainhack_stream2.txt --hl-ip 192.168.137.53 --hl-port 9009
```

The run `ifconfig` and find your own computerto get your ip address (the one of the PC). *Note* that the pc and the hololens should be on the same network.

Final example:

```bash
$ python Stream_AR_mt.py -i test_data/Brainhack_stream2.txt --hl-ip 192.168.137.53 --hl-port 9009 --my-ip 192.168.137.66 --hl-port 9005
```


## Troubleshooting

Use the scripts `udp_listener` and `udp_sender` to check that the connection with the hololens is working.

### UDP Listener

In one shell start the listener. It will listen from UPD packets sent by the Hololens.

```bash
$ python udp_listener --ip-address <my-ip> --port <my-port>
```

### UDP Sender

In another shell use the `upd_sender` to send UDP messages to the Hololens (use the port on which the hololens is listening on).

```bash
$ python udp_sender --ip-address <hololens-ip-address> --port <hololens-port>
```

## Credits
- Riccardo Poggi
- Olivier Reynaud
