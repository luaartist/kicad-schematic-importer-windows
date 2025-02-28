# This file makes the directory a Python package
# It allows the plugin to be imported by KiCad

try:
    from .minimal_plugin import MinimalPlugin
except Exception as e:
    import traceback
    traceback.print_exc()
    raise e
