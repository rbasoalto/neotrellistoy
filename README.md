# NeoTrellis toy

Simple experiment for toddlers to play with buttons and colors.

It's built on a NeoTrellis 8x8 grid, with a button and RGB LED in every cell.

It's all driven by a nRF52840 feather that is powerful enough to run
Python, and has Bluetooth!

There's a CLI interface to test in the computer, no need to flash to the
actual device.

## The hardware

I built it from:

- 4x [neotrellis 4x4 boards](https://www.adafruit.com/product/3954)
- 4x [elastomer keypads](https://www.adafruit.com/product/1611)
- 1x [acrylic enclosure for 8x8 trellis](https://www.adafruit.com/product/4372)
- 1x [nRF52840 feather board](https://www.adafruit.com/product/4516) (could be any
  feather, but this one has bluetooth and a ton of sensors)
- 1x [JST PH 4-pin cable](https://www.adafruit.com/product/3955)

Optional, to play untethered:

- 1x [lipo battery](https://www.adafruit.com/product/2011)
- 1x [dpdt switch](https://www.adafruit.com/product/3220)

Follow the [assembly
instructions](https://learn.adafruit.com/neotrellis-feather-case-assembly)
(also linked in the enclosure kit). Flash CircuitPython by following [these
instructions](https://learn.adafruit.com/adafruit-feather-sense/circuitpython-on-feather-sense),
then follow [these
instructions](https://learn.adafruit.com/adafruit-feather-sense/feather-sense-circuitpython-libraries)
to download and flash the required libraries:

- `adafruit_neotrellis`
- `adafruit_seesaw`
- `adafruit_ble`

Then copy the .py files in this project to the root folder of the storage
device exposed by the feather board over USB. Done.

## Running on the PC

Run `python3 pc.py`

You can simulate button presses by typing a 2-digit number with the 1-based
`xy` coordinates. To simulate a button release, type `-xy`. Anything that's
not parsable as int will be interpreted as a toy command.

## Commands

You can pass remote commands via BLE UART. You can use the Bluefruit Connect
app for
[iOS](https://itunes.apple.com/app/adafruit-bluefruit-le-connect/id830125974?mt=8)
or
[Android](https://play.google.com/store/apps/details?id=com.adafruit.bluefruit.le.connect),
or there are even some WebBluetooth
[implementations](https://wiki.makerdiary.com/web-device-cli/) that work in
Chrome.

For now, there are 2 commands implemented:

- `clear [x y]`

  Clears the board. If the optional `x y` args are passed, it clears just x,y,
  but if either is 0 it clears the whole row/column, or the whole board if both
  are 0.

- `color <color> [x y]`

  Colors the board with the given color. It can be one of a few named colors,
  or 3- or 6-digit hex RGB. The optional `x y` args work just like `clear`.
