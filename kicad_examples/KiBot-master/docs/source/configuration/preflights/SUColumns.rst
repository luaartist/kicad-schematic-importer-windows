.. _SUColumns:


SUColumns parameters
~~~~~~~~~~~~~~~~~~~~

-  **separator** :index:`: <pair: preflight - draw_stackup - draw_stackup - columns; separator>` [:ref:`string <string>`] (default: ``' '``) Text used as separator, usually one or more spaces.
-  **type** :index:`: <pair: preflight - draw_stackup - draw_stackup - columns; type>` ''
-  **width** :index:`: <pair: preflight - draw_stackup - draw_stackup - columns; width>` [:ref:`number <number>`] (default: ``10``) Relative width. We first compute the total width and then distribute it according
   to the relative width of each column. The absolute width depends on the area
   assigned for the whole drawing.
-  ``side`` :index:`: <pair: preflight - draw_stackup - draw_stackup - columns; side>` [:ref:`string <string>`] (default: ``'auto'``) (choices: "auto", "right", "left") Side for the dimension used for the *thickness* type.
   When using *auto* the side is detected looking for a *drawing* column.

