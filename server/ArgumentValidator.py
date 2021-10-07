import yaml
import distutils.dir_util as dir_util


class ArgumentValidator:
    def __init__(self, args):
        self._work_dir = args.output
        self._datastore = args.datastore
        self._warning = None
        self._valid = False

        # Output must be valid directory
        if self._work_dir is None or not path.isdir(str(self._work_dir)):
            return

        self.maybe_clone_input(args.input)
        self.decide_datastore()

        self.validate_settings_file()
        self.validate_datastore_file()

        # Make sure we have a file in work_dir, set datastore, check agreement
        # Check datastore and work_dir agree
        with open(self._work_dir) as work_dir_file:
            work_dir = yaml.load(work_dir_file)
            if work_dir.get("datastore") != self._datastore:
                self._warning = (
                    "This working directory is based on a different datastore."
                )

        self._valid = True

    def args_valid(self):
        return self._valid

    def get_args(self):
        return {
            "work_dir": self._work_dir,
            "datastore": self._datastore,
            "warning": self._warning,
        }

    def validate_settings_file(self):
        # TODO Could check schema
        settings_path = path.join(self._work_dir, "pf_settings.json")
        if not path.isfile(settings_path):
            new_settings = {"datastore": self._datastore}
            with open(settings_path) as settings_file:
                yaml.dump(settings_file, new_settings)

    def validate_datastore_file(self):
        datastore_path = path.join(self._datastore, "pf_datastore.yaml")
        if not path.isfile(datastore_path):
            new_datastore = {"files": []}
            with open(datastore_path) as datastore_file:
                yaml.dump(datastore_file, new_datastore)

    def maybe_clone_input(self, input_dir):
        if not path.isdir(str(input_dir)):
            print(f"Ignoring --input {input_dir} because invalid directory")
            return

        input_path = path.join(str(input_dir), "pf_settings.yaml")
        output_path = path.join(str(self.datastore), "pf_settings.yaml")
        if path.isfile(input_path):
            if path.isfile(output_path):
                print(
                    f"Ignoring --input {input_path} because --output {output_path} already exists"
                )
            else:
                dir_util.copy_tree(input_dir, self._work_dir)

    def decide_datastore(self):
        if not path.isdir(str(self._datastore)):
            if self._datastore is not None:
                print(
                    f"Ignoring --datastore {self._datastore} because invalid directory"
                )

            # Try to get datastore from settings in _work_dir
            work_dir_path = path.join(str(self._work_dir), "pf_settings.yaml")
            with open(work_dir_path) as work_dir_file:
                settings = yaml.load(work_dir_file)
            work_dir_datastore = settings.get("datastore")
            if path.isdir(str(work_dir_datastore)):
                self._datastore = work_dir_datastore
                return

            # Use _work_dir as datastore
            self._datastore = self._work_dir
