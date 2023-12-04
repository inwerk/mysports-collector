# Data collector for MySports.com

[MySports](https://www.mysports.com/) is a German fitness platform featuring several thousand gyms that use this platform to offer
their members various services. The website contains information about gyms such as
descriptions, pictures, opening hours, occupancy rates and visitor numbers.

This tool can be used to collect and store visitor numbers and occupancy rates of gyms over the long term.

By default, the application will collect visitor information for
[Sportfabrik Bonn-Beuel](https://www.mysports.com/studio/c3BvcnRmYWJyaWs6MTIxMDAwOTc0MA%3D%3D) and
[Sportfabrik Bonn-Hardtberg](https://www.mysports.com/studio/c3BvcnRmYWJyaWs6MTIxNDEwMTUwMA%3D%3D).
However, other fitness studios can also be configured.

## Instructions

```
gymstalker --help
gymstalker start
gymstalker status
gymstalker stop
```

## How to install on Linux

Run the script for installing the application.

```
curl -sSL https://raw.githubusercontent.com/inwerk/mysports-collector/main/install.sh | bash
```

## How to uninstall

Run the script to remove the application from your system.

```angular2html
curl -sSL https://raw.githubusercontent.com/inwerk/mysports-collector/main/uninstall.sh | bash
```# mysports-collector
