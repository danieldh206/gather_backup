import tablib
import yaml
import click


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--file_name",
    default="inventory.csv",
    prompt="name of csv file",
    help="file name of csv file containing host.",
)
def main(file_name):
    # open up a csv file with headings of name,hostname,group
    with open(file_name, "r") as fh:
        # create a dataset of the inventory using tablib "pip install tablib"
        imported_data = tablib.Dataset().load(fh)

        inventory = {}
        # loop through the lines of the dataset
        for name, hostname, group in imported_data:
            inventory[name] = {
                "hostname": hostname,
                "group": group,
            }

        # create or open the host.yaml file
        with open("host_2.yaml", "a") as f:
            yaml.dump(
                inventory,
                f,
                sort_keys=False,
                default_flow_style=False,
                explicit_start=True,
            )


if __name__ == "__main__":
    main()
