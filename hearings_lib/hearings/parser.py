import re
from collections import namedtuple
from typing import NamedTuple


class TranscriptStartMatchException(Exception):
    pass


class Parser:
    TRANSCRIPT_START_PATTERN: re.RegexObject = re.compile(
        r'The\\s+.{1,5}ommittee(s?)\\s+met,\\s+pursuant\\s+to\\s+(notice|call),\\s+at'
    )
    PREPARED_STATEMENT_PATTERN: re.RegexObject = re.compile(
        r'^\\[The\\s+prepared\\s+statement\\s+of\\s+([A-Z,a-z]*\\.?)\\s+([A-Z,a-z,\\-]+)'
    )
    STANDARD_SPEAKER_PATTERN: re.RegexObject = re.compile(
        r'^([A-Z][a-z]+\\.?)\\s+(([A-Z][A-z]+-){0,1}(([A-Z]){2,})\\.)\\s+'
    )
    TRANSCRIPT_END_PATTERN: re.RegexObject = re.compile(
        r'\\[Whereupon,'
    )
    Speaker: NamedTuple = namedtuple('Speaker', ['name', 'member_id'])

    def __init__(self):
        self.output: list[tuple] = []
        self.speakers: dict[str, int] = {}

    @property
    def contribution_count(self):
        return len(self.output)

    @property
    def speaker_count(self):
        return len(self.speakers)

    def parse(self, transcript) -> None:
        # clear out stored state for new transcript
        self.output = []
        self.speakers = []
        transcript_start: int = None
        for i, line in enumerate(transcript):
            start_match: re.MatchObject = self.TRANSCRIPT_START_PATTERN.search(line)
            if start_match:
                transcript_start = i
                break
        if not transcript_start:
            raise TranscriptStartMatchException("The beginning of the testimony could not be found.")

        contribution_start: int = None
        speaker: str = None
        for i in range(transcript_start, len(transcript)):
            line: str = transcript[i]
            transcript[i] = line.strip()

            end_line: re.MatchObject = self.TRANSCRIPT_END_PATTERN.search(line)
            statement: re.MatchObject = self.PREPARED_STATEMENT_PATTERN.search(line)
            contribution: re.MatchObject = self.STANDARD_SPEAKER_PATTERN.search(line)

            if end_line:
                # must replace carriage return new lines first.
                entry: str = self._make_entry(transcript[contribution_start: i])
                self.output.append((speaker, entry))
                break

            if statement or contribution:
                if contribution_start:
                    entry = self._make_entry(transcript[contribution_start: i])
                    self.output.append((speaker, entry))
                    speaker = self.config
                speaker = self._configure_speaker(statement) if statement else self._configure_speaker(contribution)
                contribution_start = i

    def _configure_speaker(self, regex_match: re.MatchObject) -> NamedTuple:
        name: str = f"{regex_match.group(1).replace('.', '')} {regex_match.group(2).replace('.', '').upper()}"
        if name not in self.speakers:
            self.speakers[name] = self._match_speaker_to_member_id(name)
        return self.Speaker(name, self.speakers[name])

    def _match_speaker_to_member_id(self, name: str) -> int:
        return 0

    def _make_entry(self, lines: list[str]) -> str:
        return " ".join(lines).replace('\r\n', '').replace('\n', '')
