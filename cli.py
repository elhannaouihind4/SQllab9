import click
from db import get_conn

@click.group()
def cli():
    pass

@cli.command()
@click.argument("titre")
def add_course(titre):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO COURS (titre, credits) VALUES (%s, %s)", (titre, 3))
    conn.commit()
    click.echo(f"Cours '{titre}' ajouté.")
    conn.close()

# Ajoutez des commandes pour lister, modifier, supprimer

if __name__ == "__main__":
    cli()
