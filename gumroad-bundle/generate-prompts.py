#!/usr/bin/env python3
"""Generate the full Lunar Myth Kintsugi Bible prompt libraries."""

import os
import random

random.seed(42)

# Base template
BASE = "{mood} lunarpunk tactile-stained-mosaic kintsugi botanist mythpunk full-body female {pose}, body meticulously constructed from {collage} with vibrant watercolor bleed painted directly over the collage, defiant folklore reassembly using {repair}, {botanicals} blooming from cracks and fractures, {tactility} for hyper-sensory tactile depth, {glitch}, {lighting}, vibrant jewel tones vs crisp black and white inking, chromatic aberration fringing, {intensity}, ultra-detailed mixed-media collage masterpiece --ar 3:4 --stylize 250 --v 6"

# Component pools
MOODS = {
    "Luminous wonder": [
        "floating gently upward with arms open",
        "rising from shattered obsidian like a phoenix",
        "emerging from a bed of glowing moonflowers",
        "standing in a shaft of silver moonlight",
        "dancing weightlessly among falling petals",
        "kneeling in a pool of bioluminescent water",
        "reaching toward a massive luminous moon",
        "spinning slowly with arms outstretched",
        "walking on a path of glowing star-ferns",
        "seated on a throne of crystallized light",
        "embracing a column of golden moonbeams",
        "floating in a void of soft silver mist",
        "standing atop a mountain of obsidian shards",
        "bathed in cascading waterfall of light",
        "surrounded by a halo of regenerative vines",
        "ascending through layers of stained-glass clouds",
        "resting in a garden of eternal moonlight",
        "standing at the edge of a glowing aurora",
        "wrapped in a cloak of living starlight",
        "levitating above a field of sleeping moonflowers",
        "pouring light from cupped hands",
        "unfurling like a bloom under first moonlight",
        "standing in doorway between worlds made of light",
        "crowned with constellation of glowing ferns",
        "transforming from shadow into radiance",
        "gathering luminous moths to her heart",
        "weaving a tapestry of captured moonbeams",
        "planting seeds of light in cracked earth",
        "singing to a choir of glowing night-blooms",
        "becoming one with the bioluminescent forest",
    ],
    "Melancholic reverie": [
        "sitting gracefully on fractured obsidian throne",
        "kneeling with head bowed in quiet sorrow",
        "standing in gentle rain of glowing petals",
        "gazing into a pool of dark water",
        "holding a wilted moonflower to her chest",
        "walking through ruins of a forgotten temple",
        "resting against a broken stained-glass window",
        "trapped in a cage of her own golden hair",
        "watching dawn break from a tower of solitude",
        "cradling a cracked obsidian mirror",
        "sitting at edge of a dissolving world",
        "lying among fallen leaves that never rot",
        "standing in doorway of abandoned chapel",
        "weeping tears that become tiny kintsugi rivers",
        "reading from a book with pages of dried petals",
        "waiting on a bench made of memory and moss",
        "wrapped in shawl woven from forgotten lullabies",
        "standing beneath a tree that grows downward",
        "holding a lantern that illuminates only shadows",
        "dancing alone in ballroom of shattered mirrors",
        "collecting fragments of broken constellations",
        "sitting in garden where time flows backwards",
        "staring at horizon that never arrives",
        "sleeping in coffin lined with pressed moonflowers",
        "walking through corridor of doors that lead nowhere",
        "playing harp with strings of silver spider silk",
        "wearing crown of dried jasmine and rust",
        "standing in puddle that reflects a different sky",
        "talking to ghost of her former self",
        "writing letters in ink made of evaporated tears",
    ],
    "Defiant rebellion": [
        "standing powerfully with fist raised",
        "leaping defiantly through wall of flames",
        "breaking chains of obsidian with raw strength",
        "shattering a stained-glass ceiling with spear",
        "running toward viewer with fragments trailing",
        "standing atop pile of broken idols",
        "tearing open her chest to reveal glowing heart",
        "screaming into void that cracks and bleeds light",
        "wielding a whip made of golden kintsugi thread",
        "painting her body with molten gold and ash",
        "dancing on grave of every doubt she ever had",
        "burning a bridge made of her own fears",
        "carving her name into wall of infinite darkness",
        "lifting a mountain of shattered expectations",
        "wearing armor forged from rejected versions of herself",
        "planting a flag of iridescent silk on peak of ruin",
        "splitting the earth with a stomp of pure will",
        "grabbing lightning and bending it into a crown",
        "refusing to kneel even as gravity intensifies",
        "walking through fire that parts for her alone",
        "smashing a mirror that shows only obedience",
        "composing symphony on instrument made of broken glass",
        "unleashing a storm of embroidered butterflies",
        "rewriting constellations to spell her true name",
        "drinking poison that turns to wine in her throat",
        "strangling the serpent of self-doubt with bare hands",
        "dancing on tightrope stretched between two collapsing worlds",
        "refusing to fade even as colors drain away",
        "building fortress from fragments of betrayed trust",
        "laughing as the old world burns behind her",
    ],
    "Sacred-profane tension": [
        "kneeling in prayer pose with torn garments",
        "holding a chalice made of obsidian and gold",
        "standing at altar where incense meets datamosh",
        "wearing halo of thorns and moonflowers",
        "bleeding light from wounds that heal instantly",
        "preaching to congregation of broken statues",
        "baptizing herself in pool of liquid mercury",
        "carrying cross made of stitched newspaper and wire",
        "communion with serpent wrapped around golden arm",
        "standing between cathedral and cybernetic shrine",
        "praying with hands that spark electricity",
        "wearing robes that shift between silk and static",
        "offering her heart on plate of pressed flowers",
        "ascending staircase that exists in two dimensions",
        "crowned with both halo and horns simultaneously",
        "holding bible with pages of corrupted code",
        "blessing a crowd of faceless mannequins",
        "standing in confessional booth made of transparent obsidian",
        "anointing her forehead with oil that shifts colors",
        "wearing veil that reveals more than it hides",
        "dancing on grave of forgotten gods",
        "eating fruit from tree of knowledge and regret",
        "baptizing a robot in pool of living watercolor",
        "burning incense that forms faces of ancestors",
        "standing at intersection of holiness and heat",
        "wearing necklace of saints and sinners intertwined",
        "preaching from pulpit made of fused keyboards",
        "offering wine that tastes like forgotten memories",
        "praying in language that predates sound",
        "embodying both Madonna and Medusa at once",
    ],
    "Nocturnal mystery": [
        "walking through moonlit ruins with veil half-lifted",
        "partially veiled in shadow with glowing eyes",
        "emerging from a well of liquid starlight",
        "standing in fog that whispers secrets",
        "hunting through forest where trees have eyes",
        "peering through keyhole into another dimension",
        "wearing mask made of moth wings and midnight",
        "disappearing into corridor that breathes",
        "reading fortune in pool of black mercury",
        "standing at crossroads where all paths are wrong",
        "holding lantern that attracts only shadows",
        "dancing with partner made of smoke and rumor",
        "collecting teeth from dreams of strangers",
        "wearing cloak sewn from fragments of night",
        "standing in room where gravity forgets direction",
        "pouring tea that steams with faces",
        "walking backwards through mirror maze",
        "whispering to ravens who whisper back prophecies",
        "standing in garden where flowers bloom only in echo",
        "playing chess with opponent who has no face",
        "wearing perfume distilled from abandoned lullabies",
        "opening door that leads to yesterday's tomorrow",
        "standing in rain that falls upward at midnight",
        "holding key made of frozen moonlight",
        "sitting in chair that remembers everyone who sat before",
        "wearing gloves that leave trails of stardust",
        "walking through market that sells only memories",
        "drinking from cup that shows future in reflection",
        "standing in circle of candles that never melt",
        "becoming shadow that other shadows fear",
    ],
    "Primordial chaos": [
        "in swirling vortex of shattered matter",
        "exploding outward as form and void collide",
        "dancing in storm where gravity fluctuates",
        "being born from crack between realities",
        "merging with swarm of bioluminescent particles",
        "tearing open sky to reveal the machinery behind",
        "dissolving and reconstituting in endless cycle",
        "conducting orchestra of screaming colors",
        "standing at center of fracturing timeline",
        "feeding on pure unfiltered starlight",
        "unraveling like tapestry caught in hurricane",
        "becoming living bridge between order and entropy",
        "screaming a song that rewrites physics",
        "wearing dress made of unstable elements",
        "dancing on surface of collapsing neutron star",
        "holding together world with threads of will alone",
        "transforming through all seven elements simultaneously",
        "standing in eye of storm made of pure potential",
        "giving birth to constellation from her chest",
        "eating pomegranate that contains all possible futures",
        "walking through gallery where paintings bleed into reality",
        "wearing crown of compressed supernovas",
        "swimming in ocean where waves are made of sound",
        "standing in place where geometry fails",
        "weaving reality from strands of dark matter",
        "becoming axis around which chaos organizes",
        "drinking from fountain of uncreated colors",
        "holding map that changes based on who reads it",
        "standing at edge of universe watching it fold",
        "becoming the storm she was born to survive",
    ],
    "Ethereal grace": [
        "dancing slowly in mid-air with fabric flowing",
        "floating through corridor of weightless water",
        "gliding on currents of invisible music",
        "ascending spiral staircase made of frozen breath",
        "drifting like feather in zero gravity",
        "unfurling from cocoon of translucent silk",
        "walking on surface of still lake without ripples",
        "being carried by wind that knows her name",
        "dissolving into mist and reforming as rain",
        "standing on cloud that shapes itself to her thoughts",
        "weaving garland from strands of captured dawn",
        "singing note that suspends all motion",
        "wearing gown that weighs less than a promise",
        "moving through space as if time is suggestion",
        "collecting dewdrops on eyelashes like jewels",
        "resting on bed of floating lily pads in sky",
        "brushing hair with comb made of hummingbird wings",
        "standing in field where gravity is gentle suggestion",
        "blowing bubbles that contain entire peaceful worlds",
        "wearing necklace of captured sighs",
        "dancing so slowly she appears to be sculpture in motion",
        "floating in sphere of perfect silence",
        "walking up waterfall as if it were staircase",
        "wearing crown of frost that never melts",
        "stretching like cat made of morning light",
        "resting in hammock strung between two moons",
        "bathing in pool of liquid moonstone",
        "whispering to flowers that lean toward her voice",
        "becoming so still that dust settles on her like snow",
        "transcending physical form in moment of pure beauty",
    ],
}

COLLAGES = [
    "sliced newspaper clippings and vintage photo cutouts",
    "layered Japanese newsprint and black-and-white portrait fragments",
    "torn financial headlines and botanical illustration fragments",
    "aged obituary text and scientific journal fragments",
    "vintage magazine clippings and handwritten letter pieces",
    "layered book pages and cartographic fragments",
    "sliced concert posters and poetry chapbook pages",
    "torn blueprint sections and astronomical chart pieces",
]

REPAIRS = [
    "iridescent stained-glass mosaic shards and obsidian repaired by glowing golden kintsugi veins",
    "sharp obsidian fragments with thick bold golden kintsugi",
    "delicate hairline kintsugi on fractured porcelain-white skin",
    "web-pattern kintsugi across shattered mosaic surfaces",
    "river-flow kintsugi connecting obsidian shards like golden arteries",
    "stained-glass cathedral fragments repaired with molten gold",
    "obsidian geode cracks sealed with luminescent kintsugi resin",
    "porcelain doll fractures mended with threads of starlight",
]

BOTANICALS = [
    "lush regenerative moonflowers and iridescent ivy",
    "thorned shadow roses and bioluminescent vines",
    "star ferns and lunar orchids cascading",
    "night jasmine and obsidian lilies",
    "evening primrose and silver artemisia",
    "wild angel's trumpet and glowing mushrooms",
    "moonflowers and star ferns blooming abundantly from golden kintsugi cracks",
    "iridescent ivy and lunar orchids cascading down her body",
    "thorned shadow roses and bioluminescent vines bursting through obsidian",
    "night jasmine and obsidian lilies wilting yet reviving",
    "lunar orchids and white lotus contrasting with thorned shadow roses",
    "star ferns and glowing moonflowers weaving through stained-glass shards",
    "bioluminescent vines and thorned shadow roses erupting chaotically",
    "iridescent ivy and lunar orchids flowing gracefully",
    "evening primrose and silver artemisia catching moonlight",
]

TACTILITIES = [
    "extreme heavy visible embroidery with raised thread patterns and clustered pearl beading",
    "dense sashiko stitching in Kikkō pattern with yarn tufting",
    "intricate Yabane arrow-feather stitching with crystal clusters",
    "heavy chain stitch vines with matte glass bead clusters",
    "visible French knots and bullion knots creating tactile topography",
    "couched gold thread forming kintsugi-inspired raised lines",
    "blanket stitch borders with scattered seed pearl accents",
    "feather stitch botanicals with faceted crystal dewdrops",
]

GLITCHES = [
    "subtle datamosh glitch distortion melting collage edges",
    "controlled pixel sorting on sleeve and hem transitions",
    "strong channel-shift chromatic aberration",
    "gentle datamosh shimmer with soft RGB split",
    "digital corruption blooming like frost across obsidian surfaces",
    "scan-line interference rippling through watercolor layers",
    "mosaic tile displacement creating shifting pattern illusions",
    "temporal ghosting leaving trails of previous poses",
]

LIGHTINGS = [
    "ethereal lunarpunk bioluminescent moonlight creating soft halo",
    "dramatic lunarpunk moonlight from behind with rim lighting",
    "diffuse silver-blue glow with floating particle dust",
    "sharp contrast moonlight with deep indigo shadows",
    "multidirectional bioluminescence from botanical elements themselves",
    "golden hour filtered through stained-glass creating prismatic shadows",
    "cold lunar spotlight with warm kintsugi accent lighting",
    "pulsing aurora borealis wrapping around the figure",
]

INTENSITIES = [
    "regenerative sensory wonder",
    "ethereal wondrous mood",
    "deeply melancholic beauty",
    "fierce regenerative defiance",
    "dramatic sacred-profane tension",
    "deep enigmatic mood",
    "raw primordial power",
    "transcendent graceful beauty",
    "luminous hopeful atmosphere",
    "quiet introspective sorrow",
    "powerful rebellious energy",
    "holy yet broken contrast",
    "mysterious nocturnal allure",
    "explosive chaotic force",
    "delicate yet unbreakable elegance",
]


def generate_prompt(mood_name):
    """Generate a single prompt for a given mood."""
    return BASE.format(
        mood=mood_name,
        pose=random.choice(MOODS[mood_name]),
        collage=random.choice(COLLAGES),
        repair=random.choice(REPAIRS),
        botanicals=random.choice(BOTANICALS),
        tactility=random.choice(TACTILITIES),
        glitch=random.choice(GLITCHES),
        lighting=random.choice(LIGHTINGS),
        intensity=random.choice(INTENSITIES),
    )


def generate_all_prompts():
    out_dir = "prompts"
    os.makedirs(out_dir, exist_ok=True)

    # Generate mood-specific prompt files
    all_prompts = []
    mood_counts = {}

    for mood_name, poses in MOODS.items():
        # Generate ~52 prompts per mood
        prompts = []
        seen = set()
        target = 52
        attempts = 0
        while len(prompts) < target and attempts < target * 3:
            p = generate_prompt(mood_name)
            if p not in seen:
                seen.add(p)
                prompts.append(p)
            attempts += 1

        # Write mood file
        safe_name = mood_name.lower().replace(" ", "_").replace("-", "_")
        with open(os.path.join(out_dir, f"{safe_name}_prompts.txt"), "w") as f:
            f.write(f"# {mood_name.upper()} PROMPTS\n")
            f.write(f"# Count: {len(prompts)}\n")
            f.write("=" * 60 + "\n\n")
            for i, p in enumerate(prompts, 1):
                f.write(f"[{i}]\n{p}\n\n")

        all_prompts.extend(prompts)
        mood_counts[mood_name] = len(prompts)

    # Write master file with all prompts
    with open(os.path.join(out_dir, "ALL_PROMPTS_357.txt"), "w") as f:
        f.write("# LUNAR MYTH KINTSUGI BIBLE\n")
        f.write("# Complete Prompt Library\n")
        f.write(f"# Total: {len(all_prompts)} prompts\n")
        f.write("# Generated: 2026\n")
        f.write("# By: Jennipher Troup\n\n")
        f.write("## Mood Breakdown\n")
        for mood, count in mood_counts.items():
            f.write(f"# {mood}: {count} prompts\n")
        f.write("\n" + "=" * 60 + "\n\n")
        for i, p in enumerate(all_prompts, 1):
            f.write(f"[{i:03d}]\n{p}\n\n")

    # Write signature/hero prompts file
    hero_prompts = []
    for mood_name in MOODS:
        hero_prompts.append(generate_prompt(mood_name))

    with open(os.path.join(out_dir, "SIGNATURE_HERO_PROMPTS.txt"), "w") as f:
        f.write("# SIGNATURE HERO PROMPTS\n")
        f.write("# One representative prompt per mood\n")
        f.write("# Use these as style anchors and starting points\n\n")
        for mood_name, p in zip(MOODS, hero_prompts):
            f.write(f"## {mood_name.upper()}\n{p}\n\n")

    # Write fashion prompts
    fashion_prompts = []
    for _ in range(20):
        fashion_prompts.append(
            f"High fashion editorial of lunarpunk tactile-stained-mosaic kintsugi botanist mythpunk full-body female model wearing {random.choice(['a structured corset gown','an ethereal floating cape','a utilitarian boro jumpsuit','an armor-inspired dress','a flowing slip dress','a regenerative botanical gown','a mosaic-panelled bodice','a newspaper-print silk robe'])}, garment constructed from {random.choice(COLLAGES)}, featuring {random.choice(REPAIRS)}, adorned with {random.choice(TACTILITIES)}, botanical elements {random.choice(BOTANICALS)}, {random.choice(GLITCHES)}, {random.choice(LIGHTINGS)}, {random.choice(INTENSITIES)}, ultra-detailed fashion photography, dramatic {random.choice(['runway','studio','street'])} setting --ar 9:16 --stylize 250 --v 6"
        )

    with open(os.path.join(out_dir, "FASHION_PROMPTS.txt"), "w") as f:
        f.write("# FASHION EDITORIAL PROMPTS\n")
        f.write(f"# Count: {len(fashion_prompts)}\n\n")
        for i, p in enumerate(fashion_prompts, 1):
            f.write(f"[{i}]\n{p}\n\n")

    # Write tattoo prompts
    tattoo_prompts = []
    for _ in range(15):
        tattoo_prompts.append(
            f"Vertical tattoo flash design of lunarpunk tactile-stained-mosaic kintsugi botanist mythpunk female {random.choice(['upper body','full sleeve','back piece','thigh piece','chest panel'])}, {random.choice(COLLAGES)} style with watercolor bleed, {random.choice(REPAIRS)}, {random.choice(BOTANICALS)}, bold black and white with {random.choice(['vibrant teal','magenta','gold','electric blue'])} highlights, {random.choice(GLITCHES)}, clean linework, tattoo flash sheet composition --ar 2:3 --stylize 250 --v 6"
        )

    with open(os.path.join(out_dir, "TATTOO_PROMPTS.txt"), "w") as f:
        f.write("# TATTOO FLASH PROMPTS\n")
        f.write(f"# Count: {len(tattoo_prompts)}\n\n")
        for i, p in enumerate(tattoo_prompts, 1):
            f.write(f"[{i}]\n{p}\n\n")

    # Write negative prompts
    negative = """# MASTER NEGATIVE PROMPT
# Use with every generation

blurry, lowres, deformed, ugly, extra limbs, bad anatomy, watermark, text, logo, oversaturated, flat lighting, minimalism, plastic skin, cartoon, 3d render, smooth surfaces, no texture, no embroidery, no beading, no watercolor bleed, no stained glass, no kintsugi gold, no botanical growth, no datamosh, no lunarpunk glow, modern clean design, photorealistic skin, doll-like, low detail, dull colors, seamless digital look, no torn paper edges, no visible newspaper text, overexposed, underexposed, bad composition

# MOOD-SPECIFIC NEGATIVES

Luminous Wonder: dark, creepy, horror, heavy shadows, gloomy
Defiant Rebellion: weak pose, passive, defeated, timid, sad
Melancholic Reverie: bright daylight, overly cheerful, cartoonish
Primordial Chaos: organized, clean, symmetrical, static, minimal
Nocturnal Mystery: bright daylight, overexposed, cheerful
Ethereal Grace: chaotic, aggressive, dark, heavy
Sacred-Profane: plain, simple, minimal, modern
"""

    with open(os.path.join(out_dir, "NEGATIVE_PROMPTS.txt"), "w") as f:
        f.write(negative)

    print(f"Generated {len(all_prompts)} total prompts across {len(MOODS)} moods")
    print(f"Files written to {out_dir}/")
    for mood, count in mood_counts.items():
        print(f"  {mood}: {count} prompts")
    print(f"  Fashion: {len(fashion_prompts)} prompts")
    print(f"  Tattoo: {len(tattoo_prompts)} prompts")
    print(f"  Signature heroes: {len(hero_prompts)} prompts")

    return all_prompts


if __name__ == "__main__":
    generate_all_prompts()
