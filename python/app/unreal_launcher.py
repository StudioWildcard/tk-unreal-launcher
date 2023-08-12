"""
unreal_launcher v0.4
Runs Unreal Editor 5 (UE5) with the Shotgrid (SG) environment

You can run it using the SG toolkit manager which uses bootstrapping (recommended)
In this case, SG toolkit manager will download all needed engines.
The tool will set/modify env variables needed to run UE5 with the SG menu whether you are in a UE5 environment or not.

Alternatively, you can run the tool without the SG toolkit manager (not recommended).
The tool will add extra env variabl Before running the tool in this mode, please make sure
to run Unreal from Shotgrid desktop at least once to download necessary engines.


Running command:
"C:\Program Files\Shotgun\Python3\python.exe" "unreal_launcher_v0.4.py"
"""


import subprocess
import os
import sys
from pathlib import Path

# Make sure to use the correct tk-core version
sys.path.append("C:/Program Files/Shotgun/Resources/Desktop/Python/bundle_cache/app_store/tk-core/v0.20.14/python")
#sys.path.append("C:/Program Files/Shotgun/Resources/Desktop/Python/bundle_cache/app_store/tk-core/v0.20.11/python")

import sgtk

class UnrealLauncher():
    def __init__(self, launch_dict):
        # ARK project ID: 254 GPL Test project ID: "155",  ARK 2 project ID: "188"
        self.project_id = launch_dict.get("sg_project_id", "254")
        # sg-ai config ID: "727" - ARK2 - Beta config ID: "529" - ARK2 - Primary config ID: "298"
        #self.config_id = "496"
        #self.config_name = "alaa ark1"
        self.tk_unreal_version = "v1.2.0"
        self.unrealqt_version = "v1.2.2"

        self.engine_location = launch_dict.get("unreal_engine_location")
        self.unreal_project_path = launch_dict.get("unreal_project_path")
        self.unreal_command = '"{}" "{}" -skipcompile'.format(self.engine_location, self.unreal_project_path)
        # self.unreal_command = f'"{self.unreal_root}/Engine/Binaries/Win64/UnrealEditor.exe" "{self.unreal_root}/Projects/PrimalArk/PrimalArk.uproject" -skipcompile'

        # Current Unreal project path
        self.current_unreal_project = launch_dict.get("unreal_project")

        self.app_data = os.getenv('APPDATA')
        self.bundle_cache = "{}/Shotgun/bundle_cache".format(self.app_data)
        self.bundle_cache_fall_back = "C:/Program Files/Shotgun/Resources/Desktop/Python/bundle_cache"
        self.virtual_env = "{}/github/ue4plugins/tk-framework-unrealqt/{}/python/vendors/py3/windows".format(self.bundle_cache, self.unrealqt_version)
        self.unrealqt_scripts = "{}/Scripts".format(self.virtual_env)
        self.cfg = os.environ.get("TANK_CURRENT_PC")
        #if not self.cfg:
        #    # CFG value
        #    # Find this value if needed
        #    self.basic_desktop = "p188c529"
        #    self.cfg = "{}/Shotgun/ark/{}.basic.desktop/cfg".format(self.app_data, self.basic_desktop)
        self.site_packages = "C:/Program Files/Shotgun/Python3/lib/site-packages"
        self.ssl_cert = "{}/certifi/cacert.pem".format(self.site_packages)
        self.ue_pythonpath = "{}/install/core/python".format(self.cfg)
        self.startup_folder = "{}/Microsoft/Windows/Start Menu/Programs/Startup".format(self.app_data)
        self.tk_unreal = "{}/github/ue4plugins/tk-unreal/{}".format(self.bundle_cache, self.tk_unreal_version)
        self.sep = ";"
        self.sg_pyside2 = "{}/PySide2".format(self.site_packages)
        self.pywin = "{}/pywin32_system32".format(self.site_packages)
        self.ark_pyside2 = "{}/Content/Python/PySide2".format(self.current_unreal_project)
        self.cfg_python = "{}/install/core/python".format(self.cfg)
        self.sg_bootstrap = "{}/plugins/basic/bootstrap.py".format(self.tk_unreal)
        self.unreal_path = "{}/startup".format(self.tk_unreal)
        self.fallback = "C:/Program Files/Shotgun/Resources/Desktop/Python/bundle_cache"

    def set_sg_env(self):
        """
        Setting/modifying env variables needed to run UE5 with SG menu
        """
        print("Setting/modifying env variables needed to run UE5 with SG menu ...")
        os.environ["UNREAL_PATH"] = self.unreal_path
        os.environ["SHOTGUN_ENGINE"] = "tk-unreal"
        os.environ["UE_SHOTGUN_BOOTSTRAP"] = self.sg_bootstrap
        os.environ["UE_SHOTGRID_BOOTSTRAP"] = self.sg_bootstrap
        os.environ["UE_PYTHONPATH"] = os.environ.get("PYTHONPATH") or ""


        os.environ["SHOTGUN_BUNDLE_CACHE_FALLBACK_PATHS"] = self.bundle_cache_fall_back
        os.environ["SHOTGUN_DESKTOP_CURRENT_USER"] = "(dp0"
        os.environ["SHOTGUN_SITE"] = "https://ark.shotgunstudio.com"
        os.environ["SHOTGUN_ENTITY_ID"] = str(self.project_id)
        os.environ["SHOTGUN_ENTITY_TYPE"] = "Project"
        # ------
        # os.environ["SHOTGUN_PIPELINE_CONFIGURATION_ID"] = self.config_id
        # -------

        os.environ["SHOTGUN_SITE"] = "https://ark.shotgunstudio.com"#os.environ["PYTHONPATH"] = self.cfg_python

        os.environ["QT_D3DCREATE_MULTITHREADED"] = "1"
        os.environ["UNREAL_PATH"] = self.unreal_path
        os.environ["UE_SHOTGUN_ENABLED"] = "True"

    def set_extra_env_var(self):
        """
        Env variables that are needed if Shotgrid bootstaping is not run
        """
        os.environ["PATH"] = "{}{}{}".format(self.sg_pyside2, self.sep, os.environ.get("PATH"))
        os.environ["PATH"] = "{}{}{}".format(self.pywin, self.sep, os.environ.get("PATH"))
        os.environ["PATH"] = "{}{}{}".format(self.sg_pyside2, self.sep, os.environ.get("PATH"))
        os.environ["PATH"] = "{}{}{}".format(self.ark_pyside2, self.sep, os.environ.get("PATH"))
        os.environ["PATH"] = "{}{}{}".format(self.unrealqt_scripts, self.sep, os.environ.get("PATH"))
        os.environ["SSL_CERT_FILE"] = self.ssl_cert
        os.environ["TANK_CURRENT_PC"] = self.cfg
        os.environ["VIRTUAL_ENV"] = self.virtual_env

    def run_unreal(self):
        """
        launch UE5 with SG menu
        """
        print("Attempting to launch UE5 with SG menu ...")
        cmd = self.unreal_command
        pipe = subprocess.Popen(cmd, shell=True,
                                stdin=None, stdout=None, stderr=None)
        # Don't wait to see if it launches, it's in its own process now

        print("\n Unreal Editor 5 launched!")

    def sg_toolkit_manager(self):

        import sgtk
        sa = sgtk.authentication.ShotgunAuthenticator()

        # get pre cached user credentials
        user = sa.get_user()
        sgtk.set_authenticated_user(user)

        project = {"type": "Project", "id": self.project_id}

        mgr = sgtk.bootstrap.ToolkitManager(sg_user=user)
        mgr.plugin_id = "basic."
        # The bootstrap process will automatically pick a config if you don't specify one
        #mgr.pipeline_configuration = self.config_name
        #mgr.base_configuration = "sgtk:descriptor:git_branch?branch=beta-ai&path=https://gitlab.com/nexodus/consulting/swc/tk-config-swc.git&version=c6e1a36"

        # The following will fail if running outside the UE5 env as it will not have access to
        # the "unreal" Python API module
        # However, several needed env variables are already set
        # And we will set the remaining env variables in the next step
        try:
            engine = mgr.bootstrap_engine("tk-unreal", entity=project)
        except:
            print("Failed to bootstrap tk-unreal engine, UE5 environment is needed to access Unreal Python API module ")
            pass

    def env_run(self):
        """
        Run WITHOUT using the SG toolkit manager that uses bootstrapping
        """
        self.set_extra_env_var()
        self.set_sg_env()
        self.run_unreal()

    def sg_api_run(self):
        """
        Run using the SG toolkit manager that uses bootstrapping
        """
        # We don't need to bootstrap if we are already in SG environment
        # self.sg_toolkit_manager()
        # We must set missing env variables whether we are in UE5 environment or not
        self.set_sg_env()
        # Run UE5
        self.run_unreal()


if __name__ == '__main__':

    launcher = UnrealLauncher()

    # Run WITHOUT using the SG toolkit
    launcher.env_run()

    # Run using the SG toolkit manager
    #launcher.sg_api_run()
