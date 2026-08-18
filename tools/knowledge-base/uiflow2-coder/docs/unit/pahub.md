# PaHub Unit

PaHub Unit is an I2C hub used to connect multiple I2C Units to one host I2C bus.

Support the following products:

    PaHubUnit

## Usage

1. Add **Unit PaHub**.

2. Set the PaHub address. The address must match the actual DIP switch setting
   on the PaHub hardware.

3. Add the other I2C Unit connected to Unit PaHub.

4. In the connected Unit configuration, select **Bus: PAHUB**, then select the
   PaHub port/channel number that the Unit is connected to.

The default PaHub address is `0x70`. If the DIP switch changes the hardware
address, update the address setting in UiFlow2 to the same value.
