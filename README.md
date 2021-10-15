
# python-svg

This library imports and handles Scalable Vector Graphics (SVG).
It does not aim for full file format support, only to enable format-aware scripting.
Supports parsing essential tags, simple data extraction and some processing.

## Primary use cases

...aimed to be supported, not necessarily working (yet).

### File level: Import, inspect and export

The library enables loading i.e. importing an SVG from file and providing simplified access to it's content and properties e.g. the number of paths found.

### DOM level: Find, create, edit and remove

The library shall enable jQuery-like search for SVG DOM elements and support basic manipulation.

### Transformations

* apply transform attributes: matrix, rotate, translate
* flatten: convert all elements' coordinates to absolute values by traversing the DOM and applying all transform attributes

### Path parsing

The library parses path definitions (the "d" attribute of path elements).

* enumerate path commands (with arguments)
* convert relative commands to absolute and vice-versa
* calculate a path's bounding box
* break combined path definitions apart into separate path elements

Read more about path commands here:
https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d#path_commands


## License

GNU Affero GPL v3, see LICENSE file.
