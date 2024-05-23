from enum import StrEnum


class EventType(StrEnum):
    ACTIVITY_LOG = 'activity-log'
    INSTRUMENT_STREAM = 'instrument-stream'
    FORWARD_STREAM = 'forward-stream'
