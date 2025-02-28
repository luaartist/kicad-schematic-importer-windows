.. index::
   single: preprocessing
   single: definitions
   pair: configuration; substitution

.. _yaml-substitution:

Doing YAML substitution or preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you could want to change values in the YAML depending on
external stuff, or just want to be able to change something for each
variant run.

In this case you can use external tools to create various YAML files
using a template, but you can also use KiBot’s definitions.

The definitions allows you to replace tags like ``@VARIABLE@`` by some
specified value. These definitions can be specified at the command line
using the ``-E`` option. As an example: ``-E UNITS=millimeters`` will
replace all ``@UNITS@`` markers by ``millimeters``. This is applied to
all YAML files loaded, so this propagates to all the imported YAML
files.

You can use ``-E`` as many times as you need.

Also note that the ``--def-from-env`` option adds all the environment
variables as definitions.

.. index::
   pair: definitions; default

Default definitions
^^^^^^^^^^^^^^^^^^^

A configuration file using the ``@VARIABLE@`` tags won’t be usable
unless you provide proper values for **all** de used variables. When
using various tags this could be annoying. KiBot supports defining
default values for the tags. Here is an example:

.. code:: yaml

   kibot:
     version: 1

   outputs:
     - name: 'gerbers_@ID@'
       comment: "Gerbers with definitions"
       type: gerber
       output_id: '_@ID@'
       layers: '@LAYERS@'
   ...
   definitions:
     ID: def_id
     LAYERS: F.Cu

Note that from the YAML point this is two documents in the same file.
The second document is used to provide default values for the
definitions. As defaults they have the lowest precedence.


.. index::
   pair: definitions; during import

.. _definitions-during-import:

Definitions during import
^^^^^^^^^^^^^^^^^^^^^^^^^

When importing a configuration you can specify values for the
``@VARIABLE@`` tags. This enables the creation of parametrizable
imports. Using the example depicted in `Default
definitions <#default-definitions>`__ saved to a file named
*simple.kibot.yaml* you can use:

.. code:: yaml

   kibot:
     version: 1

   import:
     - file: simple.kibot.yaml
       definitions:
         ID: external_copper
         LAYERS: "[F.Cu, B.Cu]"

This will import *simple.kibot.yaml* and use these particular values.
Note that they have more precedence than the definitions found in
*simple.kibot.yaml*, but less precedence than any value passed from the
command line.


.. index::
   pair: definitions; recursive expansion

Recursive definitions expansion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When KiBot expands the ``@VARIABLE@`` tags it first applies all the
replacements defined in the command line, and then all the values
collected from the ``definitions``. After doing a round of replacements
KiBot tries to do another. This process is repeated until nothing is
replaced or we reach 20 iterations. So you can define a tag that
contains another tag.

As an example, if the configuration shown in `Definitions during
import <#definitions-during-import>`__ is stored in a file named
*top.kibot.yaml* you could use:

.. code:: shell

   kibot -v -c top.kibot.yaml -E ID=@LAYERS@

This will generate gerbers for the front/top and bottom layers using
*[F.Cu, B.Cu]* as output id. So you’ll get *light_control-B_Cu_[F.Cu,
B.Cu].gbr* and *light_control-F_Cu_[F.Cu, B.Cu].gbr*.
