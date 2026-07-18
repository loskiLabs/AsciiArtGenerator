from pathlib import Path


class FileSaver:
    """Save text content to files."""

    def save(self, content, filename="output/output.txt"):
        """Save text content with UTF-8 encoding."""
        output_path = Path(filename)

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding="utf-8")
            print(f"ASCII art saved to {output_path}")
        except OSError as error:
            print(f"Error saving ASCII art to '{output_path}': {error}")
