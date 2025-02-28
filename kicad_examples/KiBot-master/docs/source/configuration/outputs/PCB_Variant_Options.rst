.. _PCB_Variant_Options:


PCB_Variant_Options parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **output** :index:`: <pair: output - pcb_variant - options; output>` [:ref:`string <string>`] (default: ``'%f-%i%I%v.%x'``) Filename for the output (%i=variant, %x=kicad_pcb). Affected by global options.
-  ``copy_project`` :index:`: <pair: output - pcb_variant - options; copy_project>` [:ref:`boolean <boolean>`] (default: ``true``) Copy the KiCad project to the destination directory.
-  ``dnf_filter`` :index:`: <pair: output - pcb_variant - options; dnf_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to mark components as not fitted.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``hide_excluded`` :index:`: <pair: output - pcb_variant - options; hide_excluded>` [:ref:`boolean <boolean>`] (default: ``false``) Hide components in the Fab layer that are marked as excluded by a variant.
   Affected by global options.
-  ``pre_transform`` :index:`: <pair: output - pcb_variant - options; pre_transform>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to transform fields before applying other filters.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``title`` :index:`: <pair: output - pcb_variant - options; title>` [:ref:`string <string>`] (default: ``''``) Text used to replace the sheet title. %VALUE expansions are allowed.
   If it starts with `+` the text is concatenated.
-  ``variant`` :index:`: <pair: output - pcb_variant - options; variant>` [:ref:`string <string>`] (default: ``''``) Board variant to apply.

