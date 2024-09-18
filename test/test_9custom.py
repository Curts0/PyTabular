"""These are tests I have for pretty janky features of PyTabular.

These were designed selfishly for my own uses.
So seperating out... To one day sunset and remove.
"""

from test.config import testingtablename


def test_backingup_table(model):
    """Tests model.backup_table()."""
    model.backup_table(testingtablename)
    assert (
        len(
            [
                table
                for table in model.Model.Tables.GetEnumerator()
                if f"{testingtablename}_backup" == table.Name
            ]
        )
        == 1
    )


def test_revert_table2(model):
    """Tests model.revert_table()."""
    model.revert_table(testingtablename)
    assert (
        len(
            [
                table
                for table in model.Model.Tables.GetEnumerator()
                if f"{testingtablename}" == table.Name
            ]
        )
        == 1
    )
