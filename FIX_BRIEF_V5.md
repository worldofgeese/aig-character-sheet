# Fix Brief: New Player Friendly Enhancements (v4)

## Branch
Work on branch `feat/v4-new-player-friendly`. Do NOT merge to main.

## Overview
Make the character sheet genuinely new-player-friendly. A player who has never seen Mythras or RuneQuest should be able to create a character and understand what every number means.

## Feature 1: Contextual Help Text on Every Step

Add brief, friendly explanation text to each wizard step explaining WHY the player is doing this and what it means for their character. Not rules text — plain English.

### Step 1 (Concept)
Current: "Begin by imagining your character. Who are they? What drives them?"
Add: Nothing needed — this is already good.

### Step 2 (Characteristics)  
Add after the header paragraph:
```html
<div class="help-box">
  <b>What do these mean?</b>
  <ul>
    <li><b>STR</b> (Strength) — How strong you are. Affects damage in melee and how much you can carry.</li>
    <li><b>CON</b> (Constitution) — Your health and stamina. Determines hit points and healing speed.</li>
    <li><b>SIZ</b> (Size) — Your physical size. Affects hit points, damage, and how hard you are to knock down.</li>
    <li><b>DEX</b> (Dexterity) — Agility and reflexes. Affects action points, initiative, and many skills.</li>
    <li><b>INT</b> (Intelligence) — Reasoning and memory. Affects action points, initiative, and knowledge skills.</li>
    <li><b>POW</b> (Power) — Spiritual strength and willpower. Determines magic points and luck points.</li>
    <li><b>CHA</b> (Charisma) — Force of personality. Affects social skills and experience advancement.</li>
  </ul>
</div>
```

### Step 3 (Attributes)
Add explanations for each derived attribute:
- **Action Points (AP):** "How many actions you get per combat round — attack, parry, cast a spell, or move."
- **Damage Modifier (DM):** "Extra damage (or penalty) added to your melee attacks based on your size and strength."
- **Experience Modifier:** "Bonus (or penalty) to improvement rolls between adventures."
- **Healing Rate:** "How many hit points you naturally recover per day of rest."
- **Initiative Bonus:** "Added to your initiative roll to determine who acts first in combat."
- **Luck Points:** "Spend these to re-roll a failed skill check or reduce damage. Very precious!"
- **Magic Points (MP):** "Fuel for casting spells. Equal to your POW. Regenerate daily."
- **Movement Rate:** "How far you can move in a combat round (in metres)."

### Step 4 (Culture)
Add: "Your culture shapes who you are — the skills you learned growing up, the fighting styles your people use, and what you believe in. Pick the culture that fits your character concept."

### Step 5 (Cultural Skills)
Add: "These are the skills your character learned growing up in their culture. You have 100 points to distribute among them. Put more points in skills you want your character to be good at."

### Step 8 (Career)  
Add: "Your career is what your character does for a living. It determines which professional skills you can learn. A Warrior fights, a Merchant trades, a Shaman speaks to spirits."

### Step 10 (Bonus Points)
Add: "These are extra skill points from life experience. Older characters get more points but may have physical penalties. Spend these on any skills you want to improve — or pick up a new hobby!"

### Step 11 (Equipment)
Add: "Buy weapons, armor, and gear with your starting money. Your culture determines how much money you start with."

### CSS for help boxes:
```css
.help-box {
  background: #f0f4ff;
  border-left: 3px solid var(--accent);
  padding: 10px 15px;
  margin: 10px 0;
  font-size: 0.9em;
  line-height: 1.5;
  border-radius: 0 4px 4px 0;
}
.help-box ul { margin: 5px 0; padding-left: 20px; }
.help-box li { margin: 3px 0; }
```

## Feature 2: Skill Tooltips (ℹ️)

Add an ℹ️ icon next to each skill name. On hover (desktop) or tap (mobile), show a tooltip with a one-line description of what the skill does in play.

### Implementation
Add a `SKILL_DESCRIPTIONS` constant with descriptions for each skill. Example entries:
```js
const SKILL_DESCRIPTIONS = {
  "Athletics": "Running, jumping, climbing, throwing. Used for physical feats of agility and endurance.",
  "Brawn": "Raw physical power. Lifting, breaking, pushing, holding doors shut.",
  "Conceal": "Hiding objects on your person or in the environment.",
  "Customs": "Knowledge of your own culture's laws, traditions, and social norms.",
  "Dance": "Formal and ritual dancing. Also used for balance and grace.",
  "Deceit": "Lying, misdirection, and fast-talking. Opposed by Insight.",
  "Drive": "Handling carts, chariots, and wagons.",
  "Endurance": "Resisting fatigue, poison, disease, and harsh conditions.",
  "Evade": "Dodging attacks and diving for cover. You end up prone afterward.",
  "First Aid": "Emergency wound treatment. Stops bleeding and restores 1d3 hit points.",
  "Influence": "Persuasion, negotiation, and charm. Getting people to agree with you.",
  "Insight": "Reading people — detecting lies, sensing motives, understanding emotions.",
  "Locale": "Knowledge of local geography, landmarks, and navigation in familiar areas.",
  "Perception": "Spotting hidden things, noticing ambushes, finding clues, and general awareness.",
  "Ride": "Staying mounted, controlling a horse or other mount in difficult situations.",
  "Sing": "Vocal performance. Also used for storytelling and oral tradition.",
  "Stealth": "Moving quietly, hiding in shadows, and avoiding detection.",
  "Swim": "Swimming and diving. Failing can mean drowning.",
  "Unarmed": "Fighting without weapons. Punching, kicking, grappling.",
  "Willpower": "Mental resilience. Resisting fear, magic, intimidation, and temptation.",
  "Boating": "Rowing, sailing small boats, and river navigation.",
  // Professional skills
  "Acrobatics": "Tumbling, backflips, tightrope walking. Flashy physical stunts.",
  "Acting": "Pretending to be someone else. Different from Deceit — this is theatrical.",
  "Commerce": "Buying, selling, and evaluating the worth of goods and services.",
  "Courtesy": "Court etiquette, formal address, and navigating noble society.",
  "Healing": "Long-term medical care, surgery, treating disease. Slower but more thorough than First Aid.",
  "Lore": "Academic knowledge of a specific subject (History, Mythology, etc.).",
  "Musicianship": "Playing musical instruments. Used for entertainment and ritual.",
  "Navigate": "Finding your way across unfamiliar terrain using stars, landmarks, and maps.",
  "Seduction": "Romantic or sexual persuasion.",
  "Streetwise": "Knowing the criminal underworld — finding black markets, fences, and underground contacts.",
  "Survival": "Living off the land — finding food, water, shelter in the wilderness.",
  "Track": "Following footprints, trails, and signs left by creatures or people.",
  "Folk Magic": "Simple, common magic available to everyone. Spells like Bladesharp, Heal, and Protection."
};
```

### Tooltip CSS:
```css
.skill-tooltip {
  position: relative;
  display: inline-block;
  cursor: help;
  margin-left: 4px;
  font-size: 0.8em;
  color: var(--accent);
}
.skill-tooltip .tooltip-text {
  visibility: hidden;
  background: #333;
  color: #fff;
  padding: 8px 12px;
  border-radius: 4px;
  position: absolute;
  z-index: 1000;
  width: 250px;
  left: 50%;
  transform: translateX(-50%);
  bottom: 125%;
  font-size: 12px;
  line-height: 1.4;
  opacity: 0;
  transition: opacity 0.2s;
}
.skill-tooltip:hover .tooltip-text,
.skill-tooltip:focus .tooltip-text {
  visibility: visible;
  opacity: 1;
}
```

### Rendering:
When rendering skill lists, append the tooltip after the skill name:
```js
function skillWithTooltip(name) {
  const desc = SKILL_DESCRIPTIONS[name] || SKILL_DESCRIPTIONS[name.split('(')[0].trim()];
  if (desc) {
    return `${name} <span class="skill-tooltip" tabindex="0">ℹ️<span class="tooltip-text">${desc}</span></span>`;
  }
  return name;
}
```

## Feature 3: "What does this mean in play?" Sidebars for Attributes

On Step 3 (Attributes), show each attribute with a plain-English explanation of what it means in actual gameplay. See the attribute explanations in Feature 1, Step 3 above — display these INLINE with each attribute value, not as a separate block.

Example layout for each attribute:
```html
<div class="attribute-card">
  <div class="attribute-name">Action Points</div>
  <div class="attribute-value">2</div>
  <div class="attribute-help">How many actions you get per combat round — attack, parry, cast a spell, or move.</div>
</div>
```

```css
.attribute-card {
  background: #f8f9fa;
  padding: 8px 12px;
  border-radius: 4px;
  margin: 4px 0;
}
.attribute-name { font-weight: bold; font-size: 0.85em; color: #666; }
.attribute-value { font-size: 1.4em; font-weight: bold; }
.attribute-help { font-size: 0.8em; color: #888; margin-top: 2px; }
```

## Feature 4: Suggested Builds per Culture

On Step 4 (Culture selection), when a culture is selected, show a "Suggested Builds" section with 2-3 character archetypes that work well with that culture. These are suggestions, not requirements.

### Data:
```js
const CULTURE_BUILDS = {
  "Praxian": [
    { name: "Beast Rider Warrior", stats: "High STR, CON", career: "Warrior", style: "Beast Rider Warrior", tip: "Mounted combat specialist. Lance charges and archery from the saddle." },
    { name: "Desert Shaman", stats: "High POW, INT", career: "Shaman", style: "Desert Skirmisher", tip: "Spirit talker who survives the wastes through cunning and magic." },
    { name: "Tribal Hunter", stats: "High DEX, CON", career: "Hunter", style: "Desert Skirmisher", tip: "Patient tracker and skirmisher. Javelin and sling from a distance." }
  ],
  "Sartarite/Heortling": [
    { name: "Orlanthi Thane", stats: "High STR, CHA", career: "Warrior", style: "Orlanthi Warrior", tip: "Sword-and-shield fighter who leads from the front." },
    { name: "Wind Lord Aspirant", stats: "High POW, STR", career: "Priest", style: "Thane's Guard", tip: "Devotee of Orlanth who combines martial prowess with divine magic." },
    { name: "Clan Skald", stats: "High CHA, INT", career: "Entertainer", style: "Orlanthi Warrior", tip: "Storyteller and musician who inspires the warband with tales of glory." }
  ],
  "Lunar Heartland": [
    { name: "Lunar Legionary", stats: "High STR, CON", career: "Warrior", style: "Lunar Legionary", tip: "Disciplined soldier in the Emperor's armies. Shield wall and scimitar." },
    { name: "Seven Mothers Priestess", stats: "High POW, CHA", career: "Priest", style: "Palace Guard", tip: "Devoted to the Red Goddess. Combines faith with political cunning." },
    { name: "Heartland Spy", stats: "High DEX, CHA", career: "Agent", style: "Noble Cavalry", tip: "Works in the shadows for the Lunar Empire. Charm and a hidden blade." }
  ],
  "Esrolian": [
    { name: "Earth Priestess", stats: "High POW, CHA", career: "Priest", style: "Clan Protector", tip: "Devoted to the Earth goddesses. Political power through the temples." },
    { name: "Citizen Soldier", stats: "High STR, CON", career: "Warrior", style: "Citizen Legionary", tip: "Formation fighter defending the city-states. Spear, shield, and discipline." },
    { name: "Temple Scholar", stats: "High INT, CHA", career: "Scholar", style: "City-State Phalangite", tip: "Esrolian intellectual. Knows more about Glorantha than most." }
  ],
  "Balazaring": [
    { name: "Hawk Hunter", stats: "High DEX, CON", career: "Hunter", style: "Hawk Slayer", tip: "Hunts with trained hawks in the wild hills. Expert with longspear." },
    { name: "Clan Raider", stats: "High STR, DEX", career: "Warrior", style: "Hunter Raider", tip: "Fast and vicious. Raids neighbouring clans for cattle and glory." }
  ],
  "Telmori Hsunchen": [
    { name: "Wolf Pack Alpha", stats: "High STR, POW", career: "Warrior", style: "Wolf Pack Hunter", tip: "Fights alongside wolves. Can shapeshift during the full moon." },
    { name: "Wolfbrother Shaman", stats: "High POW, INT", career: "Shaman", style: "Wolfbrother", tip: "Speaks to wolf spirits and the spirit of Telmor." }
  ]
};
```

### Rendering:
Display after culture details as a collapsible section:
```html
<div class="collapsible">
  <div class="collapsible-header" onclick="App.toggleCollapsible(this)">
    💡 Suggested Character Builds for [Culture]
  </div>
  <div class="collapsible-content hidden">
    [build cards here]
  </div>
</div>
```

Each build card:
```html
<div class="build-card">
  <div class="build-name">Beast Rider Warrior</div>
  <div class="build-detail">Stats: High STR, CON | Career: Warrior | Style: Beast Rider Warrior</div>
  <div class="build-tip">Mounted combat specialist. Lance charges and archery from the saddle.</div>
</div>
```

## Feature 5: Plain English Character Summary (Step 12)

On Step 12 (Review), generate a natural language paragraph describing the character based on their stats, skills, and background. This should read like a character introduction.

### Algorithm:
1. Get the character's top 5 skills (highest total value, excluding combat styles)
2. Get their combat styles
3. Get their highest characteristic
4. Get their passions
5. Generate a paragraph:

```js
App.generateCharacterSummary = function() {
  const char = CharacterData;
  // ... collect top skills, combat styles, passions
  
  // Example output:
  // "Wolf is a Lunar Heartland entertainer, aged 21. She's charming and 
  //  perceptive (Insight 122%), a gifted musician (Musicianship 116%), and 
  //  knows how to work a crowd (Influence 94%). In combat, she fights with 
  //  broadsword in the Lunar Legionary style. She's devoted to the Red 
  //  Goddess and fiercely loyal to the Red Emperor."
  
  return summary;
};
```

Display in a styled box at the top of Step 12:
```css
.character-summary {
  background: #f8f4e8;
  border: 1px solid #d4c9a8;
  padding: 15px 20px;
  border-radius: 6px;
  font-style: italic;
  font-size: 1.1em;
  line-height: 1.6;
  margin-bottom: 20px;
}
```

## Feature 6: Hit Location Body Diagram

Replace (or supplement) the hit location table with a simple SVG human silhouette showing HP and AP per location.

### SVG Approach:
Create a simple body outline SVG inline. Each body region is a `<path>` or `<rect>` with a `<text>` label showing HP/AP.

```html
<svg viewBox="0 0 200 400" width="150" class="body-diagram">
  <!-- Head -->
  <circle cx="100" cy="40" r="25" fill="#f0f0f0" stroke="#333"/>
  <text x="100" y="45" text-anchor="middle" font-size="11">5 HP</text>
  
  <!-- Chest -->
  <rect x="65" y="70" width="70" height="60" rx="5" fill="#f0f0f0" stroke="#333"/>
  <text x="100" y="105" text-anchor="middle" font-size="11">8 HP</text>
  
  <!-- Abdomen -->
  <rect x="70" y="135" width="60" height="40" rx="3" fill="#f0f0f0" stroke="#333"/>
  <text x="100" y="160" text-anchor="middle" font-size="11">7 HP</text>
  
  <!-- Arms -->
  <rect x="30" y="75" width="30" height="70" rx="5" fill="#f0f0f0" stroke="#333"/>
  <text x="45" y="115" text-anchor="middle" font-size="10">4 HP</text>
  <rect x="140" y="75" width="30" height="70" rx="5" fill="#f0f0f0" stroke="#333"/>
  <text x="155" y="115" text-anchor="middle" font-size="10">4 HP</text>
  
  <!-- Legs -->
  <rect x="70" y="180" width="25" height="90" rx="5" fill="#f0f0f0" stroke="#333"/>
  <text x="82" y="230" text-anchor="middle" font-size="10">6 HP</text>
  <rect x="105" y="180" width="25" height="90" rx="5" fill="#f0f0f0" stroke="#333"/>
  <text x="117" y="230" text-anchor="middle" font-size="10">6 HP</text>
</svg>
```

Generate this dynamically from `CharacterData.attributes.hitPoints`. Show both HP and AP (from armor) if armor is equipped.

Display this on:
- Step 3 (Attributes) — just HP values
- Play Mode — HP + AP from armor
- Print layout — HP + AP
- Pocketfold panel 3 — compact version alongside the table

## Testing
1. `python3 -m unittest tests.test_calculations -v` must pass
2. All new features should be visible in the wizard steps
3. Character summary should generate readable English
4. Body diagram should show correct HP values matching the table
5. Commit and push, do NOT merge
