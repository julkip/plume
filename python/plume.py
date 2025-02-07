import os

import click
import git
import toml

FILE_PATH = "plume.toml"
PLUGIN_PATH = (
    "/home/julkip/.local/share/nvim/plume-plugins"  # TODO: XDG_DATA_HOME benutzen
)


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


def _get_name(url, name):
    if name:
        return name
    localname = url.split("/")[-1].removesuffix(".git")
    return localname


def _update_url_store(update_url, url, name, commit):
    if update_url:
        for entry in url_store:
            if entry["url"] == url:
                entry.update({"url": url, "name": name, "commit": commit})
    else:
        url_store.append({"url": url, "name": name, "commit": commit})


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
    default="HEAD",
    type=click.STRING,
    required=False,
    help="Optional. Commit/Tag/Branch des Plugins.",
)
# TODO:
# - [x] Den Namen als letzten Part der URL extrahieren und separat abspeichern
# - [x] Optionaler Parameter für den checkout (branch, tag, commit…)
# - [x] Plugin updaten, wenn sich der Name oder der commit ändert
def add(url, name="", commit="HEAD"):
    localname = _get_name(url, name)
    update_url = False
    for entry in url_store:
        if entry["url"] == url:
            if (
                (entry["name"] == localname and name == "")
                or (entry["name"] == name and name != "")
                and entry["commit"] == commit
            ):
                click.echo(f"Das Plugin {url} ist bereits vorhanden.")
                return
            else:
                update_url = True
    if commit == "HEAD":  # Get commit for current HEAD
        repo = git.cmd.Git()
        commit = repo.ls_remote(url).splitlines()[0][:7]
    _update_url_store(update_url, url, localname, commit)
    save_urls(url_store)
    click.echo(f"Das Plugin {url} wurde hinzugefügt.")


@click.command()
@click.argument("plugin", type=click.STRING)
# TODO: Nach Namen oder nach URL suchen um zu löschen
def remove(plugin):
    for plugin in url_store:
        if plugin["url"] == plugin:
            url_store.remove(plugin)
        save_urls(url_store)
        click.echo(f"Das Plugin {plugin} wurde entfernt.")
        return
    else:
        click.echo(f"Das Plugin {plugin} ist nicht vorhanden.")


@click.command()
def show():
    if url_store:
        click.echo("Installierte Plugins:")
        for url in url_store:
            click.echo(f"- {url}")
    else:
        click.echo("Es sind keine Plugins installiert.")


@click.command()
def sync():
    for plugin in url_store:
        if not os.path.exists(PLUGIN_PATH + "/" + plugin["name"]):
            click.echo(f"Plugin {plugin} wird installiert")
            repo = git.Repo.clone_from(plugin["url"], f"{PLUGIN_PATH}/{plugin["name"]}")
            repo.commit(plugin["commit"])


@click.command()
def update():
    for plugin in url_store:
        if os.path.exists(PLUGIN_PATH + "/" + plugin["name"]):
            click.echo(f"Plugin {plugin} wird aktualisiert")
            repo = git.Repo(PLUGIN_PATH + "/" + plugin["name"])
            o = repo.remotes.origin
            o.pull()
            repo.commit(plugin["commit"])


# TODO:
# [ ] Pluginverzeichnis anlegen, wenn nicht vorhanden
# [-] neues Kommando sync zum installierten der Plugins
# [-] neues Kommando update zum aktualisieren der Plugins
# [ ] neues Kommando clean zum entfernen nicht gelisteter Plugins
# [ ] neues Kommando freeze mit optionalen parametern name und commit zum nachträglichen
#     Festsetzen Sub-TODO: macht das überhaupt sinn? oder brauche ich dann ein freeze
#     flag, damit diese Plugins von Update ignoriert werden?
# [ ] Konfiguration aus plume.toml einlesen
# [ ] Standardkonfiguration erzeugen, wenn plume.toml nicht vorhanden ist


if __name__ == "__main__":
    plume.add_command(add)
    plume.add_command(remove)
    plume.add_command(show)
    plume.add_command(sync)
    plume.add_command(update)
    plume()
