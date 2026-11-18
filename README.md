# World News — Tuesday, 17 November 2026

[![news-image-20261117](https://make.fun/bounty/news-image-20261117/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/bounty/news-image-20261117/tiars837/news-image-17-nov/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/bounty/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

One image that sums up the world's news of **Tuesday, 17 November 2026**,
built for the [make.fun](https://make.fun) bounty
`news-image-20261117`.

## The image

An editorial front page drawn entirely from code (`generate.py`, Python + PIL,
DejaVu fonts): masthead, the date in large red type, and six stories that
defined the day, each with its own small illustration drawn with vector
shapes — no photographs, no downloaded assets, no AI-generated imagery.

1. **Kerch Bridge struck again** — Ukraine hits the road-and-rail link to
   Crimea for a second straight day; a span collapses into the Kerch Strait.
2. **Tankers hit as Gulf tensions flare** — US strikes hit Qeshm Island;
   Iranian drones target a US base in Bahrain; a tanker hits a mine.
3. **West urges Israel: open Gaza crossings** — four nations call the
   situation catastrophic; the UN warns 1.7 million remain displaced.
4. **Trump opens Asia trip; Xi meeting set** — Trump lands in Manila for a
   Quad summit; a Xi–Trump–Putin meeting is set.
5. **Japan scrambles jets after Russian incursion** — two suspected Russian
   aircraft enter Japanese airspace; Tokyo lodges a strong protest.
6. **Five EU states plan Rwanda return hub** — rejected asylum seekers to be
   sent to a return hub in Rwanda.

Also on the day: Mongolia's president resigns amid a corruption scandal;
Depardieu admits a sexual assault charge in Paris; COP31 climate talks enter
a decisive stage in Antalya.

## How it runs

`main.ts` (Node 22) copies `entry.png` from this repository to
`/output/entry.png`. It uses no network, and every run writes the same
bytes. The output directory is never removed itself — only its contents are
cleared — because the grader mounts `/output` as a volume.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Stories were checked against world-news reporting of 17 November 2026
(Associated Press-style digests, Arab News, NPR News Now, Foreign Exchanges,
and other same-day roundups). Nothing is speculation presented as fact.

## License

MIT — see `LICENSE`.
