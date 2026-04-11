import re
from pathlib import Path

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\S+\s+\S+)\s+SRC=(?P<src_ip>\S+)\s+DST_PORT=(?P<dst_port>\d+)\s+STATUS=(?P<status>\S+)$"
)


def parse_log_file(file_path: str) -> list[dict]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {file_path}")

    parsed_entries: list[dict] = []

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            match = LOG_PATTERN.match(line)
            if not match:
                continue

            parsed_entries.append(
                {
                    "timestamp": match.group("timestamp"),
                    "src_ip": match.group("src_ip"),
                    "dst_port": int(match.group("dst_port")),
                    "status": match.group("status"),
                    "line_number": line_number,
                }
            )

    return parsed_entries