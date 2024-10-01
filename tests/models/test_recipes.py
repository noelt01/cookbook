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
    assert db_inspector.has_table("recipes")

"""
- [ ] Validate the existence of expected columns in each table, ensuring correct data types.
"""

def test_model_structure_column_data_types(db_inspector):
    table = "recipes"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["title"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["description"]["type"], String)
    assert isinstance(columns["created_at"]["type"], DateTime)
    assert isinstance(columns["updated_at"]["type"], DateTime)
    
# """
# - [ ] Ensure that column foreign keys are correctly defined.
# """

# def test_model_structure_foriegn_key(db_inspector):
#     table = "recipes"
#     foreign_keys = db_inspector.get_foreign_keys(table)
#     product_foreign_key = next(
#         (
#             fk
#             for fk in foreign_keys
#             if set(fk["constrained_columns"]) == {"category_id"}
#             or set(fk["constrained_columns"]) == {"seasonal_id"}
#         ),
#         None,
#     )
#     assert product_foreign_key is not None

"""
- [ ] Verify nullable or not nullable fields
"""

def test_model_structure_nullable_constraints(db_inspector):
    table = "recipes"
    columns = db_inspector.get_columns(table)

    expected_nullable = {
        "id": False,
        "title": False,
        "slug": False,
        "description": True,
        "categories": True,
        "ingredients": True,
        "directions": True,
        "created_at": False,
        "updated_at": False,
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
    table = "recipes"
    constraints = db_inspector.get_check_constraints(table)

    assert any(
        constraint["name"] == "recipe_title_length_check" for constraint in constraints
    )
    assert any(
        constraint["name"] == "recipe_description_length_check" for constraint in constraints
    )
"""
- [ ] Verify the correctness of default values for relevant columns.
"""

# def test_model_structure_default_values(db_inspector):
#     table = "recipes"
#     columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

#     assert columns["is_digital"]["default"] == "false"
#     assert columns["is_active"]["default"] == "false"
#     assert columns["stock_status"]["default"] == "'oos'::status_enum"

"""
- [ ] Ensure that column lengths align with defined requirements.
"""

def test_model_structure_column_lengths(db_inspector):
    table = "recipes"
    columns = {columns["name"]: columns for columns in db_inspector.get_columns(table)}

    assert columns["title"]["type"].length == 80
    assert columns["description"]["type"].length == 200

"""
- [ ]  Validate the enforcement of unique constraints for columns requiring unique values.
"""

def test_model_structure_unique_constraints(db_inspector):
    table = "recipes"
    constraints = db_inspector.get_unique_constraints(table)

    assert any(constraint["name"] == "uq_recipe_title" for constraint in constraints)
    assert any(constraint["name"] == "uq_recipe_slug" for constraint in constraints)
    
