import click
from .pipeline import run_pipeline


@click.group()
def cli():
    pass


@cli.command()
@click.argument("fastq", type=click.Path(exists=True))
@click.argument("ref", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
def run(fastq, ref, output_dir):
    run_pipeline(fastq, ref, output_dir)


if __name__ == "__main__":
    cli()
