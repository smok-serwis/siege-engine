# siege-engine
A tactical piece of software that allows the magnificient company SMOK sp. z o. o. strike it's enemies from afar


Installation and operation
==========================

Just type:

```bash
pip install git+https://github.com/smok-serwis/siege-engine.git
python -m siege_engine 300 tass.com
```

Note that a helpful error message will be displayed if you just type:

```bash
python -m siege_engine
```

Please set the 300 value regarding your network conditions. This is the amount of threads
that will be spawned. Obviously, more is better (I bet your network could hold about 2000
of them)

# Change log

* v1.1: added graceful support for time-out sessions