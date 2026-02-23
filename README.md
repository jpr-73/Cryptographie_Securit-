# ISC Chat Client

A Python client for the ISC protocol server — CLI first, GUI planned.  
Built as part of a cryptography & networking course at HES-SO.

## Features

- TCP socket communication with the ISC protocol server
- Text, server-command, and image message support
- Cryptographic tasks
- CLI interface (GUI in progress)

## Protocol Overview

All messages use the `ISC` binary protocol:

| Byte(s)   | Content |
|-----------|---------|
| 1–3       | `ISC` (protocol identifier) |
| 4         | Message type: `t` (text), `s` (server), `i` (image) |
| 5–6       | (text/server) Message length N |
| 7–(7+N*4) | Message body — each char encoded as 4-byte big-endian UTF-8 |

**Image format:** bytes 5–6 = width/height (max 128px), followed by raw RGB pixel data row by row. (y-axis then x-axis)

> Any malformed message causes immediate disconnection.

## Server

- **Address:** `vlbelintrocrypto.hevs.ch`
- **Port:** `6000`
- **Access:** HEI network or VPN required

## Server Commands (type `s`)

Send commands via server messages (`s` type):

```
task shift encode 50       # Shift cipher encoding task (50 chars)
task vigenere decode 100   # Vigenère decoding task
task RSA encode 200        # RSA encoding task
task DifHel                # Start Diffie-Hellman key exchange
task hash verify           # Hash verification task
task hash hash             # Hashing task
```

After sending a `task` command, the server replies with instructions.  
Send your answer as a plain server message (no command prefix).


## Status

- [ ] TCP connection & ISC framing
- [ ] Text & server message support
- [ ] Image message support
- [ ] Cryptographic modules
- [ ] GUI
