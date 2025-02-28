KiBot (formerly KiPlot)
=======================

.. figure:: https://raw.githubusercontent.com/INTI-CMNB/KiBot/dev/docs/images/kibot_740x400_logo.png
   :alt: KiBot Logo

|Python application| |Coverage Status| |PyPI version| |DOCs status| |Donate|

|doc_id|

**Important for CI/CD**:

- The GitHub actions now use the full/test docker images. So now they include PanDoc and also Blender.
- If you are looking for the GitHub Actions documentation, and you already know how
  to use KiBot, or want a quick start, read: :ref:`usage-of-github-actions`

**New on v1.8.2**

- New **Experimental GUI**
- New preflights: draw_fancy_stackup and include_table
- New global variables: dnp_cross_top_layer and dnp_cross_bottom_layer
- Support for fonts and colors in the worksheet when printing the PCB

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   introduction
   installation
   configuration
   usage
   usage_with_ci_cd

.. toctree::
   :maxdepth: 3
   :caption: Notes and extra information:

   notes_gerber
   notes_position
   notes_3d
   propose
   KiPlotYAML
   Changelog

.. toctree::
   :maxdepth: 2
   :caption: Final notes:

   contributing
   credits

.. toctree::
   :maxdepth: 2
   :caption: Indices and tables:

   genindex


.. |Coverage Status| image:: https://img.shields.io/coveralls/github/INTI-CMNB/KiBot?style=plastic&logo=coveralls
   :target: https://coveralls.io/github/INTI-CMNB/KiBot?branch=master
.. |PyPI version| image:: https://img.shields.io/pypi/v/kibot?style=plastic&logo=pypi
   :target: https://pypi.org/project/kibot/
.. |Donate| image:: https://img.shields.io/badge/Donate-PayPal-green.svg?style=plastic&logo=paypal
   :target: https://www.paypal.com/donate/?hosted_button_id=K2T86GDTTMRPL
.. |DOCs status| image:: https://img.shields.io/readthedocs/kibot?style=plastic&logo=readthedocs
   :target: https://kibot.readthedocs.io/en/latest/
   :alt: Documentation Status
