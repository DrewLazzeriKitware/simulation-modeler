import click
import yaml
import json

proxies = []
proxy_count = 1


def make_new_proxy(name):
    global proxy_count
    prox = {
        "id": proxy_count,
        "mtime": 1,
        "own": [],
        "name": name,
        "type": name,
        "tags": [],
        "properties": {},
    }
    proxy_count += 1
    return prox

@click.command()
@click.option(
    "-r",
    "--run-file",
    required=True,
    help="A flat map of keys to value from a previous parflow run.",
)
@click.option(
    "-m",
    "--model-file",
    required=True,
    help="A pysimput model whose modeltypes will extract values from the run into proxies.",
)
@click.option(
    "-o",
    "--output",
    default="pf_settings.yaml",
    help="location to write the output to.",
)
def cli(run_file, model_file, output):

    with open(run_file) as run_file_handle:
        run = yaml.safe_load(run_file_handle)
    with open(model_file) as model_file_handle:
        model = yaml.safe_load(model_file_handle)

    # Make one proxy for each modeltype, and fill it with run's values or None
    for (model_type_name, model_type) in model.items():
        new_proxy = make_new_proxy(model_type_name)
        for (prop_name, prop) in model_type.items():
            value = run.get(prop['_parflowId'], None)
            # yaml.safe_load not specific enough (eg parses 1e-4 as string)
            if isinstance(value, str):
                try:
                    value = float(value)
                except:
                    pass
            new_proxy["properties"][prop_name] = value
        proxies.append(new_proxy)

    pf_settings = {"save": json.dumps({"model": model, "proxies": proxies})}

    with open(output, "w") as output_handle:
        yaml.dump(pf_settings, output_handle)


if __name__ == "__main__":
    cli()
