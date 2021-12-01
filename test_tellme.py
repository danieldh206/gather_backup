"""
This is the cli.py file.
"""
import sys
import click
import logging
import traceback


# Click automatically adds a --help option to each command; this annotation
# adds -h as an alias. It's polite!
@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option('-d', '--device', type=str, required=False,
              help="The name or IP address of the device to which to issue commands.")
@click.option('-l', '--list', type=str, required=False,
              help="The path to a file containing a list of devices to which to issue commands. When connecting to devices already found in the database, each line should contain the name or IP or the device. When connecting to devices that aren't found in the database, each line should be a comma separated list of IP, device make, and device model. A file can contain list devices both found and not found in the database. This option is ignored if --device option is used.")
@click.option('-c', '--command', type=str, required=False,
              help="A single line command to execute on the device. The command MUST be quoted or it will likely not do what you expect. Only commands that begin with show or the checksum, compare, list, and show subcommands of file are supported, the Cisco variants dir and verify and APC radius. This option is ignored if the --show-devices flag is used or --file is used.")
@click.option('--device-make', 'device_make', type=str, required=False,
              help="Used with --device-ip and --device-model to specify a target device not in the device database. This option is ignored if the --device or --list options are used.")
@click.option('--device-model', 'device_model', type=str, required=False,
              help="Used with --device-make and --device-ip to specify a target device not in the device database. This option is ignored if the --device or --list options are used.")
@click.option('--device-ip', 'device_ip', type=str, required=False,
              help="Used with --device-make and --device-model to specify a target device not in the device database. This option is ignored if the --device or --list options are used.")
@click.option('-f', '--file', 'command_list_path', type=str, required=False,
              help="A file containing a list of commands to execute, one command per line. You must use either this argument or --command. Use this argument with caution! Be sure to test your script carefully before deploying to multiple devices. This argument overrides --command.")
@click.option('--make', type=str, required=False,
              help="Issue commands to all devices of a given make such as cisco or juniper. This may be combined with --model. This option is ignored if the --device or --list options are used.")
@click.option('--model', type=str, required=False,
              help="Issue commands to all devices of a given model such as swjunex2200. This may be combined with --make. This option is ignored if the --device or --list options are used.")
@click.option('--regex', type=str, required=False,
              help="Issue commands to all devices with name matching standard regular expressions. For example: acar.* or ^uw.*. This option is ignored if the --device or --list or --device-[make,model,ip] options are used. Double uotes MUST be used when the regex includes a shell expansion such as *.")
@click.option('--show-devices', 'show_devices', is_flag=True, required=False,
              help="Show a list of the devices that matches the given options but do not attempt to actually connect to them.")
@click.option('--timeout', type=int, default=30,
              help="Some commands can take a really long time to complete, use this flag to extend the default timeout value. By default, the timeout is 30 seconds.")
@click.argument('arg_device', type=str, required=False)
@click.argument('arg_command', type=str, required=False)
# All CLI programs should support an -e/--environment option to allow querying/
# updating deployment stages other than production. The click.Choice option type
# handles validation of the argument for you.
@click.option('--test',
              type=click.Choice(['development', 'testing', 'production']),
              default='production',
              help="If this option is set to testing then all queries to the database will be done against the test database.")
@click.option('-v', '--verbose', is_flag=True,
              help="send verbose output to the console")
def main(arg_device, arg_command, device, list, command, device_make, device_model, device_ip, command_list_path, make, model, regex, show_devices, timeout, test, verbose):
    """
\b
Name:
    tellme - issue informational command to network devices

\b
Usage:
        tellme --help
        tellme --device=<device_name|ip_address> [--file=/path/to/file|--command="command"]
        tellme --device-ip=<ip_address> --device-make=<make> --device-model=<model> [--file=/path/to/file|--command="command"]
        tellme --list=foo.txt --show-devices\n

\b
Description:
    Issue a single information command or a script of commands to one or
    more network devices and output the result to the screen. This tool is
    limited to commands that beginning with "show" and read-only subcommands
    of "file".

\b
    Access to run this tool is restriced to members of the unix group
    "netops". If you need access your manager can request it from Managed
    Server at help@uw.edu.
    """
    # configure logging
    logging.captureWarnings(True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler(stream=sys.stdout)
    log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s - %(message)s"))
    logger.addHandler(log_handler)

    # change the level and output format if we're going to be verbose
    if verbose:
        logger.setLevel(logging.DEBUG)
        log_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] - %(message)s"))

    # start the main program
    try:
    
        from tellme import TellmeTool
        x = TellmeTool(verbose=verbose, environment=test)
        x.run(arg_device=arg_device, arg_command=arg_command, device_name=device, device_make=device_make, device_model=device_model, device_ip=device_ip, device_list_path=list, select_device_make=make, select_device_model=model, select_device_regex=regex, show_devices=show_devices, command=command, command_list_path=command_list_path, timeout=timeout)
        return 0
    except Exception as e:
        logger.error(str(e))
        logger.debug(traceback.format_exc())
        return 1


# Setting prog_name explicitly here is a workaround to ensure the usage
# looks nice despite our local command-wrapper scripts; if we deployed tools
# using Python installation, it'd be taken care of more automatically.
if __name__ == "__main__":
    sys.exit(main(prog_name="tellme"))