"""Bulk of pytests for `PyMeasure()` class."""


def test_create_measure(model):
    """Test Creating Measure."""
    name = "Test Measure"
    expression = "1 + 4"
    folder = "Testing"
    model.Measures(name, expression, DisplayFolder=folder)
    query = model.query(f"EVALUATE {{[{name}]}}")
    ans = 5
    new_measure = model.Measures[name]._object
    new_measure.Parent.Measures.Remove(new_measure)
    model.save_changes()
    assert query == ans
