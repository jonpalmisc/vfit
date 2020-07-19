<div align="center">
  <img src="vfit-logo.png" width="300">
</div>

## About

VFIT (Variable Font Instancing Tool) allows you to generate customized,
backwards-compatible, static instances of a variable font from a configuration
file. Additionally, VFIT can manipulate font metadata such as the family name,
version, or copyright information.

## Usage

To begin, you will need a variable font file to work with. Your first step will
be creating a configuration file. You can find a minimal example below. For an
example will all available metadata options, see `sample-full.yaml`.

``` yaml
metadata:
  family: Canary
  version: 1.0.1

styles:
  - name: Regular
    axes:
      wght: 400.0
      wdth: 100.0
  
  - name: Regular
    subfamily: Wide
    axes:
      wght: 400.0
      wdth: 150.0
```

Next, run VFIT and pass your configuration and variable font file as arguments:

``` sh
$ ./vfit.py config.yaml Input-VF.ttf
```

If you would like to generate instances into a specific directory, you can use
the `-o` option. For more information, see `./vift.py --help`.

## Contributing

All contributions are welcome. If you find a bug or have a request for a
feature, feel free to create a new issue (or even better, a pull request).

## License

Copyright &copy; 2020 Jon Palmisciano

VFIT is available under the MIT License. See [LICENSE.txt](LICENSE.txt) for more
information.
