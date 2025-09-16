# Ps4 trophies

## Project

I wanted to learn more about the trophy system on the PS4 and more in general on any ps console available.

So I started looking around and reading guides and forums trying to implement, at start, a .TRP file parser to list all trophies related to a specific game.

## How to create the .PKG file (for PS4)

Refer on "How to build" in the guide [here](./pkg/README.md)

## Long-term idea

I'd like to provide a .PKG file to run an HTTP server that give the user the ability to unlock trophies remotely thorugh a web-ui.

## Folder structure

Project root contains the python .TRP file loader

The payload folder instead contains a ps4 payload built with [libPS4](https://github.com/Scene-Collective/ps4-payload-sdk) to decrypt the `sealedkey` using the `sce_sbl_ss_decrypt_sealed_key` kernel function.

This will contain the code for the HTTP .pkg file in the future.

The payload folder also contains a `Dockerfile` to make it easier to build the .bin payload.

## Kernel logs output

In order to get to see kernel logs you need to use the following commands in two separate shells.

```sh
$ socat -d -d pty,raw,echo=0,link=/tmp/virtualTTY TCP:<CONSOLE_IP>:3232
```

and then

```sh
$ cat /tmp/virtualTTY | sed 's/[[:space:]]\+$//'
```

## Sources

- https://www.psxhax.com/
- https://www.psdevwiki.com/
- https://github.com/bucanero/apollo-ps4/
- https://github.com/xXxTheDarkprogramerxXx