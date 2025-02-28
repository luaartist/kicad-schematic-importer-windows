.. _PcbDrawOptions:


PcbDrawOptions parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

-  **bottom** :index:`: <pair: output - pcbdraw - options; bottom>` [:ref:`boolean <boolean>`] (default: ``false``) Render the bottom side of the board (default is top side).
-  **format** :index:`: <pair: output - pcbdraw - options; format>` [:ref:`string <string>`] (default: ``'svg'``) (choices: "svg", "png", "jpg", "bmp") Output format. Only used if no `output` is specified.
-  **mirror** :index:`: <pair: output - pcbdraw - options; mirror>` [:ref:`boolean <boolean>`] (default: ``false``) Mirror the board.
-  **output** :index:`: <pair: output - pcbdraw - options; output>` [:ref:`string <string>`] (default: ``'%f-%i%I%v.%x'``) Name for the generated file. Affected by global options.
-  **show_components** :index:`: <pair: output - pcbdraw - options; show_components>` [:ref:`list(string) <list(string)>` | :ref:`string <string>`] (default: ``'none'``) (choices: "none", "all") (also accepts any string) List of components to draw, can be also a string for none or all.
   The default is none.
   There two ways of using this option, please consult the `add_to_variant` option.
   You can use `_kf(FILTER)` as an element in the list to get all the components that pass the filter.
   You can even use `_kf(FILTER1;FILTER2)` to concatenate filters.

-  **style** :index:`: <pair: output - pcbdraw - options; style>`  [:ref:`PcbDrawStyle parameters <PcbDrawStyle>`] [:ref:`string <string>` | :ref:`dict <dict>`] (default: empty dict, default values used) PCB style (colors). An internal name, the name of a JSON file or the style options.
-  ``add_to_variant`` :index:`: <pair: output - pcbdraw - options; add_to_variant>` [:ref:`boolean <boolean>`] (default: ``true``) The `show_components` list is added to the list of components indicated by the variant (fitted and not
   excluded).
   This is the old behavior, but isn't intuitive because the `show_components` meaning changes when a variant
   is used. In this mode you should avoid using `show_components` and variants.
   To get a more coherent behavior disable this option, and `none` will always be `none`.
   Also `all` will be what the variant says.
-  ``dnf_filter`` :index:`: <pair: output - pcbdraw - options; dnf_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to mark components as not fitted.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``dpi`` :index:`: <pair: output - pcbdraw - options; dpi>` [:ref:`number <number>`] (default: ``300``) (range: 10 to 1200) Dots per inch (resolution) of the generated image.
-  ``highlight`` :index:`: <pair: output - pcbdraw - options; highlight>` [:ref:`list(string) <list(string)>`] (default: ``[]``) List of components to highlight. Filter expansion is also allowed here,
   see `show_components`.

-  ``libs`` :index:`: <pair: output - pcbdraw - options; libs>` [:ref:`list(string) <list(string)>`] (default: ``['KiCAD-base']``) List of libraries.

-  ``margin`` :index:`: <pair: output - pcbdraw - options; margin>`  [:ref:`PcbMargin parameters <PcbMargin>`] [:ref:`number <number>` | :ref:`dict <dict>`] (default: ``0``) Margin around the generated image [mm].
   Using a number the margin is the same in the four directions.
-  ``no_drillholes`` :index:`: <pair: output - pcbdraw - options; no_drillholes>` [:ref:`boolean <boolean>`] (default: ``false``) Do not make holes transparent.
-  ``outline_width`` :index:`: <pair: output - pcbdraw - options; outline_width>` [:ref:`number <number>`] (default: ``0.15``) (range: 0 to 10) Width of the trace to draw the PCB border [mm].
   Note this also affects the drill holes.
-  ``placeholder`` :index:`: <pair: output - pcbdraw - options; placeholder>` [:ref:`boolean <boolean>`] (default: ``false``) Show placeholder for missing components.
-  ``pre_transform`` :index:`: <pair: output - pcbdraw - options; pre_transform>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to transform fields before applying other filters.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``remap`` :index:`: <pair: output - pcbdraw - options; remap>` [:ref:`string_dict <string_dict>` | :ref:`string <string>`] (default: ``'None'``) (DEPRECATED) Replacements for PCB references using specified components
   (lib:component). Use `remap_components` instead.

-  ``remap_components`` :index:`: <pair: output - pcbdraw - options; remap_components>`  [:ref:`PcbDrawRemapComponents parameters <PcbDrawRemapComponents>`] [:ref:`list(dict) <list(dict)>`] (default: ``[]``) Replacements for PCB references using specified components.
   Replaces `remap` with type check.
-  ``resistor_flip`` :index:`: <pair: output - pcbdraw - options; resistor_flip>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``''``) [:ref:`comma separated <comma_sep>`] List of resistors to flip its bands.

-  ``resistor_remap`` :index:`: <pair: output - pcbdraw - options; resistor_remap>`  [:ref:`PcbDrawResistorRemap parameters <PcbDrawResistorRemap>`] [:ref:`list(dict) <list(dict)>`] (default: ``[]``) List of resistors to be remapped. You can change the value of the resistors here.
-  ``show_solderpaste`` :index:`: <pair: output - pcbdraw - options; show_solderpaste>` [:ref:`boolean <boolean>`] (default: ``true``) Show the solder paste layers.
-  ``size_detection`` :index:`: <pair: output - pcbdraw - options; size_detection>` [:ref:`string <string>`] (default: ``'kicad_edge'``) (choices: "kicad_edge", "kicad_all", "svg_paths") Method used to detect the size of the resulting image.
   The `kicad_edge` method uses the size of the board as reported by KiCad,
   components that extend beyond the PCB limit will be cropped. You can manually
   adjust the margins to make them visible.
   The `kicad_all` method uses the whole size reported by KiCad. Usually includes extra space.
   The `svg_paths` uses all visible drawings in the image. To use this method you
   must install the `numpy` Python module (may not be available in docker images).
-  ``svg_precision`` :index:`: <pair: output - pcbdraw - options; svg_precision>` [:ref:`number <number>`] (default: ``4``) (range: 3 to 6) Scale factor used to represent 1 mm in the SVG (KiCad 6).
   The value is how much zeros has the multiplier (1 mm = 10 power `svg_precision` units).
   Note that for an A4 paper Firefox 91 and Chrome 105 can't handle more than 5.
-  ``variant`` :index:`: <pair: output - pcbdraw - options; variant>` [:ref:`string <string>`] (default: ``''``) Board variant to apply.
-  ``vcuts`` :index:`: <pair: output - pcbdraw - options; vcuts>` [:ref:`boolean <boolean>`] (default: ``false``) Render V-CUTS on the `vcuts_layer` layer.
-  ``vcuts_layer`` :index:`: <pair: output - pcbdraw - options; vcuts_layer>` [:ref:`string <string>`] (default: ``'Cmts.User'``) Layer to render the V-CUTS, only used when `vcuts` is enabled.
   Note that any other content from this layer will be included.
-  ``warnings`` :index:`: <pair: output - pcbdraw - options; warnings>` [:ref:`string <string>`] (default: ``'visible'``) (choices: "visible", "all", "none") Using visible only the warnings about components in the visible side are generated.

.. toctree::
   :caption: Used dicts

   PcbDrawRemapComponents
   PcbDrawResistorRemap
   PcbDrawStyle
   PcbMargin
