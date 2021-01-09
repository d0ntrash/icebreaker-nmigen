from nmigen import Elaboratable, Signal, Module
from nmigen.lib.io import Pin
from nmigen_boards.icebreaker import ICEBreakerPlatform
from nmigen.build import Resource, Pins, Attrs


class Gpio(Elaboratable):
    def __init__(self, maxperiod):
        self.maxperiod = maxperiod
        self.counter = Signal(range(maxperiod))
        self.gpio = Pin(1, "o")
        self.led = Pin(1, "o")

    def elaborate(self, platform):
        m = Module()

        if platform is not None:
            self.led = platform.request("led_r")
            self.gpio = platform.request("gpio")

            with m.If(self.counter == 0):
                # Toggle pin and led after maxperiod clockcycles
                m.d.sync += [self.led.eq(~self.led),
                             self.gpio.eq(~self.gpio),
                             self.counter.eq(self.maxperiod)]
            with m.Else():
                m.d.sync += self.counter.eq(self.counter - 1)
        return m


if __name__ == "__main__":
    # This example shows how a single pin can be added
    # to the resources to use it as GPIO.
    dut = Gpio(3000000)
    p = ICEBreakerPlatform()

    # Add GPIO pin to resources
    p.add_resources([
        Resource("gpio",
                 0,
                 Pins("4", dir="o"),
                 Attrs(IO_STANDARD="SB_LVCMOS"))
            ])
    p.build(dut)
