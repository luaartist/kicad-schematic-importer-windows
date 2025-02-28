.. _KiCadVariable:


KiCadVariable parameters
~~~~~~~~~~~~~~~~~~~~~~~~

-  ``after`` :index:`: <pair: preflight - set_text_variables - set_text_variables; after>` [:ref:`string <string>`] (default: ``''``) Text to add after the output of `command`.
-  ``before`` :index:`: <pair: preflight - set_text_variables - set_text_variables; before>` [:ref:`string <string>`] (default: ``''``) Text to add before the output of `command`.
-  ``command`` :index:`: <pair: preflight - set_text_variables - set_text_variables; command>` [:ref:`string <string>`] (default: ``''``) Command to execute to get the text, will be used only if `text` is empty.
   This command will be executed using the Bash shell.
   Be careful about spaces in file names (i.e. use "$KIBOT_PCB_NAME").
   The `KIBOT_PCB_NAME` environment variable is the PCB file and the
   `KIBOT_SCH_NAME` environment variable is the schematic file.
-  ``expand_kibot_patterns`` :index:`: <pair: preflight - set_text_variables - set_text_variables; expand_kibot_patterns>` [:ref:`boolean <boolean>`] (default: ``true``) Expand %X patterns. The context is `schematic`.
-  ``name`` :index:`: <pair: preflight - set_text_variables - set_text_variables; name>` [:ref:`string <string>`] (default: ``''``) Name of the variable. The `version` variable will be expanded using `${version}`.
-  ``text`` :index:`: <pair: preflight - set_text_variables - set_text_variables; text>` [:ref:`string <string>`] (default: ``''``) Text to insert instead of the variable.
-  *variable* :index:`: <pair: preflight - set_text_variables - set_text_variables; variable>` Alias for name.

