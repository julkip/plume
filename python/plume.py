import click
import toml


FILE_PATH = "plume.toml"


def load_plugins():
    try:
        data = toml.load(FILE_PATH)
        return set(data.get('plugins', []))
    except FileNotFoundError:
        return set()


def save_urls(plugins):
    with open(FILE_PATH, 'w') as file:
        toml.dump({'plugins': list(plugins)}, file)


url_store = load_plugins()


@click.group()
def plume():
    pass


@click.command()
@click.argument("url", type=click.STRING)
# TODO:
# - [ ] Den Namen als letzten Part der URL extrahieren und separat abspeichern
# - [ ] Optionaler Parameter für den checkout (branch, tag, commit…)
def add(url):
    if url in url_store:
        click.echo(f"Das Plugin {url} ist bereits vorhanden.")
    else:
        url_store.add(url)
        save_urls(url_store)
        click.echo(f"Das Plugin {url} wurde hinzugefügt.")


@click.command()
@click.argument("url", type=click.STRING)
# TODO: Nach Namen oder nach URL suchen um zu löschen
def remove(url):
    if url in url_store:
        url_store.remove(url)
        save_urls(url_store)
        click.echo(f"Das Plugin {url} wurde entfernt.")
    else:
        click.echo(f"Das Plugin {url} ist nicht vorhanden.")


@click.command()
def show():
    if url_store:
        click.echo("Installierte Plugins:")
        for url in url_store:
            click.echo(f"- {url}")
    else:
        click.echo("Es sind keine Plugins installiert.")

# TODO: neues Kommando sync zum Aktualisieren der installierten Plugins


if __name__ == "__main__":
    plume.add_command(add)
    plume.add_command(remove)
    plume.add_command(show)
    plume()
