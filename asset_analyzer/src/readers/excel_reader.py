"""Excel file reader with work order sheet detection."""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Union, Optional

class WorkOrderReader:
    """Reads and validates work order data from Excel files."""
    
    def __init__(self, file_path: Union[str, Path]):
        """Initialize reader with Excel file path."""
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
    
    @staticmethod
    def is_work_order_sheet(df: pd.DataFrame) -> bool:
        """Check if a dataframe contains work order data."""
        return 'EVT_CODE' in df.columns
    
    def read_work_order_sheets(self) -> pd.DataFrame:
        """Read and combine all work order sheets from the Excel file."""
        xl = pd.ExcelFile(self.file_path)
        dfs = []
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name)
            if self.is_work_order_sheet(df):
                df['Source_Sheet'] = sheet_name
                dfs.append(df)
        
        if not dfs:
            raise ValueError(f"No work order sheets found in {self.file_path}")
        
        return pd.concat(dfs, ignore_index=True)
    
    def get_sheet_summary(self) -> Dict[str, dict]:
        """Get summary of all sheets in the workbook."""
        xl = pd.ExcelFile(self.file_path)
        summary = {}
        
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name)
            summary[sheet_name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'is_work_order': self.is_work_order_sheet(df)
            }
        
        return summary