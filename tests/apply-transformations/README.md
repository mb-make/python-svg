
## Applying transformations

This test reads a test SVG file
and flattens all contained transformations,
i.e. applys all elements' transformations
onto the coordinates of respective contained elements.
The result is saved as result.svg.
It must visually be identical to test.svg,
but contain no more elements with a transform attribute.
