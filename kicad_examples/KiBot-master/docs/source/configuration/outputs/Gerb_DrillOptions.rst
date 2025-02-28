.. _Gerb_DrillOptions:


Gerb_DrillOptions parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **output** :index:`: <pair: output - gerb_drill - options; output>` [:ref:`string <string>`] (default: ``'%f-%i%I%v.%x'``) name for the drill file, KiCad defaults if empty (%i='PTH_drill'). Affected by global options.
-  ``dnf_filter`` :index:`: <pair: output - gerb_drill - options; dnf_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to mark components as not fitted.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``map`` :index:`: <pair: output - gerb_drill - options; map>`  [:ref:`DrillMap parameters <DrillMap>`] [:ref:`dict <dict>` | :ref:`string <string>`] (default: ``'None'``) (choices: "hpgl", "ps", "gerber", "dxf", "svg", "pdf", "None") Format for a graphical drill map.
   Not generated unless a format is specified.
-  ``npth_id`` :index:`: <pair: output - gerb_drill - options; npth_id>` [:ref:`string <string>`] Force this replacement for %i when generating NPTH files.
-  ``pre_transform`` :index:`: <pair: output - gerb_drill - options; pre_transform>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to transform fields before applying other filters.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``pth_id`` :index:`: <pair: output - gerb_drill - options; pth_id>` [:ref:`string <string>`] Force this replacement for %i when generating PTH and unified files.
-  ``report`` :index:`: <pair: output - gerb_drill - options; report>`  [:ref:`DrillReport parameters <DrillReport>`] [:ref:`dict <dict>` | :ref:`string <string>`] (default: ``''``) Name of the drill report. Not generated unless a name is specified.
-  ``use_aux_axis_as_origin`` :index:`: <pair: output - gerb_drill - options; use_aux_axis_as_origin>` [:ref:`boolean <boolean>`] (default: ``false``) Use the auxiliary axis as origin for coordinates.
-  ``variant`` :index:`: <pair: output - gerb_drill - options; variant>` [:ref:`string <string>`] (default: ``''``) Board variant to apply.
   Used for sub-PCBs.

.. toctree::
   :caption: Used dicts

   DrillMap
   DrillReport
