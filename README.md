# ar-neuronav
Screenless AR-guided Neuronavigation for non-invasive brain stimulation

## How to start

```bash
$ pip install -r requirements.txt
```

### Stream to Hololens

```bash
$ python Stream_AR.py --help
usage: Stream_AR.py [-h] [--hl-ip ip-address] [--hl-port port] --input-file
                    INPUT_FILE

Stream coordinates to HL

optional arguments:
  -h, --help            show this help message and exit
  --hl-ip ip-address    Hololens ip-address
  --hl-port port        Hololens port
  --input-file INPUT_FILE
                        Brain sight exported file
```
