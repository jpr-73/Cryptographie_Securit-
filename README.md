# ISC Chat Client

A Python client for the ISC protocol server — complete with CLI and GUI interfaces.  
Built as part of a cryptography & networking course at HES-SO.

## Features

- TCP socket communication with the ISC protocol server
- Text, server-command, and image message support
- Cryptographic tasks
- CLI and GUI interfaces

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

## CLI Commands

The CLI supports the following commands:

**General:**
```
- /help - Show available commands
- /send <text> - Send text
- /send -s <text> - Send a server message
- /exit - Close the client
```

**Buffer Management:**
```
- /set <text> - Set the local buffer
- /show - Show current buffer content
- /clear - Clear the buffer
```

**Cryptographic Operations:**
```
- /encode shift <key>
- /encode vigenere <key>
- /encode rsa <n> <e>
- /encode hash
- /decode shift
- /decode rsa <n> <d> <content>
- /generate rsa
- /generate dh
- /generate dh-hk <p> <g>
- /generate dh-secret <p> <privKey> <pubKey>
```
**Server Tasks:**
```
- /task shift|vigenere|RSA encode|decode <length>
- /task DifHel
- /task hash hash|verify
```

After sending a task request, the server replies with instructions.  
Send your answer using `/send -s <answer>`.


## Status

- [x] TCP connection & ISC framing
- [x] Text & server message support
- [x] Cryptographic modules
- [x] GUI
