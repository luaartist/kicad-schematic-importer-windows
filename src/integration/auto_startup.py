import sys
import logging
from pathlib import Path
from .python_version_manager import KiCadPythonManager
from .plugin_env_manager import PluginEnvironmentManager
from .auto_config import AutoConfig

class AutoStartupManager:
    def __init__(self):
        self.logger = logging.getLogger('AutoStartup')
        self.config = AutoConfig()
        self.python_manager = KiCadPythonManager()
        self.plugin_manager = PluginEnvironmentManager()
        
    def initialize(self):
        """Automatically initialize environment on KiCad startup"""
        if not self.config.config["auto_setup"]:
            return

        try:
            # Setup logging
            if self.config.config["monitoring"]["enable_logging"]:
                self._setup_logging()

            # Check and setup environments for all configured plugins
            for plugin_name, settings in self.config.config["plugins"].items():
                if settings["auto_load"]:
                    self._ensure_plugin_environment(plugin_name, settings)

            # Register startup hooks
            self._register_startup_hooks()

        except Exception as e:
            self.logger.error(f"Startup initialization failed: {e}")

    def _setup_logging(self):
        log_path = Path.home() / ".kicad" / "logs" / "plugin_manager.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            filename=str(log_path),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def _ensure_plugin_environment(self, plugin_name: str, settings: dict):
        """Ensure plugin environment exists and is properly configured"""
        version = settings["preferred_version"]
        if not self.plugin_manager.create_plugin_env(plugin_name, version):
            fallback = self.config.config["python_versions"]["fallback"]
            self.logger.warning(f"Failed to create env with {version}, trying fallback {fallback}")
            self.plugin_manager.create_plugin_env(plugin_name, fallback)

    def _register_startup_hooks(self):
        """Register necessary startup hooks with KiCad"""
        # This will be called when KiCad starts
        import pcbnew
        pcbnew.GetBoard().AddListener(self._on_board_loaded)