import click 
from .qc import count_read, filter_read_by_gc

@click.group()
def cli():
    pass

@cli.command()
@click.argument("path")
def count(path):
    result = count_read(path)
    click.echo(f"Read Count: {result}")

@cli.command()
@click.argument("path")
@click.option("--min-gc", type = float, default = 0.3, help = "Minimum GC ratio")
@click.option("--max-gc", type = float, default = 0.7, help = "Maximum GC ratio")
def filter_gc(path, min_gc, max_gc):
    result = filter_read_by_gc(path, min_gc, max_gc)
    click.echo(f"Reads passing filter: {result}")


if __name__ == "__main__":
    cli()
