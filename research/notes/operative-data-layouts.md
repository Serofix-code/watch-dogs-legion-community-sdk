# Additional operative data layouts

Observed on Steam PC DX11 on 2026-08-14. Every traversal begins with roster-identity revalidation.

## Biography events and statistics

NPC data stores age at `+0x28`, income at `+0x30`, an additional-event count at `+0x54`, an event-array pointer at `+0x58`, the primary biography event at `+0x78`, and status at `+0xC8`. Event elements occupy eight-byte slots while the observed ID is a 32-bit value. City-level birthplace is represented by detailed `BIRTH_*` event records, not only by the broader country tag.

## Appearance

Current appearance is at operative `+0x150`; wardrobe defaults are at `+0xF8`. The observed record is 24 bytes and uses big-endian bit packing. The first nine bits encode format version and the following four bits encode format type. The decoded build used version 12/type 2. Memory readback alone does not prove every component rebuilds visually.

## Perks

The perk container starts at NPC data `+0x90`. It resembles a small vector: capacity (`int32`), length (`uint16`), flags (`uint16`), then eight bytes of inline storage or an external pointer. Flag `0x8000` selects inline storage for up to two 32-bit IDs. Existing reads are useful; growth requiring a new allocation remains unresolved because one allocator signature was not unique.

## Contracts and attendance

The observed sparse contract table begins at NPC data `+0xE0`. Contracts reference participants resolvable through census data and a hashed attendance table. Attendance start/end values are stored as seconds and become hours after division by 3600. Container ownership, persistence, and AI-scheduling consequences remain unknown.
