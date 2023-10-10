import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class XmlSourceWriter:
    MAX_SIZE = 10 * 1024 * 1024  # Max size in bytes for output XML files

    def __init__(
        self, *, target_dir: Path, output_stub: Optional[str] = None, counter: int = 1
    ) -> None:
        self.target_dir = target_dir
        self.output_stub = output_stub or str(target_dir.parts[-1])
        self.counter = counter
        self.result = []
        self.total_size = 0

    @property
    def current_filename(self) -> str:
        return f"{self.output_stub}-{self.counter}.xml"

    def write(self, xmlstring: bytes) -> None:
        this_size = len(xmlstring)

        # If adding the latest result would lead to the file size going over the limit, save
        if xmlstring and self.total_size + this_size > self.MAX_SIZE:
            self.write_xml(
                self.result,
                self.target_dir / self.current_filename,
            )
            self.total_size = 0
            self.result = []
            self.counter += 1

        if xmlstring:
            self.result.append(xmlstring)
            self.total_size += this_size

    def flush(self) -> None:
        if len(self.result) > 0:
            self.write_xml(self.result, self.target_dir / self.current_filename)

    def write_xml(self, texts: list[bytes], xmlpath: Path):
        """Wrap 'text' in a file tag and save as 'xmlpath'."""
        corpus_source_dir = Path(xmlpath).parent
        corpus_source_dir.mkdir(exist_ok=True, parents=True)
        with open(xmlpath, "wb") as f:
            f.write(b"<file>\n")
            for text in texts:
                f.write(text)
                f.write(b"\n")
            f.write(b"</file>\n")
        logger.info("  File %s written", xmlpath)
