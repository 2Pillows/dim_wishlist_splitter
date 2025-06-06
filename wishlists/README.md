## How Filters Work

### Tags Filter

When weapon rolls are collected from Voltron, any tags found in their valuable text are collected. Valuable text is all text after "tags:" or text inside "(...)" and "[...]" if no "tags:" is present. Wishlists use these collected tags to determine which weapon rolls should be included.

### Perks Filter

Perks are filtered by comparing each perk hash to a collection of all 3rd column, 4th column, and origin trait hashes. These hashes are unique strings of numbers that represent specific perks.

### Dupes Filter

Dupes are filtered based on the frequency of each perk recommendation. Before counting, each recommendation has its perk hashes sorted and origin traits removed for consistency. If a weapon roll has multiple instances of the same perk recommendation, it is counted once.

## Filter Descriptions

**Input** - MKB (Mouse and Keyboard) or CTR (Controller). If a roll isn't tagged, MKB is assumed.

**Gamemode** - PvE or PvP. If a roll isn't tagged, PvE is assumed.

**Author** - The author for the roll. Wishlists can specify rolls from multiple authors.

**God** - Shows rolls tagged with "God".

**!Backup** - Removes rolls tagged with "Backup Roll".

**Perks** - Limits perks to 3rd column, 4th column, and origin traits. Removes perks in 1st and 2nd columns.

**Dupes** - Removes any roll that isn't recommended at least twice. Rolls for a weapon recommended only once won't be removed.

## Filter Recommendations

**Input / Gamemode / Author / Perks** - All preference, use whatever best fits your needs.

**God / !Backups / Dupes** - If you want to only see top-tier rolls, here are some options:
* God - Extremely strict, many weapons won't have any recommendations. 
* !Backups_Dupes - Less strict, won't contain niche rolls.
* God + !Backups_Dupes - Least strict, using both wishlists catches any rolls missed by either.
