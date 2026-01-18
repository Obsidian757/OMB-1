#!/usr/bin/env python3
"""
Data Quality Checker for OMB AI Use Case Inventory

Validates CSV data against data dictionary and reports quality metrics.
"""

import csv
import yaml
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


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
        agency_counts = {}
        rights_impacting_count = 0

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            field_present = set(reader.fieldnames or [])

            for row in reader:
                total_rows += 1

                # Check for missing required values
                for field in self.required_fields:
                    if field in row and (not row[field] or row[field].strip() == ''):
                        missing_value_counts[field] += 1

                # Track agency statistics
                agency = row.get('3_agency', 'Unknown').strip()
                if agency:
                    agency_counts[agency] = agency_counts.get(agency, 0) + 1

                # Track rights-impacting use cases
                impact_type = row.get('17_impact_type', '').strip()
                if 'Rights-Impacting' in impact_type or 'Safety-Impacting' in impact_type:
                    rights_impacting_count += 1

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
            'fields_present': len(field_present),
            'statistics': {
                'total_agencies': len(agency_counts),
                'total_use_cases': total_rows,
                'rights_impacting_count': rights_impacting_count,
                'agency_counts': dict(sorted(agency_counts.items(),
                                           key=lambda x: x[1], reverse=True))
            }
        }

    def generate_markdown_report(self, results: Dict[str, Any],
                                 output_path: str = "validation/QUALITY_REPORT.md"):
        """Generate markdown quality report.

        Args:
            results: Validation results from validate_csv()
            output_path: Path to output markdown file
        """
        output_path = Path(output_path)

        # Calculate quality grade
        score = results.get('completeness_score', 0)
        if score >= 95:
            grade = "A (Excellent)"
        elif score >= 90:
            grade = "B (Good)"
        elif score >= 80:
            grade = "C (Fair)"
        else:
            grade = "D (Needs Improvement)"

        stats = results.get('statistics', {})

        # Generate report
        report = f"""# Data Quality Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Quality Score: {score}% - Grade {grade}

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Agencies | {stats.get('total_agencies', 0)} |
| Total Use Cases | {stats.get('total_use_cases', 0)} |
| Rights/Safety-Impacting | {stats.get('rights_impacting_count', 0)} |
| Required Fields | {results.get('total_required_fields', 0)} |
| Fields Present | {results.get('fields_present', 0)} |

---

## Data Completeness

**Completeness Score:** {score}%

- Total missing values in required fields: {results.get('total_missing_values', 0)}
- Total rows validated: {results.get('total_rows', 0)}

"""

        # Add missing value details if any
        if results.get('missing_value_counts'):
            report += "### Missing Values by Field\n\n"
            report += "| Field | Missing Count | % of Total |\n"
            report += "|-------|--------------|------------|\n"

            total_rows = results.get('total_rows', 1)
            for field, count in sorted(results['missing_value_counts'].items(),
                                      key=lambda x: x[1], reverse=True):
                pct = (count / total_rows * 100) if total_rows > 0 else 0
                report += f"| `{field}` | {count} | {pct:.1f}% |\n"

            report += "\n"

        # Add top agencies
        agency_counts = stats.get('agency_counts', {})
        if agency_counts:
            report += "---\n\n## Top 10 Agencies by Use Cases\n\n"
            report += "| Rank | Agency | Use Cases |\n"
            report += "|------|--------|----------|\n"

            for i, (agency, count) in enumerate(list(agency_counts.items())[:10], 1):
                report += f"| {i} | {agency} | {count} |\n"

            report += "\n"

        # Add recommendations
        report += "---\n\n## Recommendations\n\n"

        if score >= 95:
            report += "✓ Data quality is excellent. Continue monitoring for missing values.\n\n"
        elif score >= 90:
            report += "⚠️ Data quality is good but could be improved:\n\n"
        else:
            report += "⚠️ Data quality needs improvement:\n\n"

        if results.get('missing_value_counts'):
            report += "**Action Items:**\n\n"
            for field, count in list(results['missing_value_counts'].items())[:3]:
                report += f"- Investigate and populate missing values in `{field}` ({count} rows)\n"

        report += "\n---\n\n"
        report += "*Report generated by OMB-1 Data Quality Checker*\n"

        # Write report
        with open(output_path, 'w') as f:
            f.write(report)

        return str(output_path)


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

    # Display statistics
    stats = results.get('statistics', {})
    print(f"\nSummary Statistics:")
    print(f"  Total agencies: {stats.get('total_agencies', 0)}")
    print(f"  Total use cases: {stats.get('total_use_cases', 0)}")
    print(f"  Rights/Safety-impacting: {stats.get('rights_impacting_count', 0)}")

    print(f"\nTop 5 Agencies by Use Cases:")
    agency_counts = stats.get('agency_counts', {})
    for i, (agency, count) in enumerate(list(agency_counts.items())[:5], 1):
        print(f"  {i}. {agency}: {count}")

    # Generate markdown report
    print(f"\nGenerating quality report...")
    report_path = checker.generate_markdown_report(results)
    print(f"✓ Report saved to: {report_path}")


if __name__ == "__main__":
    main()
