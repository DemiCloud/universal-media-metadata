"""Internal Variables"""

# region imports
from dataclasses import dataclass
from typing import final,Final
from pathlib import Path
# endregion

@final
@dataclass
class Constants:
  """module costants"""
  # pylint: disable=invalid-name
  NAME: Final[str]= "Universal Media Metadata"

  class Table:
    """table configuration"""
    class Title:
      """table title configuration"""
      JUSTIFY: Final[str] = "left"
      STYLE: Final[str] = "bold cyan"

@dataclass
class Config:
  """Configuration File Variables"""
  class Schema:
    """Scheme Configuration"""
    dir: Path

@dataclass
class Variable:
  """Mutable Variables"""
  app_name: str
  rel_dir: Path
