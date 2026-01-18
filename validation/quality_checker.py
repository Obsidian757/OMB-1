#!/usr/bin/env python3
"""
Data Quality Checker for OMB AI Use Case Inventory

Validates CSV data against data dictionary and reports quality metrics.
"""

import csv
import yaml
from pathlib import Path
from typing import Dict, List, Any


class DataQualityChecker:
    """Validates AI use case inventory data quality."""

    def __init__(self, data_dict_path: str = "validation/data_dictionary.yaml"):
        """Initialize checker with data dictionary.

        Args:
            data_dict_path: Path to data dictionary YAML file
        """
        self.data_dict_path = Path(data_dict_path)
        self.required_fields = []
        self.field_constraints = {}
        self._load_data_dictionary()

    def _load_data_dictionary(self):
        """Load and parse data dictionary."""
        with open(self.data_dict_path, 'r') as f:
            data_dict = yaml.safe_load(f)

        # Extract required fields and constraints
        for field in data_dict.get('fields', []):
            field_name = field['name']
            constraints = field.get('constraints', {})

            if constraints.get('required', False):
                self.required_fields.append(field_name)

            self.field_constraints[field_name] = {
                'type': field.get('type', 'string'),
                'enum': constraints.get('enum', []),
                'required': constraints.get('required', False)
            }

    def validate_csv(self, csv_path: str) -> Dict[str, Any]:
        """Validate CSV file and return quality metrics.

        Args:
            csv_path: Path to CSV file to validate

        Returns:
            Dictionary with validation results and quality metrics
        """
        csv_path = Path(csv_path)

        if not csv_path.exists():
            return {
                'error': f'File not found: {csv_path}',
                'valid': False
            }

        total_rows = 0
        missing_value_counts = {field: 0 for field in self.required_fields}
        field_present = set()

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            field_present = set(reader.fieldnames or [])

            for row in reader:
                total_rows += 1

                # Check for missing required values
                for field in self.required_fields:
                    if field in row and (not row[field] or row[field].strip() == ''):
                        missing_value_counts[field] += 1

        # Calculate quality metrics
        missing_required_fields = [
            field for field in self.required_fields
            if field not in field_present
        ]

        total_missing_values = sum(missing_value_counts.values())
        completeness_score = 0.0
        if total_rows > 0 and self.required_fields:
            total_required_cells = total_rows * len(self.required_fields)
            completeness_score = ((total_required_cells - total_missing_values) /
                                 total_required_cells * 100)

        return {
            'valid': len(missing_required_fields) == 0,
            'total_rows': total_rows,
            'total_required_fields': len(self.required_fields),
            'missing_required_fields': missing_required_fields,
            'missing_value_counts': {
                k: v for k, v in missing_value_counts.items() if v > 0
            },
            'total_missing_values': total_missing_values,
            'completeness_score': round(completeness_score, 2),
            'fields_present': len(field_present)
        }


def main():
    """Run quality checker on consolidated inventory."""
    checker = DataQualityChecker()

    # Check 2024 inventory
    csv_path = "data/2024_consolidated_ai_inventory_raw.csv"
    print(f"Validating {csv_path}...\n")

    results = checker.validate_csv(csv_path)

    if not results.get('valid'):
        print(f"❌ Validation failed: {results.get('error', 'Unknown error')}")
        return

    print("✓ CSV Structure Valid")
    print(f"\nQuality Metrics:")
    print(f"  Total rows: {results['total_rows']}")
    print(f"  Required fields: {results['total_required_fields']}")
    print(f"  Fields present: {results['fields_present']}")
    print(f"  Completeness score: {results['completeness_score']}%")

    if results['missing_value_counts']:
        print(f"\n⚠️  Missing values detected in required fields:")
        for field, count in sorted(results['missing_value_counts'].items(),
                                   key=lambda x: x[1], reverse=True)[:5]:
            print(f"    {field}: {count} missing")
    else:
        print(f"\n✓ No missing values in required fields")


if __name__ == "__main__":
    main()
