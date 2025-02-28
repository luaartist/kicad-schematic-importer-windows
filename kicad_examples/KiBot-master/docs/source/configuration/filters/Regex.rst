.. _Regex_fi:


Regex parameters
~~~~~~~~~~~~~~~~

-  ``angle`` :index:`: <pair: filter - rot_footprint - rotations_and_offsets; angle>` [:ref:`number <number>`] (default: ``0.0``) Rotation offset to apply to the matched component.
-  ``apply_angle`` :index:`: <pair: filter - rot_footprint - rotations_and_offsets; apply_angle>` [:ref:`boolean <boolean>`] (default: ``true``) Apply the angle offset.
-  ``apply_offset`` :index:`: <pair: filter - rot_footprint - rotations_and_offsets; apply_offset>` [:ref:`boolean <boolean>`] (default: ``true``) Apply the position offset.
-  ``field`` :index:`: <pair: filter - rot_footprint - rotations_and_offsets; field>` [:ref:`string <string>`] (default: ``'footprint'``) Name of field to apply the regular expression.
   Use `_field_lcsc_part` to get the value defined in the global options.
   Use `Footprint` for the name of the footprint without a library.
   Use `Full Footprint` for the name of the footprint including the library.
-  ``offset_x`` :index:`: <pair: filter - rot_footprint - rotations_and_offsets; offset_x>` [:ref:`number <number>`] (default: ``0.0``) X position offset to apply to the matched component.
-  ``offset_y`` :index:`: <pair: filter - rot_footprint - rotations_and_offsets; offset_y>` [:ref:`number <number>`] (default: ``0.0``) Y position offset to apply to the matched component.
-  ``regex`` :index:`: <pair: filter - rot_footprint - rotations_and_offsets; regex>` [:ref:`string <string>`] (default: ``''``) Regular expression to match.
-  *regexp* :index:`: <pair: filter - rot_footprint - rotations_and_offsets; regexp>` Alias for regex.

