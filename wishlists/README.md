## How Filters Work

### Tag Filters

When weapon rolls are collected from Voltron, any tags found in their valuable text are collected. Valuable text is all text after "tags:" or text inside "(...)" and "[...]" if no "tags:" is present. Wishlists use these collected tags to determine which weapon rolls should be included. For a weapon roll to be included, it must contain all the include tags and none of the exclude tags.

### Perks Filters

Perks are filtered by comparing each hash to a collection of all 3rd column, 4th column, and origin trait hashes. These hashes are unique strings of numbers that represent specific perks.

### Dupes Filters

Dupes are filtered based on the frequency of each perk recommendation. Before counting, each recommendation has its perk hashes sorted and origin traits removed. If a weapon roll has multiple instances of the same perk recommendation, it is counted once.

## Filter Descriptions

**Input** - MKB (Mouse and Keyboard) or CTR (Controller). If a roll isn't tagged, MKB is assumed.

**Gamemode** - PvE or PvP. If a roll isn't tagged, PvE is assumed.

**Author** - The author for the roll. Wishlists can specify rolls from multiple authors.

**God** - Shows rolls tagged as "God". Extremely strict, not all top-tier rolls may be tagged as "God".

**!Backup** - Removes rolls tagged as "Backup Roll". Less strict version of "God".

**Perks** - Limits perks to 3rd column, 4th column, and origin traits. Removes perks in 1st and 2nd columns.

**Dupes** - Removes any roll that isn't recommended at least twice. Rolls for a weapon recommended only once won't be removed.
