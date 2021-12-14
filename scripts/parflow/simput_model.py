import click
import yaml
from pathlib import Path

model = {}


def add_type(node, prop):
    if "domains" not in node:
        return
    if "DoubleValue" in node["domains"]:
        prop["type"] = "float32"
        return
    if "IntValue" in node["domains"]:
        prop["type"] = "int8"
        return
    prop["type"] = "string"


def add_help(node, prop):
    help_text = node.get("help", "").strip("\n").split("] ", 1)
    prop["_help"] = help_text[1] if len(help_text) > 1 else help_text[0]


def add_domains(node, prop):
    domains = node.get("domains")
    if not domains:
        return

    # Check for Range
    for numeric_domain in ["DoubleValue", "IntValue"]:
        if domains.get(numeric_domain):
            min_value = None
            max_value = None
            if "min_value" in domains[numeric_domain]:
                min_value = domains[numeric_domain]["min_value"]
            if "max_value" in domains[numeric_domain]:
                max_value = domains[numeric_domain]["max_value"]
            if min_value is not None or max_value is not None:
                prop["domains"] = [
                    {
                        "type": "Range",
                        "value_range": [min_value, max_value],
                        "level": 1,
                    }
                ]
                return

    # Check for LabelList
    if "EnumDomain" in node["domains"]:
        prop["domains"] = [
            {
                "type": "LabelList",
                "values": [
                    {"text": name, "value": name}
                    for name in node["domains"]["EnumDomain"]["enum_list"]
                ],
            }
        ]
        return


def add_to_model(node, name=None, parents=[], parent_group=None):
    global model

    parents = list(parents)  # Copy

    # Ignore leaves and dynamic keys
    if type(node) is not dict:
        return
    if name and name.startswith(".{"):
        return

    # Decide identifiers for node
    if name and name != "__value__":
        # __value__ uses's parent's name
        parents += [name]
    parflowId = ".".join(parents)  # Unique identifier
    propertyName = parflowId.replace(".", "_")  # Storage identifier

    # Check whether this node starts a group for its children + self
    if node.get("__simput__", {}).get("GroupChildrenAs"):
        parent_group = node.get("__simput__", {}).get("GroupChildrenAs")

    # Set properties
    if node.get("help"):

        # Only add if in parent_group
        if parent_group:
            new_prop = {"_parflowId": parflowId}
            add_help(node, new_prop)
            add_type(node, new_prop)
            add_domains(node, new_prop)

            if not model.get(parent_group):
                model[parent_group] = {}

            model[parent_group].update(
                {
                    propertyName: new_prop,
                }
            )

    # Recurse onto children
    for key in node.keys():
        if key == "__value__" or not key.startswith("__"):
            add_to_model(node.get(key), key, parents, parent_group=parent_group)


@click.command()
@click.option(
    "-o",
    "--output",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
    help="The directory to output the model file to. If no output "
    + "is provided the file will be created in the current directory.",
)
@click.option(
    "-d",
    "--def_directory",
    default=None,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    help="The directory of definition files.",
)
@click.option(
    "-f",
    "--def_file",
    default=None,
    multiple=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="A definition file to use.",
)
@click.option(
    "--include-wells",
    default=False,
    help="Whether to include support for Wells. This is complicated and left out by default.",
)
@click.option(
    "--include-clm",
    default=False,
    help="Whether to include support for CLM. This is complicated and left out by default",
)
def cli(output, def_directory, def_file, include_wells, include_clm):
    """Accepts a single file, list of files, or directory name."""
    global model

    files = (
        Path(def_directory).iterdir() if def_directory else [Path(f) for f in def_file]
    )

    for f in files:
        with open(f) as value:
            data = yaml.load(value, Loader=yaml.Loader)
            add_to_model(data)

    with open(f"{output}/model.yaml", "w", encoding="utf8") as f:
        yaml.dump(model, f)


if __name__ == "__main__":
    cli()
