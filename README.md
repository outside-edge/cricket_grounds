# Cricket grounds

A reusable, dated bridge from ESPNcricinfo ground profile IDs to cricket
jurisdictions. Download [grounds.csv](grounds.csv) or read it directly from a
commit-pinned raw GitHub URL. No R package or cricket-rating code is required.

The initial coverage is the set of grounds in Side Order's men's Test, ODI, and
T20I match-results snapshot through 2026-10-25. It is not a census of every cricket
ground. Venue IDs and location labels come from the ground links in those result
tables. The table includes historical venues and grounds whose matches had no result.

## Join contract

Join a match's `ground_profile_id` to this table and require
`valid_from <= match_date < valid_until`. There must be at most one matching row.
Keep unmatched matches and flag their country as unknown. An unknown country is
not a neutral venue. Do not join by the short location label alone.

Country means **cricket jurisdiction**, rather than sovereign state: England
includes Welsh venues, Ireland includes venues in Northern Ireland, West Indies
is one jurisdiction, and Scotland, Jersey, Guernsey, and the Isle of Man are
separate. Happy Valley's British military facilities belong to the Cyprus cricket
jurisdiction. Applications using ISO country codes need a separate geographic map.

Validity intervals encode the supported assignment, not a stadium's opening or
closure. Legacy links use an open historical interval; newly verified locations
begin at the earliest observed match in the source snapshot. A split interval for
Dhaka preserves the historical Pakistan/Bangladesh distinction and leaves the
1971 transition gap unassigned.

## Columns

| Column | Type | Meaning |
| --- | --- | --- |
| `ground_profile_id` | Positive integer | ESPNcricinfo profile ID; distinct from the legacy ground table's IDs |
| `ground_label` | UTF-8 string | Location label in the source match-results table; not necessarily a full stadium name |
| `country` | UTF-8 string | Cricket jurisdiction during the validity interval |
| `valid_from` | ISO date | Inclusive lower bound |
| `valid_until` | ISO date | Exclusive upper bound; `9999-12-31` means no known end |
| `source` | HTTPS URL | Evidence for the jurisdiction or geographic location |
| `method` | Category | `legacy_match_link`, `audited_jurisdiction`, or `verified_location` |
| `reference_match_id` | Positive integer | A match in the initial source snapshot that identifies this ground profile |
| `reference_ground` | Nullable string | Full ground name in the linked legacy match, when available |

`legacy_match_link` uses an exact shared match ID to connect the current ground
profile to a full legacy ground name, then an exact name-to-country lookup.
`audited_jurisdiction` records an explicit dated override. `verified_location`
assigns the country of the observed location using the cited source; it does not
assert an exact stadium identity when sources use different ground names.
Countries are not inferred from participating teams, winners, or match scores.

The initial source receipts are in [provenance.json](provenance.json). Every legacy
link was checked against its recorded reference match and full ground name. New
locations were checked using cricket bodies, venue operators, public authorities,
and published competition records. For example, the Clayton venue is in Panama;
a secondary score site's Florida label was not adopted.

## Use and update

```r
grounds <- read.csv("grounds.csv", colClasses = c(ground_profile_id = "integer"))
grounds$valid_from <- as.Date(grounds$valid_from)
grounds$valid_until <- as.Date(grounds$valid_until)
```

Use the join contract above when attaching countries to match records. Pin the
Git commit and record a SHA-256 checksum for reproducible analyses.

For corrections or additions, edit `grounds.csv`, retain the supporting source,
and run:

```sh
python3 -m unittest discover -s tests -v
```

The checks validate the actual data: IDs, schema, sources, method values, date
intervals, uniqueness, and interval overlap. A changed location or jurisdiction
needs a dated row; it must not overwrite earlier history. New evidence can extend
an interval backward when earlier matches are verified.

The compilation and validation code are released under [CC0](LICENSE). Linked
source material retains its own terms; no source article text is redistributed.
