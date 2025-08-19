"""Data persistence and checkpoint management."""

import json
import os
from typing import Dict, Any, List


class DataManager:
    """Handles saving and loading of scraped data and checkpoints."""
    
    def __init__(self, checkpoint_file: str, output_file: str):
        self.checkpoint_file = checkpoint_file
        self.output_file = output_file
    
    def load_checkpoint(self) -> Dict[str, Any]:
        """Load existing checkpoint data if available."""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load checkpoint file {self.checkpoint_file}: {e}")
                return {}
        return {}
    
    def save_checkpoint(self, data: Dict[str, Any]) -> None:
        """Save current progress to checkpoint file."""
        try:
            with open(self.checkpoint_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Warning: Could not save checkpoint: {e}")
    
    def save_final_results(self, results: Dict[str, Any]) -> None:
        """Save final results to output file."""
        final_list = list(results.values())
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(final_list, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(final_list)} entries to {self.output_file}")
        except IOError as e:
            print(f"Error: Could not save final results: {e}")
    
    def backup_existing_file(self) -> None:
        """Create a backup of existing output file if it exists."""
        if os.path.exists(self.output_file):
            backup_name = f"{self.output_file}.backup"
            try:
                os.rename(self.output_file, backup_name)
                print(f"Backed up existing file to {backup_name}")
            except OSError as e:
                print(f"Warning: Could not create backup: {e}")
    
    @staticmethod
    def validate_json_structure(data: Dict[str, Any]) -> bool:
        """Validate that the data has the expected structure."""
        required_fields = ["url", "name", "location", "description", "opening_hours", "prices", "services"]
        
        for entry in data.values():
            if not isinstance(entry, dict):
                return False
            for field in required_fields:
                if field not in entry:
                    return False
        return True