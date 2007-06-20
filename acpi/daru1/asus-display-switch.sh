#!/bin/sh
echo $1 | sed -re 's/^hotkey ATKD 0+6([1-3]) [0-9a-f]+$/\1/' > /proc/acpi/asus/disp
