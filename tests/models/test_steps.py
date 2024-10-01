import pytest
from sqlalchemy import Integer, String, Boolean, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID



"""
## Table and Column Validation
"""

"""
- [ ] Confirm the presence of all required tables within the database schema.
"""

def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("steps")

"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""

def test_model_structure_column_data_types(db_inspector):
    table = "steps"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["step_number"]["type"], Integer)
    assert isinstance(columns["step"]["type"], String)
    assert isinstance(columns["recipe_id"]["type"], Integer)
    
# """
# - [ ] Ensure that column foreign keys are correctly defined.
# """

def test_model_structure_foriegn_key(db_inspector):
    table = "steps"
    foreign_keys = db_inspector.get_foreign_keys(table)
    product_foreign_key = next(
        (
            fk
            for fk in foreign_keys
            if set(fk["constrained_columns"]) == {"recipe_id"}
        ),
        None,
    )
    assert product_foreign_key is not None

"""
- [ ] Verify nullable or not nullable fields
"""

def test_model_structure_nullable_constraints(db_inspector):
    table = "steps"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "step_number": False,
        "step": False,
        "recipe_id": False,
    }

    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(
            column_name
        ), f"column '{column_name}' is not nullable as expected"

"""
- [ ] Test columns with specific constraints to ensure they are accurately defined.
"""

def test_model_structure_column_constraints(db_inspector):
    table = "steps"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "step_step_length_check" for constraint in constraints
    )

"""
- [ ] Verify the correctness of default values for relevant columns.
"""

# def test_model_structure_default_values(db_inspector):
#     table = "steps"
#     columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

#     assert columns["is_digital"]["default"] == "false"
#     assert columns["is_active"]["default"] == "false"
#     assert columns["stock_status"]["default"] == "'oos'::status_enum"

"""
- [ ] Ensure that column lengths align with defined requirements.
"""

def test_model_structure_column_lengths(db_inspector):
    table = "steps"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["step"]["type"].length == 200

"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""

def test_model_structure_unique_constraints(db_inspector):
    table = "steps"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "uq_step_number_recipe" for constraint in constraints)
    
