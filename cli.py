# cli_functions.py
import click
from models import Tenant, Property, RentPayment, Base, engine
from sqlalchemy.orm import joinedload, sessionmaker

# Bind the engine to the Base class
Base.metadata.bind = engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@cli.command()
def add_tenant():
    """Add a new tenant."""
    click.echo("\nAdding a New Tenant")

    # Get tenant details from user
    name = click.prompt("Enter tenant name")
    id_number = click.prompt("Enter tenant ID number")
    rent_payable = click.prompt("Enter rent payable by the tenant", type=int)

    # Display available properties for association
    properties = session.query(Property).all()
    click.echo("\nAvailable Properties:")
    for prop in properties:
        click.echo(f"{prop.id}. {prop.address} - Rent Amount: {prop.rent_amount}")

    # Get property choice from the user
    property_id = click.prompt("Enter the ID of the property associated with the tenant", type=int)

    # Check if the chosen property exists
    selected_property = session.query(Property).filter_by(id=property_id).first()
    if selected_property:
        # Create a new tenant and add it to the database
        new_tenant = Tenant(name=name, id_number=id_number, rent_payable=rent_payable, property_id=property_id)
        session.add(new_tenant)
        session.commit()
        click.echo(f"\nTenant {name} added successfully!")
    else:
        click.echo("Invalid property ID. Tenant not added.")

@cli.command()
def add_property():
    """Add a new property."""
    click.echo("\nAdding a New Property")

    # Get property details from user
    address = click.prompt("Enter property address")
    rent_amount = click.prompt("Enter the rent amount for the property", type=int)

    # Create a new property and add it to the database
    new_property = Property(address=address, rent_amount=rent_amount)
    session.add(new_property)
    session.commit()
    click.echo(f"\nProperty at {address} added successfully!")

@cli.command()
def view_properties():
    """View all properties."""
    click.echo("\nViewing Properties")
    
    # Display all properties
    properties = session.query(Property).all()
    if properties:
        click.echo("\nProperties:")
        for prop in properties:
            click.echo(f"ID: {prop.id}, Address: {prop.address}, Rent Amount: {prop.rent_amount}")
    else:
        click.echo("No properties available.")

@cli.command()
def remove_property():
    """Remove a property."""
    click.echo("\nRemoving a Property")

    # Display all properties
    view_properties()

    # Get property ID from user for removal
    property_id = click.prompt("\nEnter the ID of the property to remove", type=int)

    # Check if the property exists
    property_to_remove = session.query(Property).filter_by(id=property_id).first()
    if property_to_remove:
        # Remove the property and commit the changes
        session.delete(property_to_remove)
        session.commit()
        click.echo(f"\nProperty at {property_to_remove.address} removed successfully!")
    else:
        click.echo("Invalid property ID. Property not removed.")

@cli.command()
def record_rent_payment():
    """Record a rent payment."""
    click.echo("\nRecording Rent Payment")

    # Display all tenants with their associated properties
    tenants = session.query(Tenant).options(
        joinedload(Tenant.property)
    ).all()

    if tenants:
        click.echo("\nTenants and Associated Properties:")
        for tenant in tenants:
            click.echo(f"Tenant ID: {tenant.id}, Name: {tenant.name}, Property: {tenant.property.address}")

        # Get tenant ID from user
        tenant_id = click.prompt("\nEnter the ID of the tenant making the payment", type=int)
        selected_tenant = session.query(Tenant).filter_by(id=tenant_id).first()

        if selected_tenant:
            # Get payment details from user
            amount = click.prompt("Enter the payment amount", type=int)
            details = click.prompt("Enter payment details (optional)")

            # Create a new rent payment and add it to the database
            new_payment = RentPayment(amount=amount, details=details, tenant_id=tenant_id)
            session.add(new_payment)
            session.commit()
            click.echo("\nRent payment recorded successfully!")
        else:
            click.echo("Invalid tenant ID. Rent payment not recorded.")
    else:
        click.echo("No tenants available. Add tenants before recording rent payments.")

if __name__ == '__main__':
    cli()
