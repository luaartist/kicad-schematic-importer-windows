.. _ExcellonOptions:


ExcellonOptions parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **metric_units** :index:`: <pair: output - excellon - options; metric_units>` [:ref:`boolean <boolean>`] (default: ``true``) Use metric units instead of inches.
-  **mirror_y_axis** :index:`: <pair: output - excellon - options; mirror_y_axis>` [:ref:`boolean <boolean>`] (default: ``false``) Invert the Y axis.
-  **output** :index:`: <pair: output - excellon - options; output>` [:ref:`string <string>`] (default: ``'%f-%i%I%v.%x'``) name for the drill file, KiCad defaults if empty (%i='PTH_drill'). Affected by global options.
-  **pth_and_npth_single_file** :index:`: <pair: output - excellon - options; pth_and_npth_single_file>` [:ref:`boolean <boolean>`] (default: ``true``) Generate one file for both, plated holes and non-plated holes, instead of two separated files.
-  ``dnf_filter`` :index:`: <pair: output - excellon - options; dnf_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to mark components as not fitted.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``left_digits`` :index:`: <pair: output - excellon - options; left_digits>` [:ref:`number <number>`] (default: ``0``) number of digits for integer part of coordinates (0 is auto).
-  ``map`` :index:`: <pair: output - excellon - options; map>`  [:ref:`DrillMap parameters <DrillMap>`] [:ref:`dict <dict>` | :ref:`string <string>`] (default: ``'None'``) (choices: "hpgl", "ps", "gerber", "dxf", "svg", "pdf", "None") Format for a graphical drill map.
   Not generated unless a format is specified.
-  ``minimal_header`` :index:`: <pair: output - excellon - options; minimal_header>` [:ref:`boolean <boolean>`] (default: ``false``) Use a minimal header in the file.
-  ``npth_id`` :index:`: <pair: output - excellon - options; npth_id>` [:ref:`string <string>`] Force this replacement for %i when generating NPTH files.
-  ``pre_transform`` :index:`: <pair: output - excellon - options; pre_transform>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to transform fields before applying other filters.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``pth_id`` :index:`: <pair: output - excellon - options; pth_id>` [:ref:`string <string>`] Force this replacement for %i when generating PTH and unified files.
-  ``report`` :index:`: <pair: output - excellon - options; report>`  [:ref:`DrillReport parameters <DrillReport>`] [:ref:`dict <dict>` | :ref:`string <string>`] (default: ``''``) Name of the drill report. Not generated unless a name is specified.
-  ``right_digits`` :index:`: <pair: output - excellon - options; right_digits>` [:ref:`number <number>`] (default: ``0``) number of digits for mantissa part of coordinates (0 is auto).
-  ``route_mode_for_oval_holes`` :index:`: <pair: output - excellon - options; route_mode_for_oval_holes>` [:ref:`boolean <boolean>`] (default: ``true``) Use route command for oval holes (G00), otherwise use G85.
-  ``use_aux_axis_as_origin`` :index:`: <pair: output - excellon - options; use_aux_axis_as_origin>` [:ref:`boolean <boolean>`] (default: ``false``) Use the auxiliary axis as origin for coordinates.
-  ``variant`` :index:`: <pair: output - excellon - options; variant>` [:ref:`string <string>`] (default: ``''``) Board variant to apply.
   Used for sub-PCBs.
-  ``zeros_format`` :index:`: <pair: output - excellon - options; zeros_format>` [:ref:`string <string>`] (default: ``'DECIMAL_FORMAT'``) (choices: "DECIMAL_FORMAT", "SUPPRESS_LEADING", "SUPPRESS_TRAILING", "KEEP_ZEROS") How to handle the zeros.

.. toctree::
   :caption: Used dicts

   DrillMap
   DrillReport
