import subprocess
import click
import psutil
import os


def check_if_process_running(process_name: str):
    for process in psutil.process_iter():
        try:
            if process_name in process.name() or process_name in ' '.join(process.cmdline()):
                return True, process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False, None


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def start():
    click.echo(f'Attempting to start the webscraper.\n')
    if check_if_process_running('mysports_webscraper.py')[0] is False:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        subprocess.Popen(["nohup", "python3", "mysports_webscraper.py"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        click.echo(f'Webscraper successfully started.')
    else:
        click.echo(f'The webscraper is already running.')


@cli.command()
def stop():
    process = check_if_process_running('mysports_webscraper.py')
    click.echo(f'Attempting to stop the webscraper.\n')
    if process[0] is True:
        process[1].terminate()
        process[1].wait()
        click.echo(f'Webscraper successfully stopped.')
    else:
        click.echo(f'The Webscraper is not running.')


@cli.command()
def status():
    if check_if_process_running('mysports_webscraper.py')[0] is True:
        click.echo(f'The webscraper is currently active.\n')

        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        if os.path.exists(f'../log.txt'):
            click.echo(f'The most recent query retrieved the following data:\n')
            with open(f'../log.txt') as log:
                click.echo(log.read())
    else:
        click.echo(f'The webscraper is currently not active.')


if __name__ == '__main__':
    cli()
