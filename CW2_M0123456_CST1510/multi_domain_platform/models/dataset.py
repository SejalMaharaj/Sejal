class Dataset:
    def __init__(self, name: str, rows: int, columns: int):
        self.name = name
        self.rows = rows
        self.columns = columns

    def shape_str(self) -> str:
        return f"{self.rows} rows × {self.columns} columns"
