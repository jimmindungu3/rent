# cli_functions.py
from models import Tenant, Property, RentPayment
from models.database import session
from sqlalchemy.orm import joinedload

def add_tenant():
    print("\nAdding a New Tenant")

    # Get tenant details from user
    name = input("Enter tenant name: ")
    id_number = input("Enter tenant ID number: ")
    rent_payable = int(input("Enter rent payable by the tenant: "))

    # Display available properties for association
    properties = session.query(Property).all()
    print("\nAvailable Properties:")
    for prop in properties:
        print(f"{prop.id}. {prop.address} - Rent Amount: {prop.rent_amount}")

    # Get property choice from the user
    property_id = int(input("Enter the ID of the property associated with the tenant: "))

    # Check if the chosen property exists
    selected_property = session.query(Property).filter_by(id=property_id).first()
    if selected_property:
        # Create a new tenant and add it to the database
        new_tenant = Tenant(name=name, id_number=id_number, rent_payable=rent_payable, property_id=property_id)
        session.add(new_tenant)
        session.commit()
        print(f"\nTenant {name} added successfully!")
    else:
        print("Invalid property ID. Tenant not added.")

def add_property():
    print("\nAdding a New Property")

    # Get property details from user
    address = input("Enter property address: ")
    rent_amount = int(input("Enter the rent amount for the property: "))

    # Create a new property and add it to the database
    new_property = Property(address=address, rent_amount=rent_amount)
    session.add(new_property)
    session.commit()
    print(f"\nProperty at {address} added successfully!")

def view_properties():
    print("\nViewing Properties")
    
    # Display all properties
    properties = session.query(Property).all()
    if properties:
        print("\nProperties:")
        for prop in properties:
            print(f"ID: {prop.id}, Address: {prop.address}, Rent Amount: {prop.rent_amount}")
    else:
        print("No properties available.")

def remove_property():
    print("\nRemoving a Property")

    # Display all properties
    view_properties()

    # Get property ID from user for removal
    property_id = int(input("\nEnter the ID of the property to remove: "))

    # Check if the property exists
    property_to_remove = session.query(Property).filter_by(id=property_id).first()
    if property_to_remove:
        # Remove the property and commit the changes
        session.delete(property_to_remove)
        session.commit()
        print(f"\nProperty at {property_to_remove.address} removed successfully!")
    else:
        print("Invalid property ID. Property not removed.")


def record_rent_payment():
    print("\nRecording Rent Payment")

    # Display all tenants with their associated properties
    tenants = session.query(Tenant).options(
        joinedload(Tenant.property)
    ).all()

    if tenants:
        print("\nTenants and Associated Properties:")
        for tenant in tenants:
            print(f"Tenant ID: {tenant.id}, Name: {tenant.name}, Property: {tenant.property.address}")

        # Get tenant ID from user
        tenant_id = int(input("\nEnter the ID of the tenant making the payment: "))
        selected_tenant = session.query(Tenant).filter_by(id=tenant_id).first()

        if selected_tenant:
            # Get payment details from user
            amount = int(input("Enter the payment amount: "))
            details = input("Enter payment details (optional): ")

            # Create a new rent payment and add it to the database
            new_payment = RentPayment(amount=amount, details=details, tenant_id=tenant_id)
            session.add(new_payment)
            session.commit()
            print("\nRent payment recorded successfully!")
        else:
            print("Invalid tenant ID. Rent payment not recorded.")
    else:
        print("No tenants available. Add tenants before recording rent payments.")
