// The single source of truth for all 7 Mission Days & Educational Data

export const AVATARS = [
  { id: 'male', emoji: '👨‍🚀', label: 'Cadet Leo' },
  { id: 'female', emoji: '👩‍🚀', label: 'Cadet Maya' },
  { id: 'neutral', emoji: '🧑‍🚀', label: 'Cadet Nova' },
  { id: 'robot', emoji: '🤖', label: 'Rover Bot' }
];

export const MISSION_DAYS = [
  {
    day: 1,
    title: "Restore Heat",
    subtitle: "Bring back the spare battery and reconnect the heater wires before temperature drops.",
    consequence: "Freezing Lunar Night (-130°C)",
    icon: "🔥",
    baseStatus: { power: "POWER LOW", powerLevel: 35, heater: "HEATER OFF", radiation: "NOMINAL" },
    knowledgeBubbles: [
      { id: 'airlock', icon: '🚪', title: 'Airlock', badge: 'Air Safety', fact: 'Airlocks equalize pressure so warm breathable oxygen stays inside the dome when you venture outside.' },
      { id: 'suitTimer', icon: '⏳', title: 'Suit Timer', badge: '10s Limit', fact: 'Night on the Moon drops to -130°C! Suit internal heaters only buy you about 10 seconds of safe exterior walk.' },
      { id: 'battery', icon: '🔋', title: 'Battery', badge: 'Backup Pack', fact: 'Reserve power packs are kept in external charging bays to prevent fire hazard inside astronaut quarters.' },
      { id: 'temperature', icon: '❄️', title: '-130°C Cold', badge: 'Extreme Lunar', fact: 'Without an atmosphere to hold heat, lunar night is twice as cold as Antarctica’s record low!' },
      { id: 'wires', icon: '🔌', title: 'Heater Grid', badge: 'Hab Life Support', fact: 'Connecting the heater relay restores interior warmth and protects living quarters from freezing shut.' }
    ],
    checklist: [
      { id: 'step1', label: 'Exit the station', done: true },
      { id: 'step2', label: 'Collect the battery', done: false, active: true },
      { id: 'step3', label: 'Return inside', done: false },
      { id: 'step4', label: 'Plug in the battery', done: false },
      { id: 'step5', label: 'Connect the heater wires', done: false }
    ],
    initialLogs: ['Suit checked', 'Airlock opened', 'Countdown started'],
    glossary: { term: 'AIRLOCK', definition: 'A room that keeps air inside the base when you go out.' },
    learningTakeaway: 'The heater needs power from the battery.'
  },
  {
    day: 2,
    title: "Clear Solar Dust",
    subtitle: "Lunar regolith dust is covering the solar array. Clear it safely!",
    consequence: "Dust Accumulation",
    icon: "☀️",
    baseStatus: { power: "POWER DROPPING", powerLevel: 45, heater: "HEATER ON", radiation: "NOMINAL" },
    knowledgeBubbles: [
      { id: 'regolith', icon: '🌑', title: 'Regolith Dust', badge: 'Sharp Glass', fact: 'Lunar dust has no wind or water to smooth it, so it is razor sharp and sticks with static!' },
      { id: 'solarArray', icon: '☀️', title: 'Solar Array', badge: 'Power Source', fact: 'Even a thin film of dust blocks up to 90% of solar energy collection!' },
      { id: 'wiper', icon: '🧹', title: 'Electro-Wiper', badge: 'Static Tech', fact: 'NASA designs electrostatic shields to repel dust without scratching solar glass panels.' },
      { id: 'efficiency', icon: '⚡', title: 'Power Output', badge: 'Solar Cells', fact: 'Keeping arrays clear ensures the habitat batteries charge to 100% before nightfall.' }
    ],
    checklist: [
      { id: 'd2_1', label: 'Grab electrostatic wiper', done: false, active: true },
      { id: 'd2_2', label: 'Exit to Solar Grid Alpha', done: false },
      { id: 'd2_3', label: 'Wipe 3 solar panels', done: false },
      { id: 'd2_4', label: 'Return inside airlock', done: false }
    ],
    initialLogs: ['Day 2 initiated', 'Solar telemetries nominal'],
    glossary: { term: 'REGOLITH', definition: 'The powdery, sharp dust layer that blankets the Moon.' },
    learningTakeaway: 'Solar panels need clean surfaces to generate electricity for life support.'
  },
  {
    day: 3,
    title: "Solar Storm Shield",
    subtitle: "High radiation alert! Deploy the lunar regolith shield over habitat dome.",
    consequence: "Solar Particle Event",
    icon: "🛡️",
    baseStatus: { power: "NORMAL", powerLevel: 75, heater: "ON", radiation: "HIGH RISK" },
    knowledgeBubbles: [
      { id: 'storm', icon: '☀️💥', title: 'Solar Flare', badge: 'Radiation', fact: 'Coronal mass ejections shoot high-speed protons that can damage biological cells.' },
      { id: 'shield', icon: '🛡️', title: 'Regolith Shield', badge: '75% Cut', fact: 'Piling 2 meters of lunar soil over the habitat cuts harmful cosmic radiation by 75%!' },
      { id: 'magnet', icon: '🧲', title: 'Magnetic Coil', badge: 'Deflector', fact: 'Electromagnetic deflectors push charged particles away from astronaut living quarters.' },
      { id: 'shelter', icon: '🕳️', title: 'Lava Tube', badge: 'Underground', fact: 'Natural lunar lava tubes provide natural radiation vaults for long-term crew refuge.' }
    ],
    checklist: [
      { id: 'd3_1', label: 'Sound habitat radiation horn', done: false, active: true },
      { id: 'd3_2', label: 'Power up electromagnetic coil', done: false },
      { id: 'd3_3', label: 'Seal storm blast shields', done: false }
    ],
    initialLogs: ['Day 3 initiated', 'Radiation sensors active'],
    glossary: { term: 'DONKI ALERT', definition: 'NASA space weather alert tracking coronal solar storms.' },
    learningTakeaway: 'Space radiation cannot be blocked 100%, but lunar soil shielding cuts risk dramatically.'
  },
  {
    day: 4,
    title: "Water Loop Recycle",
    subtitle: "Recycling pumps are clogged with ice crystals. Flush the urine & greywater loop.",
    consequence: "Water Loop Failure",
    icon: "💧",
    baseStatus: { power: "NORMAL", powerLevel: 80, heater: "ON", radiation: "NOMINAL" },
    knowledgeBubbles: [
      { id: 'loop', icon: '💧', title: '98% Recycling', badge: 'ISS Loop', fact: 'Astronauts recover up to 98% of all water from sweat, breath moisture, and recycled urine!' },
      { id: 'filter', icon: '🧪', title: 'Osmosis Filter', badge: 'Ultra-Pure', fact: 'Membrane osmosis purifies water down to molecular levels, making it cleaner than tap water.' },
      { id: 'pump', icon: '⚙️', title: 'Loop Pump', badge: 'Recirculation', fact: 'Continuous water flow prevents freezing in the exterior unheated lunar conduit pipes.' },
      { id: 'storage', icon: '🚰', title: 'Potable Tank', badge: 'Life Support', fact: 'Each astronaut requires 2.5 liters of clean hydration daily for peak cognitive performance.' }
    ],
    checklist: [{ id: 'd4_1', label: 'Purge ice valve', done: false, active: true }],
    initialLogs: ['Day 4 initiated'],
    glossary: { term: 'ECLSS', definition: 'Environmental Control and Life Support System.' },
    learningTakeaway: 'Water recycling is vital because carrying fresh water from Earth is heavy and expensive.'
  },
  {
    day: 5,
    title: "CO2 Scrubber Reset",
    subtitle: "Carbon dioxide levels are rising! Replace the chemical zeolite filter bed.",
    consequence: "High CO2 Levels",
    icon: "🔄",
    baseStatus: { power: "NORMAL", powerLevel: 80, heater: "ON", radiation: "NOMINAL" },
    knowledgeBubbles: [
      { id: 'co2', icon: '🔄', title: 'CO2 Scrubber', badge: '4.32 kg/d', fact: '4 astronauts exhale 4.32 kg of CO2 daily. Scrubbers prevent toxic gas buildup.' },
      { id: 'zeolite', icon: '🧱', title: 'Zeolite Mineral', badge: 'Porous Bed', fact: 'Zeolite minerals act like microscopic sponges that trap carbon dioxide molecules from the air.' },
      { id: 'oxygenRatio', icon: '🫧', title: '21% Oxygen', badge: 'Hab Atmosphere', fact: 'Maintaining 78% nitrogen and 21% oxygen prevents oxygen-toxicity and fire dangers.' },
      { id: 'alarm', icon: '🚨', title: 'Sensor Alarm', badge: 'PPM Threshold', fact: 'Sensors ring when CO2 exceeds 5000 ppm to alert engineers before drowsiness occurs.' }
    ],
    checklist: [{ id: 'd5_1', label: 'Swap zeolite canister', done: false, active: true }],
    initialLogs: ['Day 5 initiated'],
    glossary: { term: 'ZEOLITE', definition: 'A porous mineral filter that traps CO2 molecules.' },
    learningTakeaway: 'Fresh oxygen is only half the battle; scrubbing exhaled CO2 is equally critical.'
  },
  {
    day: 6,
    title: "Greenhouse Oxygen",
    subtitle: "Boost lighting and nutrient feed to accelerate strawberry & microgreen growth.",
    consequence: "Oxygen Consumption",
    icon: "🌱",
    baseStatus: { power: "NORMAL", powerLevel: 70, heater: "ON", radiation: "NOMINAL" },
    knowledgeBubbles: [
      { id: 'plants', icon: '🌱', title: 'Hydroponics', badge: 'Fresh Food', fact: 'Crops recycle CO2 into fresh oxygen while providing crew vitamins!' },
      { id: 'leds', icon: '💡', title: 'Grow Spectrum', badge: 'Red & Blue', fact: 'Special red and blue LED wavelengths stimulate plant chlorophyll without wasting heat energy.' },
      { id: 'roots', icon: '🌾', title: 'Aeroponics', badge: 'Mist Nutrients', fact: 'Spraying nutrient mist onto hanging roots saves 95% more water than traditional farming!' },
      { id: 'biomass', icon: '🍓', title: 'Fresh Harvest', badge: 'Crew Morale', fact: 'Fresh crunchy strawberries in space boost astronaut mood and immune health on long missions.' }
    ],
    checklist: [{ id: 'd6_1', label: 'Adjust grow light spectrum', done: false, active: true }],
    initialLogs: ['Day 6 initiated'],
    glossary: { term: 'HYDROPONICS', definition: 'Growing plants in mineral nutrient water without soil.' },
    learningTakeaway: 'Plants provide oxygen and fresh food, but demand stable water, nutrients, and power.'
  },
  {
    day: 7,
    title: "Rock Sample Excavation",
    subtitle: "Final clearance! Venture into Shackleton Crater and secure frozen water ice core samples.",
    consequence: "Mission Climax",
    icon: "🪨",
    baseStatus: { power: "OPTIMAL", powerLevel: 95, heater: "ON", radiation: "NOMINAL" },
    knowledgeBubbles: [
      { id: 'ice', icon: '🧊', title: 'Water Ice Core', badge: 'Shackleton', fact: 'Deep craters on the lunar South Pole hold frozen water trapped in permanent darkness for billions of years!' },
      { id: 'drill', icon: '⛏️', title: 'Percussive Drill', badge: '2m Depth', fact: 'Drilling into frozen regolith requires high-torque diamond bits to penetrate concrete-hard ice.' },
      { id: 'rover', icon: '🚜', title: 'Robotic Rover', badge: 'Autonomous', fact: 'Robotic rovers scout crater depths where temperatures drop to -246°C before humans enter.' },
      { id: 'rocketFuel', icon: '🚀', title: 'Liquid Propellant', badge: 'To Mars', fact: 'Splitting lunar water into hydrogen and oxygen will fuel spaceships heading to Mars and beyond!' }
    ],
    checklist: [{ id: 'd7_1', label: 'Drill core sample', done: false, active: true }],
    initialLogs: ['Day 7 initiated', 'EVA Moonwalk clearance active'],
    glossary: { term: 'VOLATILES', definition: 'Substances like water and methane that evaporate quickly in sunlight.' },
    learningTakeaway: 'Lunar water ice can be split into rocket fuel and oxygen for future trips to Mars.'
  }
];
