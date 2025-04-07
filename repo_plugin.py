import os
from description_harvester.plugins import Plugin

class MyPlugin(Plugin):
    plugin_name = "custom_repo"

    def __init__(self):
        print (f"Setup {self.plugin_name} plugin customizing repository names.")
        # Set up any prerequisites or checks here
        
        self.ndpa_list = []
        if os.name == 'nt':
            ndpa_path = r'\\Lincoln\Library\SPE_Processing\ndpaList.txt'
        else:
            ndpa_path = '/media/Library/SPE_Processing/ndpaList.txt'
        if os.path.isfile(ndpa_path):
            with open(ndpa_path, "r") as ndpa_file:
                self.ndpa_list = {line.strip() for line in ndpa_file}

    def custom_repository(self, resource):
        from description_harvester.configurator import Config
        
        #print (f"\tCustomizing repository using {resource['id_0']}")
        
        # custom logic for repository name here and return a string
        id_0 = resource.get('id_0', '').lower()
        if id_0.startswith("apap"):
            if id_0 in self.ndpa_list:
                   repo_name = Config.read_repositories("ndpa")
            else:
                repo_name = Config.read_repositories("apap")
        else:
            for prefix in ["ger", "mss", "ua"]:
                if id_0.startswith(prefix):
                    repo_name = Config.read_repositories(prefix)
                    break
        #print (f"\tSetting repository as {repo_name}.")
        
        return repo_name

