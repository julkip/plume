import click
import toml

FILE_PATH = "plume.toml"


def load_plugins():
    try:
        data = toml.load(FILE_PATH)
        return data.get("plugins", [])
    except FileNotFoundError:
        return []


def save_urls(plugins):
    with open(FILE_PATH, "w") as file:
        toml.dump({"plugins": list(plugins)}, file)


url_store = load_plugins()


@click.group()
def plume():
    pass


@click.command()
@click.argument("url", type=click.STRING)
@click.option(
    "-n",
    "--name",
    type=click.STRING,
    required=False,
    help="Optional. Name des Plugins.",
)
@click.option(
    "-c",
    "--commit",
    type=click.STRING,
    required=False,
    help="Optional. Commit/Tag/Branch des Plugins.",
)
# TODO:
# - [ ] Den Namen als letzten Part der URL extrahieren und separat abspeichern
# - [ ] Optionaler Parameter für den checkout (branch, tag, commit…)
def add(url, name, commit):
    for entry in url_store:
        if entry["url"] == url:
            click.echo(f"Das Plugin {url} ist bereits vorhanden.")
            return
    url_store.append({"url": url, "name": name, "commit": commit})
    save_urls(url_store)
    click.echo(f"Das Plugin {url} wurde hinzugefügt.")


@click.command()
@click.argument("url", type=click.STRING)
# TODO: Nach Namen oder nach URL suchen um zu löschen
def remove(url):
    for plugin in url_store:
        if plugin["url"] == url:
            url_store.remove(plugin)
        save_urls(url_store)
        click.echo(f"Das Plugin {url} wurde entfernt.")
        return
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


# TODO:
# [ ] neues Kommando sync zum installierten der Plugins
# [ ] neues Kommando update zum aktualisieren der Plugins
# [ ] neues Kommando freeze mit optionalen parametern name und commit zum nachträglichen
#     Festsetzen
# [ ] Konfiguration aus plume.toml einlesen
# [ ] Standardkonfiguration erzeugen, wenn plume.toml nicht vorhanden ist


if __name__ == "__main__":
    plume.add_command(add)
    plume.add_command(remove)
    plume.add_command(show)
    plume()
