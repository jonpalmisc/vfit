<div align="center">
  <img src="vfit-logo.png" width="300">
</div>

## About

VFIT (Variable Font Instancing Tool) allows you to generate customized,
backwards-compatible, static instances of a variable font from a configuration
file. Additionally, VFIT can manipulate font metadata such as the family name,
version, or copyright information.

## Installation

VFIT is not currently available on the Python Package Index. You can install
VFIT by downloading a pre-built wheel from the Releases section or by building
one yourself.

``` sh
# Skip this step if you're downloading a prebuilt wheel.
$ git clone https://github.com/jonpalmisc/vfit.git && cd vfit
$ poetry build && cd dist

# Install VFIT from the wheel.
$ pip install vfit-version-py3-none-any.whl
```

## Usage

To begin, you will need a variable font file to work with. Your first step will
be creating a configuration file. See `sample.json` for an example.

Next, run VFIT and pass your configuration and variable font file as arguments:

``` sh
$ vfit config.yaml Input-VF.ttf
```

If you would like to generate instances into a specific directory, you can use
the `-o` option. For more options, see `./vift.py --help`.

## Contributing

All contributions are welcome. If you find a bug or have a request for a
feature, feel free to create a new issue (or even better, a pull request).

## Credits

Special thanks to [Viktor Rubenko](https://github.com/ViktorRubenko) for
helping me get exported fonts to work on Windows!

## License

Copyright &copy; 2020 Jon Palmisciano

VFIT is available under the MIT License. See [LICENSE.txt](LICENSE.txt) for
more information.
