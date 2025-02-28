.. _ReportOptions:


ReportOptions parameters
~~~~~~~~~~~~~~~~~~~~~~~~

-  **convert_to** :index:`: <pair: output - report - options; convert_to>` [:ref:`string <string>`] (default: ``'pdf'``) Target format for the report conversion. See `do_convert`.
-  **do_convert** :index:`: <pair: output - report - options; do_convert>` [:ref:`boolean <boolean>`] (default: ``false``) Run `Pandoc` to convert the report. Note that Pandoc must be installed.
   The conversion is done assuming the report is in `convert_from` format.
   The output file will be in `convert_to` format.
   The available formats depends on the `Pandoc` installation.
   In CI/CD environments: the `kicad_auto_test` docker image contains it.
   In Debian/Ubuntu environments: install `pandoc`, `texlive`, `texlive-latex-base` and `texlive-latex-recommended`.
-  **output** :index:`: <pair: output - report - options; output>` [:ref:`string <string>`] (default: ``'%f-%i%I%v.%x'``) Output file name (%i='report', %x='txt'). Affected by global options.
-  **template** :index:`: <pair: output - report - options; template>` [:ref:`string <string>`] (default: ``'full'``) (choices: "full", "full_svg", "simple", "testpoints") (also accepts any string) Name for one of the internal templates or a custom template file.
   Environment variables and ~ are allowed.
   Note: when converting to PDF PanDoc can fail on some Unicode values (use `simple_ASCII`).
   Note: the testpoint variables uses the `testpoint` fabrication attribute of pads.
-  ``alloy_specific_gravity`` :index:`: <pair: output - report - options; alloy_specific_gravity>` [:ref:`number <number>`] (default: ``7.4``) Specific gravity of the alloy used for the solder paste, in g/cm3. Used to compute solder paste usage.
-  ``convert_from`` :index:`: <pair: output - report - options; convert_from>` [:ref:`string <string>`] (default: ``'markdown'``) Original format for the report conversion. Current templates are `markdown`. See `do_convert`.
-  ``converted_output`` :index:`: <pair: output - report - options; converted_output>` [:ref:`string <string>`] (default: ``'%f-%i%I%v.%x'``) Converted output file name (%i='report', %x=`convert_to`).
   Note that the extension should match the `convert_to` value. Affected by global options.
-  ``dnf_filter`` :index:`: <pair: output - report - options; dnf_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to mark components as not fitted.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``eurocircuits_class_target`` :index:`: <pair: output - report - options; eurocircuits_class_target>` [:ref:`string <string>`] (default: ``'10F'``) Which Eurocircuits class are we aiming at.
-  ``eurocircuits_reduce_holes`` :index:`: <pair: output - report - options; eurocircuits_reduce_holes>` [:ref:`number <number>`] (default: ``0.45``) When computing the Eurocircuits category: Final holes sizes smaller or equal to this given
   diameter can be reduced to accommodate the correct annular ring values.
   Use 0 to disable it.
-  ``flux_specific_gravity`` :index:`: <pair: output - report - options; flux_specific_gravity>` [:ref:`number <number>`] (default: ``1.0``) Specific gravity of the flux used for the solder paste, in g/cm3. Used to compute solder paste usage.
-  ``pre_transform`` :index:`: <pair: output - report - options; pre_transform>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to transform fields before applying other filters.
   A short-cut to use for simple cases where a variant is an overkill.

-  ``solder_paste_metal_amount`` :index:`: <pair: output - report - options; solder_paste_metal_amount>` [:ref:`number <number>`] (default: ``87.75``) (range: 0 to 100) Amount of metal in the solder paste (percentage). Used to compute solder paste usage.
-  ``stencil_thickness`` :index:`: <pair: output - report - options; stencil_thickness>` [:ref:`number <number>`] (default: ``0.12``) Stencil thickness in mm. Used to compute solder paste usage.
-  ``variant`` :index:`: <pair: output - report - options; variant>` [:ref:`string <string>`] (default: ``''``) Board variant to apply.

