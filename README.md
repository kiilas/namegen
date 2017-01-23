# namegen
Fantasy name generator based on formal grammar

## Introduction
This tool uses (plaintext) modules which define the transformations resulting
in a desired kind of word, name, phrase etc. It is designed primarily to
generate fantasy names, but can be used more generally for generative grammar.

The bundled modules include Elf, Orc and Dwarf, but it's easy to change these
or create new ones.

## Features
* context-free grammar transformations (tree structure)
* supports recursion (within reason)
* customisable probabilities
* simple module syntax

## Installation
Requires Python 3. Runs as a standalone executable/script.

## Usage
`namegen.py -m <modulename> [-c <count>]`

**modulename** is the module to use; bundled are *orc*, *elf* and *dwarf*.

**count** is the number of names to output; default is *24*.

## Sample outputs
`namegen.py -m orc -c 10`
> Larrz
> Mad
> Buzgo
> Lach
> Zazz
> Jellzdud
> Khadzad
> Bazradz
> Ul
> Mazzall

`namegen.py -m elf -c 10`
> Remidh
> Lirynyw
> Rwaehrir
> Lur Rysaes
> Rim
> Loeli
> Lwedh'suiv
> Naene
> Lerrae
> Hwai'dhuilmaer

`namegen.py -m dwarf -c 10`
> Bigug
> Arizag
> Rikhigip
> Zakha
> Ramizal
> Puqash
> Urid
> Ibin
> Bak
> Raviv

## Module syntax
See **sample.def**.

## License
AGPL; see LICENSE for the full text of the license for this project.
