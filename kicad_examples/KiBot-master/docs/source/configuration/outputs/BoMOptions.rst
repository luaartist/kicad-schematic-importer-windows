.. _BoMOptions:


BoMOptions parameters
~~~~~~~~~~~~~~~~~~~~~

-  **columns** :index:`: <pair: output - bom - options; columns>`  [:ref:`BoMColumns parameters <BoMColumns>`] [:ref:`list(dict) <list(dict)>` | :ref:`list(string) <list(string)>`] (default: computed for your project) List of columns to display.
   Can be just the name of the field.
   In addition to all user defined fields you have various special columns, consult :ref:`bom_columns`.
-  **csv** :index:`: <pair: output - bom - options; csv>`  [:ref:`BoMCSV parameters <BoMCSV>`] [:ref:`dict <dict>`] (default: empty dict, default values used) Options for the CSV, TXT and TSV formats.
-  **format** :index:`: <pair: output - bom - options; format>` [:ref:`string <string>`] (default: ``'Auto'``) (choices: "HTML", "CSV", "TXT", "TSV", "XML", "XLSX", "HRTXT", "Auto") format for the BoM.
   `Auto` defaults to CSV or a guess according to the options.
   HRTXT stands for Human Readable TeXT.
-  **group_fields** :index:`: <pair: output - bom - options; group_fields>` [:ref:`list(string) <list(string)>`] (default: ``['part', 'part lib', 'value', 'footprint', 'footprint lib', 'voltage', 'tolerance', 'current', 'power']``) [:ref:`case insensitive <no_case>`]List of fields used for sorting individual components into groups.
   Components which match (comparing *all* fields) will be grouped together.
   Field names are case-insensitive.
   For empty fields the behavior is defined by the `group_fields_fallbacks`, `merge_blank_fields` and
   `merge_both_blank` options.
   Note that for resistors, capacitors and inductors the _Value_ field is parsed and qualifiers, like
   tolerance, are discarded. Please use a separated field and disable `merge_blank_fields` if this
   information is important. You can also disable `parse_value`.
   If empty: ['Part', 'Part Lib', 'Value', 'Footprint', 'Footprint Lib',
   'Voltage', 'Tolerance', 'Current', 'Power'] is used.

-  **hrtxt** :index:`: <pair: output - bom - options; hrtxt>`  [:ref:`BoMTXT parameters <BoMTXT>`] [:ref:`dict <dict>`] (default: empty dict, default values used) Options for the HRTXT formats.
-  **html** :index:`: <pair: output - bom - options; html>`  [:ref:`BoMHTML parameters <BoMHTML>`] [:ref:`dict <dict>`] (default: empty dict, default values used) Options for the HTML format.
-  **ignore_dnf** :index:`: <pair: output - bom - options; ignore_dnf>` [:ref:`boolean <boolean>`] (default: ``true``) Exclude DNF (Do Not Fit) components.
-  **normalize_values** :index:`: <pair: output - bom - options; normalize_values>` [:ref:`boolean <boolean>`] (default: ``false``) Try to normalize the R, L and C values, producing uniform units and prefixes.
-  **number** :index:`: <pair: output - bom - options; number>` [:ref:`number <number>`] (default: ``1``) Number of boards to build (components multiplier).
-  **output** :index:`: <pair: output - bom - options; output>` [:ref:`string <string>`] (default: ``'%f-%i%I%v.%x'``) filename for the output (%i=bom). Affected by global options.
-  **sort_style** :index:`: <pair: output - bom - options; sort_style>` [:ref:`string <string>`] (default: ``'type_value'``) (choices: "type_value", "type_value_ref", "ref") Sorting criteria.
-  **units** :index:`: <pair: output - bom - options; units>` [:ref:`string <string>`] (default: ``'millimeters'``) (choices: "millimeters", "inches", "mils") Units used for the positions ('Footprint X' and 'Footprint Y' columns).
   Affected by global options.
-  **xlsx** :index:`: <pair: output - bom - options; xlsx>`  [:ref:`BoMXLSX parameters <BoMXLSX>`] [:ref:`dict <dict>`] (default: empty dict, default values used) Options for the XLSX format.
-  ``aggregate`` :index:`: <pair: output - bom - options; aggregate>`  [:ref:`Aggregate parameters <Aggregate>`] [:ref:`list(dict) <list(dict)>`] (default: ``[]``) Add components from other projects.
   You can use CSV files, the first row must contain the names of the fields.
   The `Reference` and `Value` are mandatory, in most cases `Part` is also needed.
   The `Part` column should contain the name/type of the component. This is important for
   passive components (R, L, C, etc.). If this information isn't available consider
   configuring the grouping to exclude the `Part`..
-  ``angle_positive`` :index:`: <pair: output - bom - options; angle_positive>` [:ref:`boolean <boolean>`] (default: ``true``) Always use positive values for the footprint rotation.
-  ``bottom_negative_x`` :index:`: <pair: output - bom - options; bottom_negative_x>` [:ref:`boolean <boolean>`] (default: ``false``) Use negative X coordinates for footprints on bottom layer (for XYRS).
-  ``component_aliases`` :index:`: <pair: output - bom - options; component_aliases>` [:ref:`list(list(string)) <list(list(string))>`] (default: ``[['r', 'r_small', 'res', 'resistor'], ['l', 'l_small', 'inductor'], ['c', 'c_small', 'cap', 'capacitor'], ['sw', 'switch'], ['zener', 'zenersmall'], ['d', 'diode', 'd_small']]``) A series of values which are considered to be equivalent for the part name.
   Each entry is a list of equivalen names. Example: ['c', 'c_small', 'cap' ]
   will ensure the equivalent capacitor symbols can be grouped together.
   If empty the following aliases are used:

   - ['r', 'r_small', 'res', 'resistor']
   - ['l', 'l_small', 'inductor']
   - ['c', 'c_small', 'cap', 'capacitor']
   - ['sw', 'switch']
   - ['zener', 'zenersmall']
   - ['d', 'diode', 'd_small'].

-  ``cost_extra_columns`` :index:`: <pair: output - bom - options; cost_extra_columns>`  [:ref:`BoMColumns parameters <BoMColumns>`] [:ref:`list(dict) <list(dict)>` | :ref:`list(string) <list(string)>`] (default: ``[]``) List of columns to add to the global section of the cost.
   Can be just the name of the field.
-  ``count_smd_tht`` :index:`: <pair: output - bom - options; count_smd_tht>` [:ref:`boolean <boolean>`] (default: ``false``) Show the stats about how many of the components are SMD/THT. You must provide the PCB.
-  ``distributors`` :index:`: <pair: output - bom - options; distributors>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``[]``) [:ref:`comma separated <comma_sep>`] Include this distributors list. Default is all the available.

-  ``dnc_filter`` :index:`: <pair: output - bom - options; dnc_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_kibom_dnc_CONFIG_FIELD'``) Name of the filter to mark components as 'Do Not Change'.
   The default filter marks components with a DNC value or DNC in the Config field.
   This option is for simple cases, consider using a full variant for complex cases.

-  ``dnf_filter`` :index:`: <pair: output - bom - options; dnf_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_kibom_dnf_CONFIG_FIELD'``) Name of the filter to mark components as 'Do Not Fit'.
   The default filter marks components with a DNF value or DNF in the Config field.
   This option is for simple cases, consider using a full variant for complex cases.

-  ``exclude_filter`` :index:`: <pair: output - bom - options; exclude_filter>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_mechanical'``) Name of the filter to exclude components from BoM processing.
   The default filter (built-in filter '_mechanical') excludes test points, fiducial marks, mounting holes, etc.
   Please consult the built-in filters explanation to fully understand what is excluded by default.
   This option is for simple cases, consider using a full variant for complex cases.

-  ``exclude_marked_in_pcb`` :index:`: <pair: output - bom - options; exclude_marked_in_pcb>` [:ref:`boolean <boolean>`] (default: ``false``) Exclude components marked with *Exclude from BOM* in the PCB.
   This is a KiCad 6 option.
-  ``exclude_marked_in_sch`` :index:`: <pair: output - bom - options; exclude_marked_in_sch>` [:ref:`boolean <boolean>`] (default: ``true``) Exclude components marked with *Exclude from bill of materials* in the schematic.
   This is a KiCad 6 option.
-  ``expand_text_vars`` :index:`: <pair: output - bom - options; expand_text_vars>` [:ref:`boolean <boolean>`] (default: ``true``) Expand KiCad 6 text variables after applying all filters and variants.
   This is done using a **_expand_text_vars** filter.
   If you need to customize the filter, or apply it before, you can disable this option and
   add a custom filter to the filter chain.
-  ``fit_field`` :index:`: <pair: output - bom - options; fit_field>` [:ref:`string <string>`] (default: ``'config'``) [:ref:`case insensitive <no_case>`]Field name used for internal filters (not for variants).
-  ``footprint_populate_values`` :index:`: <pair: output - bom - options; footprint_populate_values>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'no,yes'``) [:ref:`comma separated <comma_sep>`] (must contain 2 elements) Values for the `Footprint Populate` column.

-  ``footprint_type_values`` :index:`: <pair: output - bom - options; footprint_type_values>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'SMD,THT,VIRTUAL'``) [:ref:`comma separated <comma_sep>`] (must contain 3 elements) Values for the `Footprint Type` column.

-  ``group_connectors`` :index:`: <pair: output - bom - options; group_connectors>` [:ref:`boolean <boolean>`] (default: ``true``) Connectors with the same footprints will be grouped together, independent of the name of the connector.
-  ``group_fields_fallbacks`` :index:`: <pair: output - bom - options; group_fields_fallbacks>` [:ref:`list(string) <list(string)>`] (default: ``[]``) [:ref:`case insensitive <no_case>`]List of fields to be used when the fields in `group_fields` are empty.
   The first field in this list is the fallback for the first in `group_fields`, and so on.

-  ``int_qtys`` :index:`: <pair: output - bom - options; int_qtys>` [:ref:`boolean <boolean>`] (default: ``true``) Component quantities are always expressed as integers. Using the ceil() function.
-  ``merge_blank_fields`` :index:`: <pair: output - bom - options; merge_blank_fields>` [:ref:`boolean <boolean>`] (default: ``true``) Component groups with blank fields will be merged into the most compatible group, where possible.
-  ``merge_both_blank`` :index:`: <pair: output - bom - options; merge_both_blank>` [:ref:`boolean <boolean>`] (default: ``true``) When creating groups two components with empty/missing field will be interpreted as with the same value.
-  ``no_conflict`` :index:`: <pair: output - bom - options; no_conflict>` [:ref:`list(string) <list(string)>`] (default: computed for your project) [:ref:`case insensitive <no_case>`]List of fields where we tolerate conflicts.
   Use it to avoid undesired warnings.
   By default the field indicated in `fit_field`, the field used for variants and
   the field `part` are excluded.

-  ``no_distributors`` :index:`: <pair: output - bom - options; no_distributors>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``[]``) [:ref:`comma separated <comma_sep>`] Exclude this distributors list.
   They are removed after computing `distributors`.

-  ``normalize_locale`` :index:`: <pair: output - bom - options; normalize_locale>` [:ref:`boolean <boolean>`] (default: ``false``) When normalizing values use the locale decimal point.
-  ``parse_value`` :index:`: <pair: output - bom - options; parse_value>` [:ref:`boolean <boolean>`] (default: ``true``) Parse the `Value` field so things like *1k* and *1000* are interpreted as equal.
   Note that this implies that *1k 1%* is the same as *1k 5%*. If you really need to group using the
   extra information split it in separated fields, add the fields to `group_fields` and disable
   `merge_blank_fields`.
-  ``pre_transform`` :index:`: <pair: output - bom - options; pre_transform>` [:ref:`string <string>` | :ref:`list(string) <list(string)>`] (default: ``'_null'``) Name of the filter to transform fields before applying other filters.
   This option is for simple cases, consider using a full variant for complex cases.

-  ``ref_id`` :index:`: <pair: output - bom - options; ref_id>` [:ref:`string <string>`] (default: ``''``) A prefix to add to all the references from this project. Used for multiple projects.
-  ``ref_separator`` :index:`: <pair: output - bom - options; ref_separator>` [:ref:`string <string>`] (default: ``' '``) Separator used for the list of references.
-  ``source_by_id`` :index:`: <pair: output - bom - options; source_by_id>` [:ref:`boolean <boolean>`] (default: ``false``) Generate the `Source BoM` column using the reference ID instead of the project name.
-  ``use_alt`` :index:`: <pair: output - bom - options; use_alt>` [:ref:`boolean <boolean>`] (default: ``false``) Print grouped references in the alternate compressed style eg: R1-R7,R18.
-  ``use_aux_axis_as_origin`` :index:`: <pair: output - bom - options; use_aux_axis_as_origin>` [:ref:`boolean <boolean>`] (default: ``true``) Use the auxiliary axis as origin for coordinates (KiCad default) (for XYRS).
-  ``variant`` :index:`: <pair: output - bom - options; variant>` [:ref:`string <string>`] (default: ``'_kibom_simple'``) Board variant, used to determine which components are output to the BoM.
   The `_kibom_simple` variant is a KiBoM variant without any filters and it provides some basic
   compatibility with KiBoM. Note that this output has default filters that behaves like KiBoM.
   The combination between the default for this option and the defaults for the filters provides
   a behavior that mimics KiBoM default behavior.

.. toctree::
   :caption: Used dicts

   Aggregate
   BoMCSV
   BoMColumns
   BoMHTML
   BoMTXT
   BoMXLSX
