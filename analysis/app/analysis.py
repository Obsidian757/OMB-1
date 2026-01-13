"""
Core analysis module for Federal AI Use Case Inventory.
Provides pandas-based analysis functions for the inventory data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List, Any
from functools import lru_cache


# Column mappings based on data dictionary
COLUMNS = {
    "use_case_name": "Use Case Name",
    "agency": "Agency",
    "agency_abbr": "Agency Abbreviation",
    "bureau": "Bureau",
    "topic_area": "Use Case Topic Area",
    "commercial_ai": "Is the AI use case found in the below list of general commercial AI products and services?",
    "purpose_benefits": "What is the intended purpose and expected benefits of the AI?",
    "outputs": "Describe the AI system's outputs.",
    "dev_stage": "Stage of Development",
    "impact_type": "Is the AI use case rights-impacting\n safety-impacting\n both\n or neither?",
    "date_initiated": "Date Initiated",
    "date_implemented": "Date Implemented",
    "dev_method": "Was the AI system involved in this use case developed (or is it to be developed) under contract(s) or in-house?",
    "hisp_support": "Is this AI use case supporting a High-Impact Service Provider (HISP) public-facing service?",
    "contains_pii": "Does this AI use case involve personally identifiable information (PII) that is maintained by the agency?",
    "has_ato": "Do you have access to an enterprise data catalog or agency-wide data repository that enables you to identify whether or not the necessary datasets exist and are ready to develop your use case?",
}


class AIInventoryAnalyzer:
    """Analyzer for Federal AI Use Case Inventory data."""

    def __init__(self, data_dir: str = "/data"):
        self.data_dir = Path(data_dir)
        self._df_2024: Optional[pd.DataFrame] = None
        self._df_2023: Optional[pd.DataFrame] = None

    @property
    def df_2024(self) -> pd.DataFrame:
        """Lazy load 2024 inventory data."""
        if self._df_2024 is None:
            self._df_2024 = self._load_csv("2024_consolidated_ai_inventory_raw_v2.csv")
        return self._df_2024

    @property
    def df_2023(self) -> pd.DataFrame:
        """Lazy load 2023 inventory data."""
        if self._df_2023 is None:
            self._df_2023 = self._load_csv("2023_consolidated_ai_inventory_raw.csv")
        return self._df_2023

    def _load_csv(self, filename: str) -> pd.DataFrame:
        """Load a CSV file from the data directory."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        return pd.read_csv(filepath, encoding="utf-8", low_memory=False)

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get high-level summary statistics."""
        df = self.df_2024

        # Clean impact type column for analysis
        impact_col = self._find_column(df, "impact")

        total_use_cases = len(df)
        unique_agencies = df[self._find_column(df, "Agency")].nunique()

        # Count impact types
        impact_counts = {"rights": 0, "safety": 0, "both": 0, "neither": 0}
        if impact_col:
            impact_series = df[impact_col].fillna("").str.lower()
            impact_counts["rights"] = impact_series.str.contains("rights").sum()
            impact_counts["safety"] = impact_series.str.contains("safety").sum()
            impact_counts["both"] = impact_series.str.contains("both").sum()
            impact_counts["neither"] = impact_series.str.contains("neither").sum()

        return {
            "total_use_cases": total_use_cases,
            "unique_agencies": unique_agencies,
            "rights_impacting": impact_counts["rights"],
            "safety_impacting": impact_counts["safety"],
            "both_impacting": impact_counts["both"],
            "neither_impacting": impact_counts["neither"],
            "high_impact_total": impact_counts["rights"] + impact_counts["safety"] + impact_counts["both"],
        }

    def get_agency_breakdown(self) -> pd.DataFrame:
        """Get use case counts by agency."""
        df = self.df_2024
        agency_col = self._find_column(df, "Agency")

        breakdown = df.groupby(agency_col).size().reset_index(name="use_case_count")
        breakdown = breakdown.sort_values("use_case_count", ascending=False)
        breakdown.columns = ["agency", "use_case_count"]
        return breakdown

    def get_topic_distribution(self) -> pd.DataFrame:
        """Get use case distribution by topic area."""
        df = self.df_2024
        topic_col = self._find_column(df, "Topic")

        if topic_col:
            dist = df[topic_col].value_counts().reset_index()
            dist.columns = ["topic_area", "count"]
            return dist
        return pd.DataFrame(columns=["topic_area", "count"])

    def get_dev_stage_distribution(self) -> pd.DataFrame:
        """Get distribution of development stages."""
        df = self.df_2024
        stage_col = self._find_column(df, "Stage")

        if stage_col:
            dist = df[stage_col].value_counts().reset_index()
            dist.columns = ["stage", "count"]
            return dist
        return pd.DataFrame(columns=["stage", "count"])

    def get_impact_by_agency(self) -> pd.DataFrame:
        """Get rights/safety impacting use cases by agency."""
        df = self.df_2024
        agency_col = self._find_column(df, "Agency")
        impact_col = self._find_column(df, "impact")

        if not impact_col:
            return pd.DataFrame()

        # Filter to impacting use cases
        mask = df[impact_col].fillna("").str.lower().str.contains("rights|safety|both")
        impacting = df[mask]

        breakdown = impacting.groupby(agency_col).size().reset_index(name="impacting_count")
        breakdown = breakdown.sort_values("impacting_count", ascending=False)
        breakdown.columns = ["agency", "impacting_count"]
        return breakdown

    def get_year_comparison(self) -> Dict[str, Any]:
        """Compare 2023 vs 2024 inventory."""
        try:
            count_2023 = len(self.df_2023)
            count_2024 = len(self.df_2024)

            growth = count_2024 - count_2023
            growth_pct = (growth / count_2023 * 100) if count_2023 > 0 else 0

            return {
                "count_2023": count_2023,
                "count_2024": count_2024,
                "growth": growth,
                "growth_percent": round(growth_pct, 1),
            }
        except FileNotFoundError:
            return {
                "count_2023": 0,
                "count_2024": len(self.df_2024),
                "growth": 0,
                "growth_percent": 0,
                "error": "2023 data not available",
            }

    def get_pii_analysis(self) -> Dict[str, Any]:
        """Analyze PII handling across use cases."""
        df = self.df_2024
        pii_col = self._find_column(df, "PII")

        if not pii_col:
            return {"error": "PII column not found"}

        pii_counts = df[pii_col].fillna("Unknown").value_counts().to_dict()
        return {
            "pii_distribution": pii_counts,
            "total_with_pii": pii_counts.get("Yes", 0),
        }

    def search_use_cases(
        self,
        query: str,
        agency: Optional[str] = None,
        topic: Optional[str] = None,
        impact_type: Optional[str] = None,
        limit: int = 50,
    ) -> pd.DataFrame:
        """Search use cases with filters."""
        df = self.df_2024.copy()

        # Text search across name and purpose columns
        if query:
            name_col = self._find_column(df, "Name")
            purpose_col = self._find_column(df, "purpose")

            mask = pd.Series([False] * len(df))
            if name_col:
                mask |= df[name_col].fillna("").str.lower().str.contains(query.lower())
            if purpose_col:
                mask |= df[purpose_col].fillna("").str.lower().str.contains(query.lower())
            df = df[mask]

        # Agency filter
        if agency:
            agency_col = self._find_column(df, "Agency")
            if agency_col:
                df = df[df[agency_col].fillna("").str.lower().str.contains(agency.lower())]

        # Topic filter
        if topic:
            topic_col = self._find_column(df, "Topic")
            if topic_col:
                df = df[df[topic_col].fillna("").str.lower().str.contains(topic.lower())]

        # Impact type filter
        if impact_type:
            impact_col = self._find_column(df, "impact")
            if impact_col:
                df = df[df[impact_col].fillna("").str.lower().str.contains(impact_type.lower())]

        return df.head(limit)

    def get_risk_report(self) -> Dict[str, Any]:
        """Generate a risk-focused report on high-impact use cases."""
        df = self.df_2024
        impact_col = self._find_column(df, "impact")

        if not impact_col:
            return {"error": "Impact column not found"}

        # Filter to rights/safety impacting
        impact_series = df[impact_col].fillna("")

        rights_mask = impact_series.str.lower().str.contains("rights")
        safety_mask = impact_series.str.lower().str.contains("safety")
        both_mask = impact_series.str.lower().str.contains("both")

        rights_df = df[rights_mask & ~both_mask]
        safety_df = df[safety_mask & ~both_mask]
        both_df = df[both_mask]

        agency_col = self._find_column(df, "Agency")

        return {
            "rights_impacting": {
                "count": len(rights_df),
                "by_agency": rights_df[agency_col].value_counts().head(10).to_dict() if agency_col else {},
            },
            "safety_impacting": {
                "count": len(safety_df),
                "by_agency": safety_df[agency_col].value_counts().head(10).to_dict() if agency_col else {},
            },
            "both": {
                "count": len(both_df),
                "by_agency": both_df[agency_col].value_counts().head(10).to_dict() if agency_col else {},
            },
            "total_high_impact": len(rights_df) + len(safety_df) + len(both_df),
        }

    def get_column_names(self) -> List[str]:
        """Return list of column names in the dataset."""
        return self.df_2024.columns.tolist()

    def _find_column(self, df: pd.DataFrame, keyword: str) -> Optional[str]:
        """Find a column containing the keyword (case-insensitive)."""
        for col in df.columns:
            if keyword.lower() in col.lower():
                return col
        return None


# Convenience function for quick analysis
def quick_summary(data_dir: str = "/data") -> Dict[str, Any]:
    """Generate a quick summary of the inventory."""
    analyzer = AIInventoryAnalyzer(data_dir)
    return {
        "summary": analyzer.get_summary_stats(),
        "top_agencies": analyzer.get_agency_breakdown().head(10).to_dict("records"),
        "topics": analyzer.get_topic_distribution().to_dict("records"),
        "year_comparison": analyzer.get_year_comparison(),
    }
