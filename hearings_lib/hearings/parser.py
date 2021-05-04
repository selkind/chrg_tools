import re
from collections import namedtuple
from typing import NamedTuple, Tuple, List, Dict, Set


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

    def parse(self, transcript) -> Tuple[List[Dict], Set[str]]:
        transcript_start: int = None
        for i, line in enumerate(transcript):
            start_match: re.MatchObject = self.TRANSCRIPT_START_PATTERN.search(line)
            if start_match:
                transcript_start = i
                break
        if not transcript_start:
            raise TranscriptStartMatchException("The beginning of the testimony could not be found.")

        speakers: set = set()
        output = []
        contribution_start: int = None
        speaker: str = None
        seq = 1
        for i in range(transcript_start, len(transcript)):
            transcript[i] = transcript[i].strip()
            line: str = transcript[i]

            end_line: re.MatchObject = self.TRANSCRIPT_END_PATTERN.search(line)
            statement: re.MatchObject = self.PREPARED_STATEMENT_PATTERN.search(line)
            contribution: re.MatchObject = self.STANDARD_SPEAKER_PATTERN.search(line)

            if end_line:
                # must replace carriage return new lines first.
                output.append({
                    'speaker': speaker,
                    'body': self._make_entry(transcript[contribution_start: i]),
                    'seq': seq
                })
                break

            if statement or contribution:
                if contribution_start:
                    output.append({
                        'speaker': speaker,
                        'body': self._make_entry(transcript[contribution_start: i]),
                        'seq': seq
                    })
                speaker = self._configure_speaker(statement) if statement else self._configure_speaker(contribution)
                speakers.add(speaker)
                contribution_start = i
                seq += 1
        return output, speakers

    def _configure_speaker(self, regex_match: re.MatchObject) -> str:
        return f"{regex_match.group(1).replace('.', '')} {regex_match.group(2).replace('.', '').upper()}"

    def _make_entry(self, lines: list[str]) -> str:
        return " ".join(lines).replace('\r\n', '').replace('\n', '')
