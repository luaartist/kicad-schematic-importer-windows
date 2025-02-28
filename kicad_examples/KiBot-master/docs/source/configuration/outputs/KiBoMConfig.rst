.. _KiBoMConfig:


KiBoMConfig parameters
~~~~~~~~~~~~~~~~~~~~~~

-  **columns** :index:`: <pair: output - kibom - options - conf; columns>`  [:ref:`KiBoMColumns parameters <KiBoMColumns>`] [:ref:`list(dict) <list(dict)>` | :ref:`list(string) <list(string)>`] (default: ``[]``) List of columns to display.
   Can be just the name of the field.
-  **fit_field** :index:`: <pair: output - kibom - options - conf; fit_field>` [:ref:`string <string>`] (default: ``'Config'``) Field name used to determine if a particular part is to be fitted (also DNC and variants).
-  **group_fields** :index:`: <pair: output - kibom - options - conf; group_fields>` [:ref:`list(string) <list(string)>`] (default: ``['Part', 'Part Lib', 'Value', 'Footprint', 'Footprint Lib']``) List of fields used for sorting individual components into groups.
   Components which match (comparing *all* fields) will be grouped together.
   Field names are case-insensitive.
   If empty: ['Part', 'Part Lib', 'Value', 'Footprint', 'Footprint Lib'] is used.

-  **ignore_dnf** :index:`: <pair: output - kibom - options - conf; ignore_dnf>` [:ref:`boolean <boolean>`] (default: ``true``) Exclude DNF (Do Not Fit) components.
-  **number_rows** :index:`: <pair: output - kibom - options - conf; number_rows>` [:ref:`boolean <boolean>`] (default: ``true``) First column is the row number.
-  ``component_aliases`` :index:`: <pair: output - kibom - options - conf; component_aliases>` [:ref:`list(list(string)) <list(list(string))>`] (default: ``[['r', 'r_small', 'res', 'resistor'], ['l', 'l_small', 'inductor'], ['c', 'c_small', 'cap', 'capacitor'], ['sw', 'switch'], ['zener', 'zenersmall'], ['d', 'diode', 'd_small']]``) A series of values which are considered to be equivalent for the part name.
   Each entry is a list of equivalen names. Example: ['c', 'c_small', 'cap' ]
   will ensure the equivalent capacitor symbols can be grouped together.
   If empty the following aliases are used:

   - ['r', 'r_small', 'res', 'resistor']
   - ['l', 'l_small', 'inductor']
   - ['c', 'c_small', 'cap', 'capacitor']
   - ['sw', 'switch']
   - ['zener', 'zenersmall']
   - ['d', 'diode', 'd_small'].

-  ``datasheet_as_link`` :index:`: <pair: output - kibom - options - conf; datasheet_as_link>` [:ref:`string <string>`] (default: ``''``) Column with links to the datasheet (HTML only).
-  ``digikey_link`` :index:`: <pair: output - kibom - options - conf; digikey_link>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``''``) Column/s containing Digi-Key part numbers, will be linked to web page (HTML only).

-  ``exclude_any`` :index:`: <pair: output - kibom - options - conf; exclude_any>`  [:ref:`KiBoMRegex parameters <KiBoMRegex>`] [:ref:`list(dict) <list(dict)>`] (default: ``[]``) A series of regular expressions used to exclude parts.
   If a component matches ANY of these, it will be excluded.
   Column names are case-insensitive.
   If empty the following list is used by KiBoM:

   - column: References |br|
     regex: '^TP[0-9]*'
   - column: References |br|
     regex: '^FID'
   - column: Part |br|
     regex: 'mount.*hole'
   - column: Part |br|
     regex: 'solder.*bridge'
   - column: Part |br|
     regex: 'test.*point'
   - column: Footprint |br|
     regex 'test.*point'
   - column: Footprint |br|
     regex: 'mount.*hole'
   - column: Footprint |br|
     regex: 'fiducial'.
-  ``group_connectors`` :index:`: <pair: output - kibom - options - conf; group_connectors>` [:ref:`boolean <boolean>`] (default: ``true``) Connectors with the same footprints will be grouped together, independent of the name of the connector.
-  ``hide_headers`` :index:`: <pair: output - kibom - options - conf; hide_headers>` [:ref:`boolean <boolean>`] (default: ``false``) Hide column headers.
-  ``hide_pcb_info`` :index:`: <pair: output - kibom - options - conf; hide_pcb_info>` [:ref:`boolean <boolean>`] (default: ``false``) Hide project information.
-  ``html_generate_dnf`` :index:`: <pair: output - kibom - options - conf; html_generate_dnf>` [:ref:`boolean <boolean>`] (default: ``true``) Generate a separated section for DNF (Do Not Fit) components (HTML only).
-  ``include_only`` :index:`: <pair: output - kibom - options - conf; include_only>`  [:ref:`KiBoMRegex parameters <KiBoMRegex>`] [:ref:`list(dict) <list(dict)>`] (default: ``[]``) A series of regular expressions used to select included parts.
   If there are any regex defined here, only components that match against ANY of them will be included.
   Column names are case-insensitive.
   If empty all the components are included.
-  ``lcsc_link`` :index:`: <pair: output - kibom - options - conf; lcsc_link>` [:ref:`boolean <boolean>` | :ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``''``) Column/s containing LCSC part numbers, will be linked to web page.
   Use **true** to copy the value indicated by the `field_lcsc_part` global option.

-  ``merge_blank_fields`` :index:`: <pair: output - kibom - options - conf; merge_blank_fields>` [:ref:`boolean <boolean>`] (default: ``true``) Component groups with blank fields will be merged into the most compatible group, where possible.
-  ``mouser_link`` :index:`: <pair: output - kibom - options - conf; mouser_link>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``''``) Column/s containing Mouser part numbers, will be linked to web page (HTML only).

-  ``ref_separator`` :index:`: <pair: output - kibom - options - conf; ref_separator>` [:ref:`string <string>`] (default: ``' '``) Separator used for the list of references.
-  ``test_regex`` :index:`: <pair: output - kibom - options - conf; test_regex>` [:ref:`boolean <boolean>`] (default: ``true``) Each component group will be tested against a number of regular-expressions.
-  ``use_alt`` :index:`: <pair: output - kibom - options - conf; use_alt>` [:ref:`boolean <boolean>`] (default: ``false``) Print grouped references in the alternate compressed style eg: R1-R7,R18.

.. toctree::
   :caption: Used dicts

   KiBoMColumns
   KiBoMRegex
