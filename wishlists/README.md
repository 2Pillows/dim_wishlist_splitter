# Wishlist Filter Notes

## How Filters Work

Each roll is read from the Voltron file and given tags based on the words found in the roll description. The words used to determine tags are either the ones denoted after "tags:" or ones inside parentheses or brackets if no "tags:" is present.

## Filter Descriptions

**Input** - MKB (Mouse and Keyboard) or CTR (Controller). If a roll has no tag for MKB or CTR, MKB is assumed.

**Gamemode** - PvE or PvP. If a roll has no tag for PvE or PvP, PvE is assumed.

**Author** - The name of the author for the roll.

**God** - Only shows rolls that have "God" as a tag. Extremely strict and reliant on Voltron for properly tagging rolls as "God" since not all "God Rolls" may be properly tagged.

**!Backup** - Removes any roll that has "backup roll" or a similar phrase. Less strict version of "God".

**Perks** - Removes the 1st and 2nd column perks from all weapons on the list. Only 3rd, 4th, and origin traits will be included.

**Dupes** - Removes any roll that doesn't appear at least 2 times. Requires multiple authors to publish roll recommendations since based on total number of appearances.
