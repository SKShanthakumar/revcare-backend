CHENNAI_AREAS = [
    ("Adyar", 600020),
    ("Anna Nagar", 600040),
    ("T. Nagar", 600017),
    ("Velachery", 600042),
    ("Nungambakkam", 600034),
    ("Guindy", 600032),
    ("Kodambakkam", 600024),
    ("Tambaram", 600045),
    ("Perambur", 600011),
    ("Mylapore", 600004),
    ("Saidapet", 600015),
    ("Royapettah", 600014),
    ("Thiruvanmiyur", 600041),
    ("Kilpauk", 600010),
    ("Egmore", 600008),
    ("Purasawalkam", 600007),
    ("Madipakkam", 600091),
    ("Porur", 600116),
    ("Ambattur", 600053),
    ("Alandur", 600016),
    ("Chromepet", 600044),
    ("Pallavaram", 600043),
    ("Sholinganallur", 600119),
    ("Medavakkam", 600100),
    ("Thoraipakkam", 600097),
    ("Manapakkam", 600125),
    ("West Mambalam", 600033),
    ("Perungudi", 600096),
    ("Avadi", 600054),
    ("Koyambedu", 600107)
]

SERVICES_DATA = [
  {
    "title": "Basic Service",
    "description": "Essential maintenance package including oil change, filter inspection, and comprehensive vehicle checkup to keep your car running smoothly.",
    "category_id": 1,
    "works": [
      "Engine oil replacement with quality lubricant",
      "Oil filter inspection and replacement",
      "Air filter condition check",
      "General visual inspection of engine components",
      "Fluid level checks (brake, coolant, windshield washer)",
      "Tyre pressure check and adjustment",
      "Basic safety system verification"
    ],
    "symptoms": [
      "car needs regular maintenance",
      "service due light is on",
      "haven't serviced in long time",
      "engine sounds different than usual",
      "want to keep car in good condition",
      "planning long trip need checkup",
      "car feels sluggish lately",
      "preventive maintenance needed",
      "routine service required"
    ],
    "warranty_kms": 5000,
    "warranty_months": 3,
    "time_hrs": 1.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/basic-service-1.jpg",
      "https://example.com/images/services/basic-service-2.jpg",
      "https://example.com/images/services/basic-service-3.jpg"
    ]
  },
  {
    "title": "Standard Service",
    "description": "Comprehensive service package building on basic maintenance with added brake, battery, and cooling system checks for enhanced reliability.",
    "category_id": 1,
    "works": [
      "Complete basic service package",
      "Brake system inspection and pad thickness check",
      "Battery health test and terminal cleaning",
      "Coolant level check and top-up",
      "Brake fluid level verification",
      "Wiper blade condition assessment",
      "Undercarriage visual inspection",
      "Test drive for performance verification"
    ],
    "symptoms": [
      "want complete checkup of car",
      "car making some unusual noises",
      "brake pedal feels different",
      "battery seems weak lately",
      "car not starting smoothly",
      "need thorough inspection",
      "car performance decreased",
      "multiple small issues noticed",
      "want peace of mind before trip",
      "comprehensive service needed"
    ],
    "warranty_kms": 7500,
    "warranty_months": 4,
    "time_hrs": 2.5,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/standard-service-1.jpg",
      "https://example.com/images/services/standard-service-2.jpg",
      "https://example.com/images/services/standard-service-3.jpg"
    ]
  },
  {
    "title": "Comprehensive Service",
    "description": "Complete all-inclusive service package with advanced diagnostics, alignment, and vehicle washing for total peace of mind.",
    "category_id": 1,
    "works": [
      "Full standard service package",
      "Advanced engine diagnostics with computer scanning",
      "Wheel alignment and geometry check",
      "Suspension system inspection",
      "Exhaust system check for leaks",
      "Complete exterior and interior washing",
      "Detailed multi-point inspection report",
      "Road test with performance analysis"
    ],
    "symptoms": [
      "car needs complete overhaul",
      "want full diagnostic scan",
      "car pulling to one side",
      "multiple problems in car",
      "car not driving smoothly",
      "want everything checked thoroughly",
      "planning to sell need full service",
      "car feels unsafe to drive",
      "want detailed inspection report",
      "complete service package needed",
      "car needs attention badly"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 4.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/comprehensive-service-1.jpg",
      "https://example.com/images/services/comprehensive-service-2.jpg",
      "https://example.com/images/services/comprehensive-service-3.jpg"
    ]
  },
  {
    "title": "Oil Change",
    "description": "Quick and efficient engine oil and filter replacement service to maintain optimal engine lubrication and performance.",
    "category_id": 2,
    "works": [
      "Drain old engine oil completely",
      "Replace oil filter with genuine or equivalent part",
      "Fill with recommended grade engine oil",
      "Check for oil leaks around drain plug and filter",
      "Reset oil service indicator if applicable",
      "Dispose of old oil in environmentally safe manner"
    ],
    "symptoms": [
      "engine oil is dark and dirty",
      "engine making ticking noise",
      "oil change light is on",
      "engine running rough",
      "low pickup and acceleration",
      "engine feels hot",
      "burning smell from engine",
      "haven't changed oil in months",
      "oil level is low",
      "engine sounds louder than before"
    ],
    "warranty_kms": 5000,
    "warranty_months": 3,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/oil-change-1.jpg",
      "https://example.com/images/services/oil-change-2.jpg",
      "https://example.com/images/services/oil-change-3.jpg"
    ]
  },
  {
    "title": "Engine Tune-Up",
    "description": "Restore engine performance and efficiency through spark plug replacement, timing adjustment, and fuel system optimization.",
    "category_id": 2,
    "works": [
      "Inspect and replace spark plugs",
      "Check and adjust ignition timing",
      "Clean or replace air filter",
      "Inspect fuel injectors and clean if needed",
      "Check and adjust idle speed",
      "Test engine compression",
      "Verify throttle response and adjust cables"
    ],
    "symptoms": [
      "engine misfiring frequently",
      "poor fuel economy",
      "engine stuttering when accelerating",
      "rough idle and shaking",
      "difficulty starting engine",
      "engine hesitates when pressing gas",
      "loss of power on highway",
      "engine backfiring",
      "check engine light on",
      "poor acceleration response",
      "engine running on only few cylinders"
    ],
    "warranty_kms": 15000,
    "warranty_months": 6,
    "time_hrs": 2.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/engine-tune-up-1.jpg",
      "https://example.com/images/services/engine-tune-up-2.jpg",
      "https://example.com/images/services/engine-tune-up-3.jpg"
    ]
  },
  {
    "title": "Engine Diagnostics & Repair",
    "description": "Advanced computerized diagnostics to identify and resolve engine performance issues, warning lights, and mechanical problems.",
    "category_id": 2,
    "works": [
      "Connect diagnostic scanner to ECU",
      "Read and interpret fault codes",
      "Perform sensor testing and verification",
      "Check engine mechanical condition",
      "Test fuel system pressure and flow",
      "Verify ignition system operation",
      "Clear codes and test drive for verification",
      "Provide detailed diagnostic report"
    ],
    "symptoms": [
      "check engine light came on",
      "engine warning light flashing",
      "engine making strange knocking sound",
      "car won't start properly",
      "engine cutting out while driving",
      "loss of power suddenly",
      "engine overheating frequently",
      "smoke coming from engine",
      "weird smell from engine bay",
      "engine running very rough",
      "multiple warning lights on dashboard",
      "engine sounds like something broken"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 3.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/engine-diagnostics-1.jpg",
      "https://example.com/images/services/engine-diagnostics-2.jpg",
      "https://example.com/images/services/engine-diagnostics-3.jpg"
    ]
  },
  {
    "title": "Timing Belt/Chain Replacement",
    "description": "Critical preventive maintenance replacing timing belt or chain to prevent catastrophic engine damage and ensure proper valve timing.",
    "category_id": 2,
    "works": [
      "Remove engine covers and accessories",
      "Lock engine in correct timing position",
      "Remove old timing belt or chain",
      "Inspect and replace tensioners and guides",
      "Replace water pump if driven by timing belt",
      "Install new timing belt/chain with proper tension",
      "Verify correct timing marks alignment",
      "Reassemble and test engine operation"
    ],
    "symptoms": [
      "ticking noise from front of engine",
      "car has done 60000 km",
      "rattling sound on startup",
      "timing belt replacement due",
      "engine making whining noise",
      "mechanic said belt looks worn",
      "preventive replacement needed",
      "engine vibration increased",
      "squealing noise from engine",
      "reached timing belt change interval"
    ],
    "warranty_kms": 60000,
    "warranty_months": 24,
    "time_hrs": 5.0,
    "difficulty": 5,
    "images": [
      "https://example.com/images/services/timing-belt-replacement-1.jpg",
      "https://example.com/images/services/timing-belt-replacement-2.jpg",
      "https://example.com/images/services/timing-belt-replacement-3.jpg"
    ]
  },
  {
    "title": "Cooling System Service",
    "description": "Complete cooling system maintenance including radiator service, coolant flush, and component inspection to prevent overheating.",
    "category_id": 2,
    "works": [
      "Pressure test cooling system for leaks",
      "Drain old coolant completely",
      "Flush radiator and cooling passages",
      "Inspect radiator, hoses, and clamps",
      "Check water pump operation",
      "Test thermostat function",
      "Refill with proper coolant mixture",
      "Bleed air from cooling system"
    ],
    "symptoms": [
      "engine overheating in traffic",
      "temperature gauge going up",
      "coolant leaking under car",
      "heater not working properly",
      "steam coming from hood",
      "coolant warning light on",
      "engine getting too hot",
      "radiator fan not working",
      "coolant level keeps dropping",
      "sweet smell from engine",
      "white smoke from exhaust"
    ],
    "warranty_kms": 20000,
    "warranty_months": 12,
    "time_hrs": 2.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/cooling-system-service-1.jpg",
      "https://example.com/images/services/cooling-system-service-2.jpg",
      "https://example.com/images/services/cooling-system-service-3.jpg"
    ]
  },
  {
    "title": "Brake Pad Replacement",
    "description": "Replace worn brake pads with quality components to restore braking performance and ensure safe stopping power.",
    "category_id": 3,
    "works": [
      "Remove wheels for brake access",
      "Inspect brake disc condition and thickness",
      "Remove worn brake pads",
      "Clean and lubricate caliper slides",
      "Install new brake pads with anti-squeal shims",
      "Compress caliper pistons properly",
      "Test brake pedal feel and firmness",
      "Road test for proper braking performance"
    ],
    "symptoms": [
      "brakes making squealing noise",
      "grinding sound when braking",
      "brake pedal goes down too far",
      "car takes longer to stop",
      "vibration when applying brakes",
      "brake warning light came on",
      "screeching noise from wheels",
      "brakes feel weak",
      "brake pedal feels spongy",
      "metal sound when braking",
      "dust on wheels constantly"
    ],
    "warranty_kms": 20000,
    "warranty_months": 12,
    "time_hrs": 1.5,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/brake-pad-replacement-1.jpg",
      "https://example.com/images/services/brake-pad-replacement-2.jpg",
      "https://example.com/images/services/brake-pad-replacement-3.jpg"
    ]
  },
  {
    "title": "Brake Disc/Drum Resurfacing",
    "description": "Machine brake discs or drums to restore smooth surface, eliminate vibration, and extend brake component life.",
    "category_id": 3,
    "works": [
      "Remove brake discs or drums from vehicle",
      "Measure disc/drum thickness and runout",
      "Machine surfaces to manufacturer specifications",
      "Check for cracks or heat damage",
      "Clean and degrease machined surfaces",
      "Reinstall discs/drums with proper torque",
      "Bed-in new brake pads if installed",
      "Verify smooth braking operation"
    ],
    "symptoms": [
      "steering wheel shakes when braking",
      "pulsating brake pedal",
      "vibration at high speed braking",
      "brake discs look damaged",
      "uneven braking feeling",
      "car shudders when stopping",
      "brake pedal pulsates",
      "grinding marks on disc",
      "brake performance inconsistent",
      "wobbling sensation when braking"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 2.5,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/brake-disc-resurfacing-1.jpg",
      "https://example.com/images/services/brake-disc-resurfacing-2.jpg",
      "https://example.com/images/services/brake-disc-resurfacing-3.jpg"
    ]
  },
  {
    "title": "Brake Fluid Replacement",
    "description": "Replace old brake fluid to maintain hydraulic pressure, prevent corrosion, and ensure responsive brake pedal feel.",
    "category_id": 3,
    "works": [
      "Test brake fluid moisture content",
      "Extract old brake fluid from reservoir",
      "Bleed brake fluid from all four wheels",
      "Flush system with new DOT-spec fluid",
      "Remove air bubbles from brake lines",
      "Top up reservoir to correct level",
      "Test brake pedal firmness",
      "Check for leaks at all connections"
    ],
    "symptoms": [
      "brake pedal feels soft",
      "brake pedal goes to floor",
      "spongy brake feel",
      "brake fluid looks dark",
      "brake fluid level low",
      "brakes not responding quickly",
      "brake pedal sinking slowly",
      "have to pump brakes to stop",
      "brake fluid dirty and old",
      "brake performance reduced"
    ],
    "warranty_kms": 30000,
    "warranty_months": 24,
    "time_hrs": 1.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/brake-fluid-replacement-1.jpg",
      "https://example.com/images/services/brake-fluid-replacement-2.jpg",
      "https://example.com/images/services/brake-fluid-replacement-3.jpg"
    ]
  },
  {
    "title": "ABS Check & Repair",
    "description": "Diagnose and repair Anti-lock Braking System issues to restore optimal braking control and safety in emergency stops.",
    "category_id": 3,
    "works": [
      "Scan ABS system for fault codes",
      "Test ABS wheel speed sensors",
      "Inspect ABS wiring and connections",
      "Check ABS hydraulic unit operation",
      "Test ABS pump and motor function",
      "Verify brake pressure distribution",
      "Clear fault codes and calibrate system",
      "Road test ABS activation"
    ],
    "symptoms": [
      "ABS light on dashboard",
      "ABS warning light stays on",
      "brakes locking up suddenly",
      "pulsating pedal in emergency stop",
      "ABS not working properly",
      "brake light and ABS light both on",
      "grinding noise from ABS pump",
      "wheels locking when braking hard",
      "ABS activating unnecessarily",
      "traction control light also on"
    ],
    "warranty_kms": 20000,
    "warranty_months": 12,
    "time_hrs": 2.5,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/abs-check-repair-1.jpg",
      "https://example.com/images/services/abs-check-repair-2.jpg",
      "https://example.com/images/services/abs-check-repair-3.jpg"
    ]
  },
  {
    "title": "Complete Brake Overhaul",
    "description": "Comprehensive brake system restoration including all components for maximum safety and like-new braking performance.",
    "category_id": 3,
    "works": [
      "Replace all brake pads and shoes",
      "Resurface or replace all discs and drums",
      "Rebuild or replace brake calipers",
      "Replace brake fluid completely",
      "Install new brake hoses if worn",
      "Replace brake hardware and springs",
      "Adjust parking brake mechanism",
      "Perform complete system testing"
    ],
    "symptoms": [
      "brakes completely worn out",
      "car not stopping properly",
      "all brakes need replacement",
      "brake system very old",
      "multiple brake problems",
      "dangerous braking condition",
      "brake failure risk",
      "complete brake renovation needed",
      "brake system overhaul required",
      "brakes totally ineffective",
      "unsafe to drive due to brakes"
    ],
    "warranty_kms": 30000,
    "warranty_months": 18,
    "time_hrs": 5.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/brake-overhaul-1.jpg",
      "https://example.com/images/services/brake-overhaul-2.jpg",
      "https://example.com/images/services/brake-overhaul-3.jpg"
    ]
  },
  {
    "title": "Clutch Plate Replacement",
    "description": "Replace worn clutch plate, pressure plate, and release bearing to restore smooth engagement and eliminate slipping.",
    "category_id": 4,
    "works": [
      "Remove transmission from engine",
      "Inspect flywheel surface condition",
      "Remove old clutch pressure plate and disc",
      "Install new clutch disc with alignment tool",
      "Install new pressure plate with proper torque",
      "Replace release bearing and fork",
      "Reinstall transmission with new pilot bearing",
      "Adjust clutch pedal free play",
      "Road test clutch engagement"
    ],
    "symptoms": [
      "clutch slipping in high gear",
      "burning smell when driving",
      "difficulty changing gears",
      "clutch pedal very hard to press",
      "car not moving despite accelerating",
      "RPM going up but speed not increasing",
      "clutch engaging at top of pedal",
      "grinding noise when changing gear",
      "clutch vibrating when engaging",
      "car jerking when releasing clutch",
      "clutch pedal staying on floor"
    ],
    "warranty_kms": 40000,
    "warranty_months": 18,
    "time_hrs": 6.0,
    "difficulty": 5,
    "images": [
      "https://example.com/images/services/clutch-plate-replacement-1.jpg",
      "https://example.com/images/services/clutch-plate-replacement-2.jpg",
      "https://example.com/images/services/clutch-plate-replacement-3.jpg"
    ]
  },
  {
    "title": "Transmission Fluid Change",
    "description": "Replace transmission fluid and filter to ensure smooth shifting, reduce wear, and extend transmission life.",
    "category_id": 4,
    "works": [
      "Drain old transmission fluid",
      "Remove and clean transmission pan",
      "Replace transmission filter and gasket",
      "Clean magnet in transmission pan",
      "Reinstall pan with new gasket",
      "Refill with manufacturer-specified fluid",
      "Check for leaks after service",
      "Test drive for smooth shifting"
    ],
    "symptoms": [
      "gear shifting rough",
      "transmission jerking",
      "grinding when changing gears",
      "delayed gear engagement",
      "transmission slipping between gears",
      "hard to shift gears",
      "transmission fluid dark and burnt",
      "whining noise from gearbox",
      "transmission hesitating",
      "gear changes not smooth"
    ],
    "warranty_kms": 40000,
    "warranty_months": 24,
    "time_hrs": 1.5,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/transmission-fluid-change-1.jpg",
      "https://example.com/images/services/transmission-fluid-change-2.jpg",
      "https://example.com/images/services/transmission-fluid-change-3.jpg"
    ]
  },
  {
    "title": "Gearbox Repair/Overhaul",
    "description": "Complete gearbox disassembly, inspection, and rebuild to resolve shifting issues and restore transmission function.",
    "category_id": 4,
    "works": [
      "Remove gearbox from vehicle",
      "Disassemble and clean all components",
      "Inspect gears, bearings, and synchronizers",
      "Replace worn or damaged parts",
      "Install new seals and gaskets",
      "Reassemble with proper shimming",
      "Fill with correct transmission oil",
      "Test shift quality on dynamometer",
      "Reinstall and road test"
    ],
    "symptoms": [
      "gears popping out",
      "cannot shift into certain gear",
      "transmission making loud noise",
      "gear grinding every time",
      "stuck in one gear",
      "gearbox leaking oil badly",
      "cannot get into reverse",
      "transmission completely failed",
      "gears slipping out while driving",
      "major gearbox problem",
      "transmission not working at all",
      "mechanic said gearbox needs rebuild"
    ],
    "warranty_kms": 50000,
    "warranty_months": 24,
    "time_hrs": 12.0,
    "difficulty": 5,
    "images": [
      "https://example.com/images/services/gearbox-overhaul-1.jpg",
      "https://example.com/images/services/gearbox-overhaul-2.jpg",
      "https://example.com/images/services/gearbox-overhaul-3.jpg"
    ]
  },
  {
    "title": "Flywheel Repair/Replacement",
    "description": "Resurface or replace flywheel to eliminate clutch chatter, vibration, and ensure smooth power transfer.",
    "category_id": 4,
    "works": [
      "Remove transmission and clutch assembly",
      "Remove flywheel bolts with proper sequence",
      "Inspect flywheel for cracks and hot spots",
      "Machine flywheel surface or install new unit",
      "Install flywheel with thread locker",
      "Torque bolts to manufacturer specifications",
      "Install new clutch components",
      "Reassemble transmission and test"
    ],
    "symptoms": [
      "clutch chattering badly",
      "vibration when starting from stop",
      "juddering when engaging clutch",
      "burning smell even after new clutch",
      "clutch pedal vibrating",
      "rough engagement of clutch",
      "car shaking when releasing clutch",
      "noise when clutch is pressed",
      "flywheel damaged according to mechanic",
      "clutch not working smooth after replacement"
    ],
    "warranty_kms": 50000,
    "warranty_months": 24,
    "time_hrs": 7.0,
    "difficulty": 5,
    "images": [
      "https://example.com/images/services/flywheel-replacement-1.jpg",
      "https://example.com/images/services/flywheel-replacement-2.jpg",
      "https://example.com/images/services/flywheel-replacement-3.jpg"
    ]
  },
  {
    "title": "Hydraulic Clutch System Service",
    "description": "Service clutch master and slave cylinders, bleed system, and restore proper hydraulic clutch operation.",
    "category_id": 4,
    "works": [
      "Inspect clutch master cylinder for leaks",
      "Check slave cylinder operation",
      "Bleed hydraulic clutch system",
      "Replace clutch fluid if contaminated",
      "Test clutch pedal feel and travel",
      "Adjust clutch engagement point if possible",
      "Check for air in hydraulic lines",
      "Road test clutch response"
    ],
    "symptoms": [
      "clutch pedal soft and spongy",
      "clutch pedal goes to floor",
      "difficulty pressing clutch",
      "clutch fluid leaking",
      "clutch not disengaging properly",
      "hard to get into gear",
      "clutch pedal has no pressure",
      "grinding when shifting with clutch pressed",
      "clutch pedal stuck down",
      "clutch engagement point changed"
    ],
    "warranty_kms": 20000,
    "warranty_months": 12,
    "time_hrs": 1.5,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/hydraulic-clutch-service-1.jpg",
      "https://example.com/images/services/hydraulic-clutch-service-2.jpg",
      "https://example.com/images/services/hydraulic-clutch-service-3.jpg"
    ]
  },
  {
    "title": "Shock Absorber Replacement",
    "description": "Replace worn shock absorbers to restore ride comfort, handling stability, and tire contact with road surface.",
    "category_id": 5,
    "works": [
      "Lift vehicle and support safely",
      "Remove wheels for access",
      "Disconnect shock absorber mounting bolts",
      "Remove old shock absorbers",
      "Install new shock absorbers with bushings",
      "Torque mounting bolts to specification",
      "Check suspension geometry",
      "Road test for ride quality improvement"
    ],
    "symptoms": [
      "car bouncing too much on bumps",
      "bottoming out on speed breakers",
      "nose diving when braking",
      "car swaying in corners",
      "excessive body roll",
      "rear end squatting when accelerating",
      "bumpy uncomfortable ride",
      "car keeps bouncing after bump",
      "suspension feels too soft",
      "knocking sound from suspension",
      "oil leaking from shocks"
    ],
    "warranty_kms": 30000,
    "warranty_months": 18,
    "time_hrs": 2.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/shock-absorber-replacement-1.jpg",
      "https://example.com/images/services/shock-absorber-replacement-2.jpg",
      "https://example.com/images/services/shock-absorber-replacement-3.jpg"
    ]
  },
  {
    "title": "Wheel Alignment",
    "description": "Precise adjustment of wheel angles to manufacturer specifications for even tire wear and straight tracking.",
    "category_id": 5,
    "works": [
      "Mount vehicle on alignment rack",
      "Attach alignment sensors to wheels",
      "Measure current alignment angles",
      "Adjust camber, caster, and toe settings",
      "Verify steering wheel centering",
      "Recheck all alignment specifications",
      "Print alignment report with before/after",
      "Test drive for straight tracking"
    ],
    "symptoms": [
      "car pulling to left",
      "car pulling to right",
      "steering wheel not centered",
      "steering wheel crooked when driving straight",
      "uneven tire wear",
      "car drifting on straight road",
      "steering feels loose",
      "vibration at high speed",
      "tires wearing on one side",
      "car veering to side",
      "have to hold steering to keep straight",
      "front tires wearing fast"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 1.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/wheel-alignment-1.jpg",
      "https://example.com/images/services/wheel-alignment-2.jpg",
      "https://example.com/images/services/wheel-alignment-3.jpg"
    ]
  },
  {
    "title": "Steering Rack & Pinion Repair",
    "description": "Repair or replace steering rack to eliminate play, leaks, and ensure precise steering response.",
    "category_id": 5,
    "works": [
      "Disconnect steering column from rack",
      "Remove tie rod ends from knuckles",
      "Unbolt steering rack from subframe",
      "Remove or rebuild steering rack",
      "Install new seals and bushings",
      "Reinstall rack with proper alignment",
      "Reconnect tie rods and steering column",
      "Refill power steering fluid",
      "Perform wheel alignment check"
    ],
    "symptoms": [
      "steering very loose and vague",
      "clunking when turning steering",
      "power steering fluid leaking",
      "steering wheel play excessive",
      "grinding noise when turning",
      "steering hard to turn",
      "knocking sound from front when steering",
      "steering wandering on highway",
      "steering feels disconnected",
      "loud noise when turning full lock",
      "steering rack making noise"
    ],
    "warranty_kms": 40000,
    "warranty_months": 18,
    "time_hrs": 4.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/steering-rack-repair-1.jpg",
      "https://example.com/images/services/steering-rack-repair-2.jpg",
      "https://example.com/images/services/steering-rack-repair-3.jpg"
    ]
  },
  {
    "title": "Suspension Bush Replacement",
    "description": "Replace worn suspension bushings to reduce noise, improve handling, and restore suspension geometry.",
    "category_id": 5,
    "works": [
      "Identify worn or damaged bushings",
      "Support suspension components safely",
      "Press out old rubber bushings",
      "Clean bushing housings thoroughly",
      "Press in new polyurethane or rubber bushings",
      "Reinstall suspension components",
      "Torque bolts with suspension loaded",
      "Check alignment after installation"
    ],
    "symptoms": [
      "clunking noise from suspension",
      "knocking sound over bumps",
      "rattling from underneath car",
      "suspension making noise when turning",
      "squeaking from suspension",
      "car handling feels loose",
      "vibration through steering wheel",
      "banging noise from front",
      "car feels unstable in corners",
      "creaking noise when going over bumps"
    ],
    "warranty_kms": 30000,
    "warranty_months": 18,
    "time_hrs": 3.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/suspension-bush-replacement-1.jpg",
      "https://example.com/images/services/suspension-bush-replacement-2.jpg",
      "https://example.com/images/services/suspension-bush-replacement-3.jpg"
    ]
  },
  {
    "title": "Power Steering Fluid Check/Refill",
    "description": "Inspect power steering system, check fluid condition, and refill to ensure smooth and effortless steering.",
    "category_id": 5,
    "works": [
      "Check power steering fluid level",
      "Inspect fluid color and condition",
      "Look for leaks in hoses and connections",
      "Top up with manufacturer-specified fluid",
      "Check power steering pump operation",
      "Test steering effort at idle and driving",
      "Verify no whining or groaning noises"
    ],
    "symptoms": [
      "steering hard to turn",
      "whining noise when turning",
      "groaning sound from steering",
      "steering heavy at low speed",
      "power steering not working",
      "squealing when turning wheel",
      "steering stiff in morning",
      "power steering fluid low",
      "hard steering especially when parking"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/power-steering-fluid-1.jpg",
      "https://example.com/images/services/power-steering-fluid-2.jpg",
      "https://example.com/images/services/power-steering-fluid-3.jpg"
    ]
  },
  {
    "title": "Battery Check & Replacement",
    "description": "Test battery health, charging system, and replace battery if needed to ensure reliable starting and electrical power.",
    "category_id": 6,
    "works": [
      "Test battery voltage and load capacity",
      "Check battery terminals for corrosion",
      "Test alternator charging output",
      "Inspect battery cables and connections",
      "Remove old battery if replacement needed",
      "Install new battery with proper securing",
      "Apply terminal protection spray",
      "Reset vehicle systems if required"
    ],
    "symptoms": [
      "car not starting",
      "engine cranking slowly",
      "battery light on dashboard",
      "dim headlights",
      "clicking sound when starting",
      "have to jump start every time",
      "battery keeps dying",
      "electrical issues in car",
      "weak cranking sound",
      "battery is old and weak",
      "car won't start in morning",
      "dashboard lights flickering"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/battery-replacement-1.jpg",
      "https://example.com/images/services/battery-replacement-2.jpg",
      "https://example.com/images/services/battery-replacement-3.jpg"
    ]
  },
  {
    "title": "Alternator & Starter Motor Repair",
    "description": "Diagnose and repair charging and starting system issues to ensure reliable engine starting and electrical power generation.",
    "category_id": 6,
    "works": [
      "Test alternator output voltage and amperage",
      "Check starter motor current draw",
      "Remove faulty alternator or starter",
      "Disassemble and inspect internal components",
      "Replace brushes, bearings, or solenoid",
      "Test rebuilt unit on bench",
      "Reinstall and test charging/starting",
      "Verify proper belt tension"
    ],
    "symptoms": [
      "battery light stays on",
      "battery draining while driving",
      "starter motor not working",
      "grinding noise when starting",
      "alternator making noise",
      "electrical system not charging",
      "lights dimming while driving",
      "smell from alternator area",
      "starter just clicks",
      "engine won't crank",
      "new battery dies quickly",
      "whining noise from engine bay"
    ],
    "warranty_kms": 25000,
    "warranty_months": 12,
    "time_hrs": 3.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/alternator-starter-repair-1.jpg",
      "https://example.com/images/services/alternator-starter-repair-2.jpg",
      "https://example.com/images/services/alternator-starter-repair-3.jpg"
    ]
  },
  {
    "title": "Headlight & Indicator Replacement",
    "description": "Replace damaged or burnt-out headlight and indicator bulbs to ensure safe visibility and legal compliance.",
    "category_id": 6,
    "works": [
      "Access headlight or indicator housing",
      "Remove old bulb carefully",
      "Check electrical connector condition",
      "Install new bulb without touching glass",
      "Test light operation and alignment",
      "Adjust headlight aim if necessary",
      "Verify all indicators flash properly"
    ],
    "symptoms": [
      "headlight not working",
      "dim headlights",
      "one headlight out",
      "indicator not blinking",
      "turn signal not working",
      "bulb blown",
      "headlight very weak",
      "indicator blinking fast",
      "both headlights dim",
      "got stopped by police for light"
    ],
    "warranty_kms": 5000,
    "warranty_months": 6,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/headlight-replacement-1.jpg",
      "https://example.com/images/services/headlight-replacement-2.jpg",
      "https://example.com/images/services/headlight-replacement-3.jpg"
    ]
  },
  {
    "title": "ECU Diagnostics",
    "description": "Advanced electronic control unit diagnostics to identify sensor failures, communication errors, and system malfunctions.",
    "category_id": 6,
    "works": [
      "Connect professional diagnostic scanner",
      "Read fault codes from all control modules",
      "Perform live data monitoring",
      "Test sensor inputs and outputs",
      "Check ECU power and ground circuits",
      "Verify communication between modules",
      "Clear codes and monitor for recurrence",
      "Provide detailed diagnostic report"
    ],
    "symptoms": [
      "check engine light on",
      "multiple warning lights on",
      "car going into limp mode",
      "engine management light flashing",
      "car not performing properly",
      "electronic problems in car",
      "computer showing errors",
      "sensor malfunction suspected",
      "need diagnostic scan",
      "car behaving strangely",
      "warning lights appearing randomly",
      "electronic fault detected"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 2.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/ecu-diagnostics-1.jpg",
      "https://example.com/images/services/ecu-diagnostics-2.jpg",
      "https://example.com/images/services/ecu-diagnostics-3.jpg"
    ]
  },
  {
    "title": "Wiring & Fuse Repair",
    "description": "Locate and repair electrical wiring faults, replace blown fuses, and restore proper electrical circuit function.",
    "category_id": 6,
    "works": [
      "Identify electrical circuit fault location",
      "Check fuse box for blown fuses",
      "Trace wiring with multimeter",
      "Repair damaged or corroded wiring",
      "Install proper gauge replacement wire",
      "Solder and heat shrink connections",
      "Replace fuses with correct amperage",
      "Test circuit operation thoroughly"
    ],
    "symptoms": [
      "fuse keeps blowing",
      "electrical short circuit",
      "some lights not working",
      "accessory stopped working",
      "burning smell from wiring",
      "intermittent electrical problem",
      "power windows not working",
      "central locking failed",
      "radio not turning on",
      "electrical fault suspected",
      "wiring issue somewhere"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 2.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/wiring-fuse-repair-1.jpg",
      "https://example.com/images/services/wiring-fuse-repair-2.jpg",
      "https://example.com/images/services/wiring-fuse-repair-3.jpg"
    ]
  },
  {
    "title": "AC Gas Refill",
    "description": "Recharge air conditioning system with refrigerant and oil to restore cold air output and comfort.",
    "category_id": 7,
    "works": [
      "Recover remaining refrigerant safely",
      "Vacuum air conditioning system",
      "Check for leaks with UV dye or detector",
      "Add required amount of PAG oil",
      "Recharge with correct refrigerant type and amount",
      "Test system pressures and temperatures",
      "Verify cold air output at vents"
    ],
    "symptoms": [
      "AC not cooling",
      "AC blowing warm air",
      "AC not cold enough",
      "AC takes long time to cool",
      "AC cooling reduced",
      "AC gas finished",
      "need AC gas refill",
      "AC compressor running but no cooling",
      "AC only cool at high speed",
      "AC stopped working suddenly"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 1.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/ac-gas-refill-1.jpg",
      "https://example.com/images/services/ac-gas-refill-2.jpg",
      "https://example.com/images/services/ac-gas-refill-3.jpg"
    ]
  },
  {
    "title": "AC Compressor Repair",
    "description": "Repair or replace faulty AC compressor to restore air conditioning system operation and cooling capacity.",
    "category_id": 7,
    "works": [
      "Recover refrigerant from system",
      "Remove serpentine belt",
      "Disconnect AC lines from compressor",
      "Unbolt and remove old compressor",
      "Install new or rebuilt compressor",
      "Replace AC receiver/drier or accumulator",
      "Evacuate and recharge system",
      "Test AC operation and temperature",
      "Check for leaks at all connections"
    ],
    "symptoms": [
      "AC compressor not working",
      "loud noise from AC compressor",
      "AC clutch not engaging",
      "squealing when AC turned on",
      "AC compressor seized",
      "grinding noise when AC on",
      "AC compressor leaking oil",
      "AC belt keeps breaking",
      "rattling noise from AC",
      "AC compressor smoking",
      "burning smell when AC on"
    ],
    "warranty_kms": 20000,
    "warranty_months": 12,
    "time_hrs": 3.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/ac-compressor-repair-1.jpg",
      "https://example.com/images/services/ac-compressor-repair-2.jpg",
      "https://example.com/images/services/ac-compressor-repair-3.jpg"
    ]
  },
  {
    "title": "AC Filter Cleaning/Replacement",
    "description": "Clean or replace cabin air filter to improve air quality, airflow, and eliminate odors from ventilation system.",
    "category_id": 7,
    "works": [
      "Locate cabin air filter access point",
      "Remove old filter from housing",
      "Clean filter housing if dirty",
      "Install new cabin air filter",
      "Ensure proper filter orientation",
      "Test airflow improvement",
      "Check for air leaks around filter"
    ],
    "symptoms": [
      "bad smell from AC",
      "musty odor from vents",
      "weak airflow from AC",
      "AC vents blowing less air",
      "dust coming from AC",
      "allergies when AC on",
      "foul smell in car",
      "reduced air from vents",
      "AC filter never changed",
      "dirty smell from AC"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/ac-filter-replacement-1.jpg",
      "https://example.com/images/services/ac-filter-replacement-2.jpg",
      "https://example.com/images/services/ac-filter-replacement-3.jpg"
    ]
  },
  {
    "title": "Heater/Blower Repair",
    "description": "Repair heater core, blower motor, or related components to restore cabin heating and ventilation function.",
    "category_id": 7,
    "works": [
      "Diagnose heater/blower malfunction",
      "Test blower motor operation",
      "Check heater core for blockage or leaks",
      "Inspect blend door actuator function",
      "Replace faulty blower motor or resistor",
      "Flush heater core if restricted",
      "Test all fan speeds and temperature control",
      "Verify proper air distribution"
    ],
    "symptoms": [
      "blower not working",
      "no air from vents",
      "heater not blowing hot",
      "fan only works on high speed",
      "blower making noise",
      "sweet smell in cabin",
      "windshield fogging up",
      "heater blowing cold air",
      "blower motor squealing",
      "no hot air in winter",
      "fan speed not changing"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 2.5,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/heater-blower-repair-1.jpg",
      "https://example.com/images/services/heater-blower-repair-2.jpg",
      "https://example.com/images/services/heater-blower-repair-3.jpg"
    ]
  },
  {
    "title": "Leak Detection & Fix",
    "description": "Locate and repair AC system refrigerant leaks to prevent gas loss and ensure long-term cooling performance.",
    "category_id": 7,
    "works": [
      "Add UV dye to AC system",
      "Operate AC system to circulate dye",
      "Inspect all AC components with UV light",
      "Use electronic leak detector for confirmation",
      "Repair or replace leaking components",
      "Evacuate system completely",
      "Recharge with proper refrigerant amount",
      "Verify system holds pressure"
    ],
    "symptoms": [
      "AC gas leaking",
      "AC gas finishing quickly",
      "need AC refill every month",
      "AC cooling decreases gradually",
      "oily residue near AC components",
      "hissing sound from AC",
      "AC stops cooling after few days",
      "AC gas not lasting",
      "refrigerant leak suspected",
      "AC needs constant recharge"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 2.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/ac-leak-detection-1.jpg",
      "https://example.com/images/services/ac-leak-detection-2.jpg",
      "https://example.com/images/services/ac-leak-detection-3.jpg"
    ]
  },
  {
    "title": "Wheel Alignment",
    "description": "Precision alignment of all wheels to manufacturer specifications for optimal handling, tire wear, and fuel efficiency.",
    "category_id": 8,
    "works": [
      "Mount vehicle on computerized alignment rack",
      "Attach alignment targets to all wheels",
      "Measure current camber, caster, and toe",
      "Adjust front and rear alignment angles",
      "Center steering wheel position",
      "Verify thrust angle is correct",
      "Print detailed alignment report",
      "Test drive for straight tracking"
    ],
    "symptoms": [
      "car pulling to one side",
      "steering wheel off center",
      "tires wearing unevenly",
      "car drifts when hands off wheel",
      "steering not straight",
      "uneven tire tread",
      "car veers to left or right",
      "front end alignment needed",
      "tires wearing on edges",
      "steering feels loose",
      "have to constantly correct steering",
      "hit big pothole need alignment"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 1.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/wheel-alignment-tyres-1.jpg",
      "https://example.com/images/services/wheel-alignment-tyres-2.jpg",
      "https://example.com/images/services/wheel-alignment-tyres-3.jpg"
    ]
  },
  {
    "title": "Wheel Balancing",
    "description": "Balance wheels and tires to eliminate vibration, ensure smooth ride, and extend tire life.",
    "category_id": 8,
    "works": [
      "Remove wheels from vehicle",
      "Mount wheels on balancing machine",
      "Spin wheels to detect imbalance",
      "Clean wheel rim and remove old weights",
      "Install proper balance weights",
      "Recheck balance accuracy",
      "Reinstall wheels with correct torque",
      "Test drive for vibration elimination"
    ],
    "symptoms": [
      "steering wheel vibrating",
      "vibration at high speed",
      "shaking when driving fast",
      "car vibrates at 80 kmph",
      "steering shakes above 60",
      "wheels out of balance",
      "vibration through floor",
      "just installed new tires",
      "vibration after tire rotation",
      "steering wobbles at speed"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 0.75,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/wheel-balancing-1.jpg",
      "https://example.com/images/services/wheel-balancing-2.jpg",
      "https://example.com/images/services/wheel-balancing-3.jpg"
    ]
  },
  {
    "title": "Tyre Rotation",
    "description": "Rotate tires to different positions to promote even wear and maximize tire life across all four corners.",
    "category_id": 8,
    "works": [
      "Loosen wheel lug nuts",
      "Lift vehicle on hoist or jack stands",
      "Remove all four wheels",
      "Rotate tires per manufacturer pattern",
      "Inspect tires for damage or uneven wear",
      "Reinstall wheels with proper torque sequence",
      "Check tire pressures and adjust",
      "Reset TPMS if equipped"
    ],
    "symptoms": [
      "front tires wearing faster",
      "uneven tire wear pattern",
      "tires need rotation",
      "want to extend tire life",
      "preventive tire maintenance",
      "rear tires still good front worn",
      "tire rotation due",
      "maximize tire lifespan",
      "even out tire wear"
    ],
    "warranty_kms": 10000,
    "warranty_months": 6,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/tyre-rotation-1.jpg",
      "https://example.com/images/services/tyre-rotation-2.jpg",
      "https://example.com/images/services/tyre-rotation-3.jpg"
    ]
  },
  {
    "title": "Tyre Replacement",
    "description": "Remove old or damaged tires and install new ones with proper mounting, balancing, and pressure adjustment.",
    "category_id": 8,
    "works": [
      "Remove wheels from vehicle",
      "Break tire bead from rim",
      "Remove old tire from wheel",
      "Inspect rim for damage or corrosion",
      "Mount new tire on rim with lubricant",
      "Inflate to proper pressure and seat bead",
      "Balance wheel and tire assembly",
      "Install on vehicle and torque properly",
      "Reset TPMS sensors if equipped"
    ],
    "symptoms": [
      "tire worn out completely",
      "tire tread gone",
      "tire damaged beyond repair",
      "tire has bulge on side",
      "tire sidewall damaged",
      "tire punctured badly",
      "tires bald and smooth",
      "tire age too old",
      "tire cracked and dry",
      "failed in tire inspection",
      "need new tires urgently"
    ],
    "warranty_kms": 1000,
    "warranty_months": 1,
    "time_hrs": 1.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/tyre-replacement-1.jpg",
      "https://example.com/images/services/tyre-replacement-2.jpg",
      "https://example.com/images/services/tyre-replacement-3.jpg"
    ]
  },
  {
    "title": "Puncture Repair",
    "description": "Locate and repair tire punctures to restore tire integrity and extend tire service life safely.",
    "category_id": 8,
    "works": [
      "Remove wheel from vehicle",
      "Locate puncture by submersion or soapy water",
      "Remove foreign object from tire",
      "Ream puncture hole to clean edges",
      "Apply rubber cement and install plug",
      "Trim plug flush with tire surface",
      "Reinflate tire to proper pressure",
      "Balance wheel and reinstall"
    ],
    "symptoms": [
      "tire punctured",
      "tire losing air",
      "flat tire",
      "tire goes flat overnight",
      "nail in tire",
      "slow puncture",
      "tire pressure keeps dropping",
      "tire deflating slowly",
      "hole in tire",
      "tire needs air daily",
      "ran over sharp object"
    ],
    "warranty_kms": 5000,
    "warranty_months": 3,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/puncture-repair-1.jpg",
      "https://example.com/images/services/puncture-repair-2.jpg",
      "https://example.com/images/services/puncture-repair-3.jpg"
    ]
  },
  {
    "title": "Dent Removal",
    "description": "Professional dent repair using paintless or traditional methods to restore body panel appearance without replacement.",
    "category_id": 9,
    "works": [
      "Assess dent location and severity",
      "Access panel from behind if possible",
      "Use PDR tools to massage dent out",
      "Apply heat or cold for metal manipulation",
      "Fill and sand if traditional repair needed",
      "Blend repair area with surrounding panel",
      "Polish repaired area to match finish"
    ],
    "symptoms": [
      "dent on door",
      "dent on bonnet",
      "car door dented",
      "body panel pushed in",
      "dent from parking accident",
      "shopping cart hit car",
      "hail damage on car",
      "someone hit my parked car",
      "dent on fender",
      "minor collision dent",
      "body work needed"
    ],
    "warranty_kms": 0,
    "warranty_months": 6,
    "time_hrs": 2.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/dent-removal-1.jpg",
      "https://example.com/images/services/dent-removal-2.jpg",
      "https://example.com/images/services/dent-removal-3.jpg"
    ]
  },
  {
    "title": "Scratch Repair",
    "description": "Repair paint scratches from minor to deep using touch-up, blending, or panel repainting techniques.",
    "category_id": 9,
    "works": [
      "Clean and assess scratch depth",
      "Sand scratch area with fine grit paper",
      "Apply primer if scratch reaches metal",
      "Apply matching color base coat layers",
      "Apply clear coat for protection and gloss",
      "Wet sand and polish for seamless blend",
      "Inspect under different lighting conditions"
    ],
    "symptoms": [
      "scratch on car door",
      "paint scratched off",
      "deep scratch on bumper",
      "someone keyed my car",
      "scratches from tree branch",
      "paint damage on side",
      "scrape mark on car",
      "minor scratch needs fixing",
      "paint chipped and scratched",
      "scratch down to metal",
      "surface scratches on paint"
    ],
    "warranty_kms": 0,
    "warranty_months": 6,
    "time_hrs": 1.5,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/scratch-repair-1.jpg",
      "https://example.com/images/services/scratch-repair-2.jpg",
      "https://example.com/images/services/scratch-repair-3.jpg"
    ]
  },
  {
    "title": "Full Body Painting",
    "description": "Complete vehicle repainting with surface preparation, multiple coat application, and professional finishing for showroom appearance.",
    "category_id": 9,
    "works": [
      "Strip old paint or sand entire vehicle",
      "Repair all dents and imperfections",
      "Apply body filler and block sand smooth",
      "Mask all trim, glass, and rubber parts",
      "Apply epoxy primer and primer surfacer",
      "Apply base coat in multiple layers",
      "Apply clear coat with proper technique",
      "Color sand and polish for mirror finish",
      "Reassemble all removed components"
    ],
    "symptoms": [
      "want to change car color",
      "paint faded badly",
      "paint oxidized and dull",
      "entire car needs repainting",
      "old paint peeling off",
      "rust patches on body",
      "want fresh new look",
      "complete repaint needed",
      "paint looks very old",
      "car body in bad condition",
      "want showroom finish",
      "restore car to new condition"
    ],
    "warranty_kms": 0,
    "warranty_months": 12,
    "time_hrs": 40.0,
    "difficulty": 5,
    "images": [
      "https://example.com/images/services/full-body-painting-1.jpg",
      "https://example.com/images/services/full-body-painting-2.jpg",
      "https://example.com/images/services/full-body-painting-3.jpg"
    ]
  },
  {
    "title": "Bumper Repair",
    "description": "Repair or refinish damaged bumper covers to restore appearance and protect vehicle structure.",
    "category_id": 9,
    "works": [
      "Remove bumper cover from vehicle",
      "Clean and prepare damaged area",
      "Plastic weld cracks from behind",
      "Fill and shape damaged areas",
      "Sand entire bumper for paint adhesion",
      "Apply plastic primer and base coat",
      "Apply color-matched paint and clear coat",
      "Reinstall bumper with proper alignment"
    ],
    "symptoms": [
      "bumper cracked",
      "bumper scratched badly",
      "bumper dent from parking",
      "bumper paint chipped",
      "rear bumper damaged",
      "front bumper broken",
      "bumper hanging loose",
      "bumper scraped on speed breaker",
      "bumper needs painting",
      "bumper collision damage"
    ],
    "warranty_kms": 0,
    "warranty_months": 6,
    "time_hrs": 3.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/bumper-repair-1.jpg",
      "https://example.com/images/services/bumper-repair-2.jpg",
      "https://example.com/images/services/bumper-repair-3.jpg"
    ]
  },
  {
    "title": "Alloy Wheel Painting",
    "description": "Refinish alloy wheels with proper preparation and coating to restore appearance and protect from corrosion.",
    "category_id": 9,
    "works": [
      "Remove wheels from vehicle",
      "Strip old paint or coating completely",
      "Repair curb rash and minor damage",
      "Sand and smooth wheel surface",
      "Apply wheel primer coat",
      "Apply color coat in multiple layers",
      "Apply protective clear coat",
      "Cure coating properly before installation"
    ],
    "symptoms": [
      "alloy wheels scratched",
      "wheel paint peeling",
      "curb damage on wheels",
      "wheels look old and worn",
      "alloy wheels corroded",
      "want black painted wheels",
      "wheel finish damaged",
      "wheels need refurbishing",
      "alloy wheels faded",
      "rims look terrible"
    ],
    "warranty_kms": 0,
    "warranty_months": 6,
    "time_hrs": 4.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/alloy-wheel-painting-1.jpg",
      "https://example.com/images/services/alloy-wheel-painting-2.jpg",
      "https://example.com/images/services/alloy-wheel-painting-3.jpg"
    ]
  },
  {
    "title": "Exterior Wash",
    "description": "Thorough exterior cleaning to remove dirt, grime, and contaminants for a clean and fresh vehicle appearance.",
    "category_id": 10,
    "works": [
      "Pre-rinse vehicle to loosen dirt",
      "Apply pH-balanced car shampoo",
      "Hand wash all exterior surfaces",
      "Clean wheels and wheel wells thoroughly",
      "Rinse completely with clean water",
      "Dry with microfiber towels or air blower",
      "Clean windows and mirrors"
    ],
    "symptoms": [
      "car very dirty",
      "car needs washing",
      "dust and dirt all over",
      "bird droppings on car",
      "mud on car body",
      "want clean car",
      "car exterior dirty",
      "need basic car wash"
    ],
    "warranty_kms": 0,
    "warranty_months": 0,
    "time_hrs": 0.5,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/exterior-wash-1.jpg",
      "https://example.com/images/services/exterior-wash-2.jpg",
      "https://example.com/images/services/exterior-wash-3.jpg"
    ]
  },
  {
    "title": "Interior Vacuuming & Cleaning",
    "description": "Deep interior cleaning including vacuuming, surface wiping, and stain removal for a fresh cabin environment.",
    "category_id": 10,
    "works": [
      "Remove floor mats and vacuum thoroughly",
      "Vacuum seats, carpets, and crevices",
      "Clean and condition leather or fabric seats",
      "Wipe down dashboard and door panels",
      "Clean center console and cup holders",
      "Clean and polish interior trim",
      "Clean windows from inside",
      "Replace air freshener"
    ],
    "symptoms": [
      "car interior very dirty",
      "dust on dashboard",
      "crumbs in seats",
      "dirty floor mats",
      "stains on seats",
      "bad smell inside car",
      "messy interior",
      "need deep cleaning inside",
      "interior looks neglected",
      "want fresh clean cabin"
    ],
    "warranty_kms": 0,
    "warranty_months": 0,
    "time_hrs": 1.0,
    "difficulty": 1,
    "images": [
      "https://example.com/images/services/interior-cleaning-1.jpg",
      "https://example.com/images/services/interior-cleaning-2.jpg",
      "https://example.com/images/services/interior-cleaning-3.jpg"
    ]
  },
  {
    "title": "Engine Bay Cleaning",
    "description": "Safe cleaning and degreasing of engine compartment to improve appearance and help identify leaks.",
    "category_id": 10,
    "works": [
      "Cover sensitive electrical components",
      "Apply engine degreaser to dirty areas",
      "Agitate with brushes for stubborn grime",
      "Rinse with low-pressure water carefully",
      "Blow dry with compressed air",
      "Apply plastic and rubber dressing",
      "Remove protective covers and inspect"
    ],
    "symptoms": [
      "engine bay very dirty",
      "oil and grease in engine",
      "dust accumulated on engine",
      "engine looks grimy",
      "want clean engine compartment",
      "engine bay needs cleaning",
      "greasy engine components",
      "engine area neglected"
    ],
    "warranty_kms": 0,
    "warranty_months": 0,
    "time_hrs": 1.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/engine-bay-cleaning-1.jpg",
      "https://example.com/images/services/engine-bay-cleaning-2.jpg",
      "https://example.com/images/services/engine-bay-cleaning-3.jpg"
    ]
  },
  {
    "title": "Full Body Polishing",
    "description": "Multi-stage paint correction and polishing to remove swirls, scratches, and restore deep gloss and shine.",
    "category_id": 10,
    "works": [
      "Wash and clay bar paint surface",
      "Inspect paint condition under proper lighting",
      "Compound heavily oxidized or scratched areas",
      "Polish paint with medium cut polish",
      "Apply finishing polish for maximum gloss",
      "Remove polish residue completely",
      "Apply paint sealant or wax protection",
      "Dress tires and exterior trim"
    ],
    "symptoms": [
      "paint looks dull",
      "swirl marks on paint",
      "paint not shiny",
      "paint oxidized",
      "want glossy finish",
      "minor scratches all over",
      "paint needs buffing",
      "car lost its shine",
      "paint looks faded",
      "want mirror finish",
      "restore paint gloss"
    ],
    "warranty_kms": 0,
    "warranty_months": 3,
    "time_hrs": 4.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/full-body-polishing-1.jpg",
      "https://example.com/images/services/full-body-polishing-2.jpg",
      "https://example.com/images/services/full-body-polishing-3.jpg"
    ]
  },
  {
    "title": "Complete Detailing Package",
    "description": "Comprehensive interior and exterior detailing for showroom-quality appearance and protection.",
    "category_id": 10,
    "works": [
      "Full exterior wash and decontamination",
      "Paint correction and polishing",
      "Apply ceramic coating or premium wax",
      "Deep clean and condition all interior surfaces",
      "Steam clean carpets and upholstery",
      "Clean and protect leather surfaces",
      "Engine bay detailing and dressing",
      "Headlight restoration if needed",
      "Apply tire shine and trim dressing",
      "Final inspection and quality check"
    ],
    "symptoms": [
      "want complete car makeover",
      "car needs full detailing",
      "want showroom condition",
      "car looking old and tired",
      "prepare car for sale",
      "want professional detailing",
      "complete car restoration",
      "car needs everything done",
      "want car like new",
      "comprehensive cleaning needed",
      "premium detailing required"
    ],
    "warranty_kms": 0,
    "warranty_months": 6,
    "time_hrs": 8.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/complete-detailing-1.jpg",
      "https://example.com/images/services/complete-detailing-2.jpg",
      "https://example.com/images/services/complete-detailing-3.jpg"
    ]
  },
  {
    "title": "Seat Cover Installation",
    "description": "Professional installation of aftermarket seat covers to protect or enhance interior appearance and comfort.",
    "category_id": 11,
    "works": [
      "Remove headrests for easier installation",
      "Position seat cover on seat properly",
      "Stretch and fit cover over seat contours",
      "Secure straps and hooks underneath seat",
      "Tuck excess material into crevices",
      "Reinstall headrests through cover openings",
      "Adjust for wrinkle-free appearance",
      "Verify airbag compatibility if applicable"
    ],
    "symptoms": [
      "want seat covers installed",
      "protect original seats",
      "seats getting worn",
      "bought new seat covers",
      "want custom seat covers",
      "seats look old",
      "need seat protection",
      "upgrade interior look",
      "cover damaged seats"
    ],
    "warranty_kms": 0,
    "warranty_months": 3,
    "time_hrs": 1.0,
    "difficulty": 2,
    "images": [
      "https://example.com/images/services/seat-cover-installation-1.jpg",
      "https://example.com/images/services/seat-cover-installation-2.jpg",
      "https://example.com/images/services/seat-cover-installation-3.jpg"
    ]
  },
  {
    "title": "Audio System Setup",
    "description": "Install and configure aftermarket audio components including head unit, speakers, and amplifiers for enhanced sound quality.",
    "category_id": 11,
    "works": [
      "Remove factory head unit and speakers",
      "Install new head unit with wiring harness",
      "Mount and wire new speakers",
      "Install amplifier and run power cables",
      "Connect RCA cables and speaker wires",
      "Mount and wire subwoofer if included",
      "Configure head unit settings and equalization",
      "Test all audio components and balance",
      "Secure all wiring properly"
    ],
    "symptoms": [
      "want better sound system",
      "factory speakers not good",
      "need music system upgrade",
      "want subwoofer installed",
      "audio quality poor",
      "speakers not working",
      "want amplifier added",
      "need new stereo installed",
      "upgrade car audio",
      "want premium sound",
      "install aftermarket speakers"
    ],
    "warranty_kms": 0,
    "warranty_months": 12,
    "time_hrs": 4.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/audio-system-setup-1.jpg",
      "https://example.com/images/services/audio-system-setup-2.jpg",
      "https://example.com/images/services/audio-system-setup-3.jpg"
    ]
  },
  {
    "title": "Reverse Camera Installation",
    "description": "Install rear-view camera system for safer reversing and parking with display integration.",
    "category_id": 11,
    "works": [
      "Choose optimal camera mounting location",
      "Drill hole for camera mounting",
      "Install camera with proper angle adjustment",
      "Route video cable through vehicle interior",
      "Connect power to reverse light circuit",
      "Install or integrate with display screen",
      "Configure camera guidelines and settings",
      "Test camera operation in reverse gear",
      "Secure all wiring and trim panels"
    ],
    "symptoms": [
      "want reverse camera",
      "difficult to reverse park",
      "need parking assistance",
      "blind spot when reversing",
      "want rear view camera",
      "safety feature needed",
      "scared to reverse",
      "parking sensors not enough",
      "need visual aid for parking",
      "upgrade safety features"
    ],
    "warranty_kms": 0,
    "warranty_months": 12,
    "time_hrs": 2.5,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/reverse-camera-installation-1.jpg",
      "https://example.com/images/services/reverse-camera-installation-2.jpg",
      "https://example.com/images/services/reverse-camera-installation-3.jpg"
    ]
  },
  {
    "title": "GPS/Tracking Device Installation",
    "description": "Install GPS tracking device for vehicle location monitoring, theft recovery, and fleet management.",
    "category_id": 11,
    "works": [
      "Choose concealed mounting location",
      "Connect power from fuse box or battery",
      "Install GPS antenna for optimal reception",
      "Program device with SIM card and settings",
      "Configure tracking platform and alerts",
      "Test GPS signal and location accuracy",
      "Secure device from detection or tampering",
      "Provide user access credentials"
    ],
    "symptoms": [
      "want GPS tracker installed",
      "need vehicle tracking",
      "security concern for car",
      "want to monitor car location",
      "theft prevention needed",
      "fleet management requirement",
      "need anti-theft device",
      "want real-time tracking",
      "safety and security upgrade",
      "track car remotely"
    ],
    "warranty_kms": 0,
    "warranty_months": 12,
    "time_hrs": 1.5,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/gps-tracking-installation-1.jpg",
      "https://example.com/images/services/gps-tracking-installation-2.jpg",
      "https://example.com/images/services/gps-tracking-installation-3.jpg"
    ]
  },
  {
    "title": "Security Alarm Installation",
    "description": "Install comprehensive vehicle security system with sensors, siren, and remote control for theft protection.",
    "category_id": 11,
    "works": [
      "Install main control module in hidden location",
      "Mount door, hood, and trunk sensors",
      "Install shock and motion sensors",
      "Wire to ignition and starter circuits",
      "Install loud siren in secure location",
      "Program remote controls and receivers",
      "Configure sensitivity and alarm settings",
      "Test all sensors and alarm triggers",
      "Provide user manual and remote controls"
    ],
    "symptoms": [
      "want car alarm installed",
      "no security system in car",
      "theft concern in area",
      "need anti-theft alarm",
      "car security upgrade",
      "want immobilizer system",
      "protect car from theft",
      "need alarm with remote",
      "security enhancement needed",
      "high crime area need alarm"
    ],
    "warranty_kms": 0,
    "warranty_months": 12,
    "time_hrs": 3.5,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/security-alarm-installation-1.jpg",
      "https://example.com/images/services/security-alarm-installation-2.jpg",
      "https://example.com/images/services/security-alarm-installation-3.jpg"
    ]
  },
  {
    "title": "High-Voltage Battery Health Check",
    "description": "Comprehensive diagnostic testing of hybrid or EV battery pack to assess capacity, health, and performance.",
    "category_id": 12,
    "works": [
      "Connect diagnostic equipment to vehicle",
      "Read battery management system data",
      "Check individual cell voltages and balance",
      "Test battery pack capacity and range",
      "Inspect high-voltage connections and cables",
      "Check battery thermal management system",
      "Test battery charge and discharge rates",
      "Provide detailed battery health report",
      "Recommend service or replacement if needed"
    ],
    "symptoms": [
      "EV range reduced",
      "hybrid battery not charging fully",
      "battery capacity decreased",
      "electric range dropped",
      "battery warning light on",
      "hybrid battery weak",
      "EV battery degradation",
      "charging taking longer",
      "battery health check needed",
      "reduced fuel economy in hybrid",
      "battery performance issues"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 1.5,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/ev-battery-health-check-1.jpg",
      "https://example.com/images/services/ev-battery-health-check-2.jpg",
      "https://example.com/images/services/ev-battery-health-check-3.jpg"
    ]
  },
  {
    "title": "Battery Cooling System Service",
    "description": "Service hybrid or EV battery cooling system to maintain optimal temperature and extend battery life.",
    "category_id": 12,
    "works": [
      "Inspect battery cooling system components",
      "Check coolant level and condition",
      "Test cooling system pressure",
      "Flush and replace battery coolant",
      "Inspect cooling pump operation",
      "Check cooling fans and air flow",
      "Test temperature sensors and controls",
      "Verify proper cooling system operation"
    ],
    "symptoms": [
      "battery overheating",
      "battery temperature high",
      "EV battery getting hot",
      "charging speed reduced due to heat",
      "battery cooling fan noise",
      "battery thermal warning",
      "battery coolant low",
      "battery temperature gauge high",
      "reduced performance in hot weather"
    ],
    "warranty_kms": 30000,
    "warranty_months": 24,
    "time_hrs": 2.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/ev-battery-cooling-1.jpg",
      "https://example.com/images/services/ev-battery-cooling-2.jpg",
      "https://example.com/images/services/ev-battery-cooling-3.jpg"
    ]
  },
  {
    "title": "Inverter & Converter Diagnostics",
    "description": "Advanced diagnostics of power electronics including inverter and DC-DC converter for hybrid and EV systems.",
    "category_id": 12,
    "works": [
      "Connect specialized diagnostic equipment",
      "Read inverter and converter fault codes",
      "Test power conversion efficiency",
      "Check high-voltage insulation resistance",
      "Inspect cooling system for power electronics",
      "Test voltage and current outputs",
      "Verify proper communication with systems",
      "Provide diagnostic report with findings",
      "Recommend repairs if issues found"
    ],
    "symptoms": [
      "EV power loss",
      "hybrid system warning light",
      "inverter fault code",
      "power electronics error",
      "electric motor not responding",
      "regenerative braking not working",
      "EV drivetrain issue",
      "hybrid system malfunction",
      "ready light not coming on",
      "electric drive problem"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 2.5,
    "difficulty": 5,
    "images": [
      "https://example.com/images/services/ev-inverter-diagnostics-1.jpg",
      "https://example.com/images/services/ev-inverter-diagnostics-2.jpg",
      "https://example.com/images/services/ev-inverter-diagnostics-3.jpg"
    ]
  },
  {
    "title": "Electric Motor Inspection & Maintenance",
    "description": "Inspect and service electric drive motors to ensure optimal performance, efficiency, and reliability.",
    "category_id": 12,
    "works": [
      "Perform visual inspection of motor housing",
      "Check motor mounting and vibration",
      "Test motor insulation resistance",
      "Inspect motor bearings for wear or noise",
      "Check motor cooling system operation",
      "Test motor performance characteristics",
      "Inspect electrical connections and cables",
      "Verify proper motor control operation",
      "Clean motor cooling passages if accessible"
    ],
    "symptoms": [
      "electric motor making noise",
      "whining from motor",
      "vibration from drivetrain",
      "motor performance reduced",
      "acceleration not smooth",
      "grinding from motor",
      "motor overheating",
      "unusual motor sound",
      "electric drive vibration",
      "motor efficiency decreased"
    ],
    "warranty_kms": 30000,
    "warranty_months": 18,
    "time_hrs": 2.0,
    "difficulty": 4,
    "images": [
      "https://example.com/images/services/ev-motor-inspection-1.jpg",
      "https://example.com/images/services/ev-motor-inspection-2.jpg",
      "https://example.com/images/services/ev-motor-inspection-3.jpg"
    ]
  },
  {
    "title": "Charging System & Port Check",
    "description": "Inspect and test EV charging system and port to ensure safe, reliable, and efficient vehicle charging.",
    "category_id": 12,
    "works": [
      "Inspect charging port for damage or corrosion",
      "Test charging port electrical connections",
      "Verify onboard charger operation",
      "Test charging at different power levels",
      "Check charging cable and connector condition",
      "Inspect charge port locking mechanism",
      "Test charging communication systems",
      "Verify proper charge indicator operation",
      "Check for software updates to charging system"
    ],
    "symptoms": [
      "car not charging",
      "charging very slow",
      "charging port loose",
      "charging cable not connecting",
      "charge port damaged",
      "charging error message",
      "intermittent charging",
      "charging stops randomly",
      "charge port light not working",
      "charging station won't connect",
      "onboard charger issue"
    ],
    "warranty_kms": 15000,
    "warranty_months": 12,
    "time_hrs": 1.0,
    "difficulty": 3,
    "images": [
      "https://example.com/images/services/ev-charging-port-check-1.jpg",
      "https://example.com/images/services/ev-charging-port-check-2.jpg",
      "https://example.com/images/services/ev-charging-port-check-3.jpg"
    ]
  }
]

# Service Fuel Types Mapping
# Maps service_id to applicable fuel_type_ids
# Fuel Types: 1=Petrol, 2=Diesel, 3=Electric, 4=Hybrid, 5=CNG

SERVICE_FUEL_TYPES_DATA = {
    # Service Packages (1-3) - All fuel types
    1: [1, 2, 3, 4, 5],  # Basic Service
    2: [1, 2, 3, 4, 5],  # Standard Service
    3: [1, 2, 3, 4, 5],  # Comprehensive Service
    
    # Engine Services (4-8) - Traditional fuel types only (no pure electric)
    4: [1, 2, 4, 5],  # Oil Change
    5: [1, 2, 4, 5],  # Engine Tune-Up
    6: [1, 2, 4, 5],  # Engine Diagnostics & Repair
    7: [1, 2, 4],     # Timing Belt/Chain Replacement
    8: [1, 2, 4, 5],  # Cooling System Service
    
    # Brake Services (9-13) - All fuel types
    9: [1, 2, 3, 4, 5],   # Brake Pad Replacement
    10: [1, 2, 3, 4, 5],  # Brake Disc/Drum Resurfacing
    11: [1, 2, 3, 4, 5],  # Brake Fluid Replacement
    12: [1, 2, 3, 4, 5],  # ABS Check & Repair
    13: [1, 2, 3, 4, 5],  # Complete Brake Overhaul
    
    # Transmission & Clutch (14-18) - Traditional only (EVs don't have traditional transmission)
    14: [1, 2, 4, 5],  # Clutch Plate Replacement
    15: [1, 2, 4, 5],  # Transmission Fluid Change
    16: [1, 2, 4, 5],  # Gearbox Repair/Overhaul
    17: [1, 2, 4, 5],  # Flywheel Repair/Replacement
    18: [1, 2, 4, 5],  # Hydraulic Clutch System Service
    
    # Suspension & Steering (19-23) - All fuel types
    19: [1, 2, 3, 4, 5],  # Shock Absorber Replacement
    20: [1, 2, 3, 4, 5],  # Wheel Alignment
    21: [1, 2, 3, 4, 5],  # Steering Rack & Pinion Repair
    22: [1, 2, 3, 4, 5],  # Suspension Bush Replacement
    23: [1, 2, 3, 4, 5],  # Power Steering Fluid Check/Refill
    
    # Electrical & Battery (24-28) - All fuel types
    24: [1, 2, 3, 4, 5],  # Battery Check & Replacement
    25: [1, 2, 3, 4, 5],  # Alternator & Starter Motor Repair
    26: [1, 2, 3, 4, 5],  # Headlight & Indicator Replacement
    27: [1, 2, 3, 4, 5],  # ECU Diagnostics
    28: [1, 2, 3, 4, 5],  # Wiring & Fuse Repair
    
    # Air Conditioning & Heating (29-33) - All fuel types
    29: [1, 2, 3, 4, 5],  # AC Gas Refill
    30: [1, 2, 3, 4, 5],  # AC Compressor Repair
    31: [1, 2, 3, 4, 5],  # AC Filter Cleaning/Replacement
    32: [1, 2, 3, 4, 5],  # Heater/Blower Repair
    33: [1, 2, 3, 4, 5],  # Leak Detection & Fix
    
    # Tyres & Wheels (34-38) - All fuel types
    34: [1, 2, 3, 4, 5],  # Wheel Alignment
    35: [1, 2, 3, 4, 5],  # Wheel Balancing
    36: [1, 2, 3, 4, 5],  # Tyre Rotation
    37: [1, 2, 3, 4, 5],  # Tyre Replacement
    38: [1, 2, 3, 4, 5],  # Puncture Repair
    
    # Body & Paint Work (39-43) - All fuel types
    39: [1, 2, 3, 4, 5],  # Dent Removal
    40: [1, 2, 3, 4, 5],  # Scratch Repair
    41: [1, 2, 3, 4, 5],  # Full Body Painting
    42: [1, 2, 3, 4, 5],  # Bumper Repair
    43: [1, 2, 3, 4, 5],  # Alloy Wheel Painting
    
    # Washing & Detailing (44-48) - All fuel types
    44: [1, 2, 3, 4, 5],  # Exterior Wash
    45: [1, 2, 3, 4, 5],  # Interior Vacuuming & Cleaning
    46: [1, 2, 3, 4, 5],  # Engine Bay Cleaning
    47: [1, 2, 3, 4, 5],  # Full Body Polishing
    48: [1, 2, 3, 4, 5],  # Complete Detailing Package
    
    # Accessories & Add-Ons (49-53) - All fuel types
    49: [1, 2, 3, 4, 5],  # Seat Cover Installation
    50: [1, 2, 3, 4, 5],  # Audio System Setup
    51: [1, 2, 3, 4, 5],  # Reverse Camera Installation
    52: [1, 2, 3, 4, 5],  # GPS/Tracking Device Installation
    53: [1, 2, 3, 4, 5],  # Security Alarm Installation
    
    # Hybrid & EV Services (54-58) - Electric and Hybrid only
    54: [3, 4],  # High-Voltage Battery Health Check
    55: [3, 4],  # Battery Cooling System Service
    56: [3, 4],  # Inverter & Converter Diagnostics
    57: [3, 4],  # Electric Motor Inspection & Maintenance
    58: [3, 4],  # Charging System & Port Check
}


# Price Chart Data
# Base prices for each service across different car classes
# Car Classes: 1-3=Hatchback, 4-6=Sedan, 7-9=SUV, 10-12=MPV, 13-14=Coupe, 
#              15-16=Convertible, 17-19=Crossover, 20-21=Pickup Truck

PRICE_CHART_DATA = [
    # Service Packages (1-3)
    {"service_id": 1, "prices": {1: 1500, 2: 2000, 3: 2800, 4: 1800, 5: 2300, 6: 3200, 7: 2200, 8: 2800, 9: 4000, 10: 2000, 11: 2600, 12: 3800, 13: 3000, 14: 4200, 15: 3200, 16: 4500, 17: 2100, 18: 2700, 19: 3900, 20: 2300, 21: 3000}},
    {"service_id": 2, "prices": {1: 2500, 2: 3200, 3: 4500, 4: 2800, 5: 3600, 6: 5000, 7: 3500, 8: 4500, 9: 6500, 10: 3200, 11: 4200, 12: 6000, 13: 4800, 14: 6800, 15: 5000, 16: 7200, 17: 3400, 18: 4400, 19: 6300, 20: 3700, 21: 4800}},
    {"service_id": 3, "prices": {1: 4000, 2: 5200, 3: 7200, 4: 4500, 5: 5800, 6: 8000, 7: 5500, 8: 7200, 9: 10500, 10: 5000, 11: 6800, 12: 9800, 13: 7800, 14: 11000, 15: 8200, 16: 11800, 17: 5300, 18: 7000, 19: 10200, 20: 5800, 21: 7800}},
    
    # Engine Services (4-8)
    {"service_id": 4, "prices": {1: 800, 2: 1000, 3: 1400, 4: 900, 5: 1200, 6: 1600, 7: 1100, 8: 1400, 9: 2000, 10: 1000, 11: 1300, 12: 1900, 13: 1500, 14: 2100, 15: 1600, 16: 2300, 17: 1050, 18: 1350, 19: 1950, 20: 1150, 21: 1500}},
    {"service_id": 5, "prices": {1: 2000, 2: 2500, 3: 3500, 4: 2300, 5: 2800, 6: 3900, 7: 2800, 8: 3500, 9: 5000, 10: 2500, 11: 3200, 12: 4600, 13: 3700, 14: 5200, 15: 3900, 16: 5600, 17: 2700, 18: 3400, 19: 4900, 20: 2900, 21: 3800}},
    {"service_id": 6, "prices": {1: 3000, 2: 3800, 3: 5300, 4: 3400, 5: 4300, 6: 6000, 7: 4200, 8: 5300, 9: 7600, 10: 3800, 11: 4900, 12: 7000, 13: 5600, 14: 7900, 15: 5900, 16: 8500, 17: 4000, 18: 5200, 19: 7400, 20: 4400, 21: 5700}},
    {"service_id": 7, "prices": {1: 8000, 2: 10000, 3: 14000, 4: 9000, 5: 11500, 6: 16000, 7: 11000, 8: 14000, 9: 20000, 10: 10000, 11: 13000, 12: 18500, 13: 15000, 14: 21000, 15: 16000, 16: 23000, 17: 10500, 18: 13500, 19: 19500, 20: 11500, 21: 15000}},
    {"service_id": 8, "prices": {1: 2500, 2: 3200, 3: 4400, 4: 2800, 5: 3600, 6: 5000, 7: 3500, 8: 4500, 9: 6400, 10: 3200, 11: 4100, 12: 5900, 13: 4700, 14: 6700, 15: 5000, 16: 7200, 17: 3400, 18: 4400, 19: 6200, 20: 3700, 21: 4800}},
    
    # Brake Services (9-13)
    {"service_id": 9, "prices": {1: 2500, 2: 3200, 3: 4500, 4: 2800, 5: 3600, 6: 5000, 7: 3500, 8: 4500, 9: 6500, 10: 3200, 11: 4200, 12: 6000, 13: 4800, 14: 6800, 15: 5000, 16: 7200, 17: 3400, 18: 4400, 19: 6300, 20: 3700, 21: 4800}},
    {"service_id": 10, "prices": {1: 3500, 2: 4500, 3: 6300, 4: 4000, 5: 5100, 6: 7100, 7: 5000, 8: 6400, 9: 9100, 10: 4500, 11: 5800, 12: 8400, 13: 6800, 14: 9600, 15: 7100, 16: 10200, 17: 4800, 18: 6200, 19: 8900, 20: 5200, 21: 6800}},
    {"service_id": 11, "prices": {1: 1200, 2: 1500, 3: 2100, 4: 1400, 5: 1700, 6: 2400, 7: 1700, 8: 2100, 9: 3000, 10: 1500, 11: 2000, 12: 2800, 13: 2200, 14: 3100, 15: 2400, 16: 3400, 17: 1600, 18: 2050, 19: 2900, 20: 1800, 21: 2300}},
    {"service_id": 12, "prices": {1: 4000, 2: 5000, 3: 7000, 4: 4500, 5: 5800, 6: 8000, 7: 5500, 8: 7000, 9: 10000, 10: 5000, 11: 6500, 12: 9300, 13: 7500, 14: 10500, 15: 8000, 16: 11500, 17: 5300, 18: 6800, 19: 9700, 20: 5800, 21: 7500}},
    {"service_id": 13, "prices": {1: 8000, 2: 10000, 3: 14000, 4: 9000, 5: 11500, 6: 16000, 7: 11000, 8: 14000, 9: 20000, 10: 10000, 11: 13000, 12: 18500, 13: 15000, 14: 21000, 15: 16000, 16: 23000, 17: 10500, 18: 13500, 19: 19500, 20: 11500, 21: 15000}},
    
    # Transmission & Clutch (14-18)
    {"service_id": 14, "prices": {1: 10000, 2: 12500, 3: 17500, 4: 11000, 5: 14000, 6: 19500, 7: 13500, 8: 17000, 9: 24500, 10: 12000, 11: 15500, 12: 22500, 13: 18000, 14: 25500, 15: 19500, 16: 28000, 17: 12800, 18: 16500, 19: 23800, 20: 14000, 21: 18000}},
    {"service_id": 15, "prices": {1: 2000, 2: 2500, 3: 3500, 4: 2300, 5: 2900, 6: 4000, 7: 2800, 8: 3500, 9: 5000, 10: 2500, 11: 3200, 12: 4600, 13: 3700, 14: 5200, 15: 3900, 16: 5600, 17: 2700, 18: 3400, 19: 4900, 20: 2900, 21: 3800}},
    {"service_id": 16, "prices": {1: 20000, 2: 25000, 3: 35000, 4: 22000, 5: 28000, 6: 39000, 7: 27000, 8: 34000, 9: 49000, 10: 24000, 11: 31000, 12: 45000, 13: 36000, 14: 51000, 15: 39000, 16: 56000, 17: 25600, 18: 33000, 19: 47600, 20: 28000, 21: 36000}},
    {"service_id": 17, "prices": {1: 12000, 2: 15000, 3: 21000, 4: 13500, 5: 17000, 6: 24000, 7: 16500, 8: 21000, 9: 30000, 10: 15000, 11: 19500, 12: 28000, 13: 22500, 14: 31500, 15: 24000, 16: 34500, 17: 15800, 18: 20500, 19: 29300, 20: 17000, 21: 22000}},
    {"service_id": 18, "prices": {1: 2500, 2: 3200, 3: 4400, 4: 2800, 5: 3600, 6: 5000, 7: 3500, 8: 4500, 9: 6400, 10: 3200, 11: 4100, 12: 5900, 13: 4700, 14: 6700, 15: 5000, 16: 7200, 17: 3400, 18: 4400, 19: 6200, 20: 3700, 21: 4800}},
    
    # Suspension & Steering (19-23)
    {"service_id": 19, "prices": {1: 4000, 2: 5000, 3: 7000, 4: 4500, 5: 5800, 6: 8000, 7: 5500, 8: 7000, 9: 10000, 10: 5000, 11: 6500, 12: 9300, 13: 7500, 14: 10500, 15: 8000, 16: 11500, 17: 5300, 18: 6800, 19: 9700, 20: 5800, 21: 7500}},
    {"service_id": 20, "prices": {1: 800, 2: 1000, 3: 1400, 4: 900, 5: 1200, 6: 1600, 7: 1100, 8: 1400, 9: 2000, 10: 1000, 11: 1300, 12: 1900, 13: 1500, 14: 2100, 15: 1600, 16: 2300, 17: 1050, 18: 1350, 19: 1950, 20: 1150, 21: 1500}},
    {"service_id": 21, "prices": {1: 8000, 2: 10000, 3: 14000, 4: 9000, 5: 11500, 6: 16000, 7: 11000, 8: 14000, 9: 20000, 10: 10000, 11: 13000, 12: 18500, 13: 15000, 14: 21000, 15: 16000, 16: 23000, 17: 10500, 18: 13500, 19: 19500, 20: 11500, 21: 15000}},
    {"service_id": 22, "prices": {1: 5000, 2: 6500, 3: 9000, 4: 5500, 5: 7200, 6: 10000, 7: 7000, 8: 9000, 9: 13000, 10: 6500, 11: 8500, 12: 12000, 13: 9500, 14: 13500, 15: 10000, 16: 14500, 17: 6800, 18: 8800, 19: 12500, 20: 7500, 21: 9500}},
    {"service_id": 23, "prices": {1: 500, 2: 600, 3: 850, 4: 550, 5: 700, 6: 950, 7: 650, 8: 850, 9: 1200, 10: 600, 11: 800, 12: 1100, 13: 900, 14: 1250, 15: 950, 16: 1350, 17: 620, 18: 820, 19: 1150, 20: 680, 21: 900}},
    
    # Electrical & Battery (24-28)
    {"service_id": 24, "prices": {1: 3000, 2: 3800, 3: 5300, 4: 3400, 5: 4300, 6: 6000, 7: 4200, 8: 5300, 9: 7600, 10: 3800, 11: 4900, 12: 7000, 13: 5600, 14: 7900, 15: 5900, 16: 8500, 17: 4000, 18: 5200, 19: 7400, 20: 4400, 21: 5700}},
    {"service_id": 25, "prices": {1: 5000, 2: 6500, 3: 9000, 4: 5500, 5: 7200, 6: 10000, 7: 7000, 8: 9000, 9: 13000, 10: 6500, 11: 8500, 12: 12000, 13: 9500, 14: 13500, 15: 10000, 16: 14500, 17: 6800, 18: 8800, 19: 12500, 20: 7500, 21: 9500}},
    {"service_id": 26, "prices": {1: 1500, 2: 1900, 3: 2700, 4: 1700, 5: 2200, 6: 3000, 7: 2100, 8: 2700, 9: 3800, 10: 1900, 11: 2500, 12: 3500, 13: 2800, 14: 4000, 15: 3000, 16: 4300, 17: 2000, 18: 2600, 19: 3700, 20: 2200, 21: 2900}},
    {"service_id": 27, "prices": {1: 2500, 2: 3200, 3: 4500, 4: 2800, 5: 3600, 6: 5000, 7: 3500, 8: 4500, 9: 6500, 10: 3200, 11: 4200, 12: 6000, 13: 4800, 14: 6800, 15: 5000, 16: 7200, 17: 3400, 18: 4400, 19: 6300, 20: 3700, 21: 4800}},
    {"service_id": 28, "prices": {1: 2000, 2: 2600, 3: 3600, 4: 2300, 5: 2900, 6: 4100, 7: 2800, 8: 3600, 9: 5200, 10: 2600, 11: 3400, 12: 4800, 13: 3800, 14: 5400, 15: 4000, 16: 5800, 17: 2700, 18: 3500, 19: 5000, 20: 3000, 21: 3800}},
    
    # Air Conditioning & Heating (29-33)
    {"service_id": 29, "prices": {1: 1500, 2: 1900, 3: 2700, 4: 1700, 5: 2200, 6: 3000, 7: 2100, 8: 2700, 9: 3800, 10: 1900, 11: 2500, 12: 3500, 13: 2800, 14: 4000, 15: 3000, 16: 4300, 17: 2000, 18: 2600, 19: 3700, 20: 2200, 21: 2900}},
    {"service_id": 30, "prices": {1: 8000, 2: 10000, 3: 14000, 4: 9000, 5: 11500, 6: 16000, 7: 11000, 8: 14000, 9: 20000, 10: 10000, 11: 13000, 12: 18500, 13: 15000, 14: 21000, 15: 16000, 16: 23000, 17: 10500, 18: 13500, 19: 19500, 20: 11500, 21: 15000}},
    {"service_id": 31, "prices": {1: 500, 2: 650, 3: 900, 4: 600, 5: 750, 6: 1050, 7: 750, 8: 950, 9: 1350, 10: 700, 11: 900, 12: 1300, 13: 1000, 14: 1400, 15: 1050, 16: 1500, 17: 720, 18: 920, 19: 1320, 20: 800, 21: 1000}},
    {"service_id": 32, "prices": {1: 4000, 2: 5000, 3: 7000, 4: 4500, 5: 5800, 6: 8000, 7: 5500, 8: 7000, 9: 10000, 10: 5000, 11: 6500, 12: 9300, 13: 7500, 14: 10500, 15: 8000, 16: 11500, 17: 5300, 18: 6800, 19: 9700, 20: 5800, 21: 7500}},
    {"service_id": 33, "prices": {1: 2500, 2: 3200, 3: 4500, 4: 2800, 5: 3600, 6: 5000, 7: 3500, 8: 4500, 9: 6500, 10: 3200, 11: 4200, 12: 6000, 13: 4800, 14: 6800, 15: 5000, 16: 7200, 17: 3400, 18: 4400, 19: 6300, 20: 3700, 21: 4800}},
    
    # Tyres & Wheels (34-38)
    {"service_id": 34, "prices": {1: 800, 2: 1000, 3: 1400, 4: 900, 5: 1200, 6: 1600, 7: 1100, 8: 1400, 9: 2000, 10: 1000, 11: 1300, 12: 1900, 13: 1500, 14: 2100, 15: 1600, 16: 2300, 17: 1050, 18: 1350, 19: 1950, 20: 1150, 21: 1500}},
    {"service_id": 35, "prices": {1: 600, 2: 750, 3: 1050, 4: 700, 5: 900, 6: 1250, 7: 850, 8: 1100, 9: 1550, 10: 800, 11: 1000, 12: 1450, 13: 1150, 14: 1600, 15: 1250, 16: 1750, 17: 820, 18: 1050, 19: 1500, 20: 900, 21: 1150}},
    {"service_id": 36, "prices": {1: 500, 2: 650, 3: 900, 4: 600, 5: 750, 6: 1050, 7: 750, 8: 950, 9: 1350, 10: 700, 11: 900, 12: 1300, 13: 1000, 14: 1400, 15: 1050, 16: 1500, 17: 720, 18: 920, 19: 1320, 20: 800, 21: 1000}},
    {"service_id": 37, "prices": {1: 3000, 2: 4000, 3: 5500, 4: 3500, 5: 4500, 6: 6200, 7: 4500, 8: 5800, 9: 8200, 10: 4000, 11: 5200, 12: 7500, 13: 6000, 14: 8500, 15: 6500, 16: 9200, 17: 4300, 18: 5600, 19: 8000, 20: 5000, 21: 6500}},
    {"service_id": 38, "prices": {1: 400, 2: 500, 3: 700, 4: 450, 5: 600, 6: 800, 7: 550, 8: 700, 9: 1000, 10: 500, 11: 650, 12: 950, 13: 750, 14: 1050, 15: 800, 16: 1150, 17: 520, 18: 680, 19: 980, 20: 580, 21: 750}},
    
    # Body & Paint Work (39-43)
    {"service_id": 39, "prices": {1: 2000, 2: 2500, 3: 3500, 4: 2300, 5: 2900, 6: 4000, 7: 2800, 8: 3500, 9: 5000, 10: 2500, 11: 3200, 12: 4600, 13: 3700, 14: 5200, 15: 3900, 16: 5600, 17: 2700, 18: 3400, 19: 4900, 20: 2900, 21: 3800}},
    {"service_id": 40, "prices": {1: 1500, 2: 1900, 3: 2700, 4: 1700, 5: 2200, 6: 3000, 7: 2100, 8: 2700, 9: 3800, 10: 1900, 11: 2500, 12: 3500, 13: 2800, 14: 4000, 15: 3000, 16: 4300, 17: 2000, 18: 2600, 19: 3700, 20: 2200, 21: 2900}},
    {"service_id": 41, "prices": {1: 30000, 2: 38000, 3: 53000, 4: 34000, 5: 43000, 6: 60000, 7: 42000, 8: 53000, 9: 76000, 10: 38000, 11: 49000, 12: 70000, 13: 56000, 14: 79000, 15: 59000, 16: 85000, 17: 40000, 18: 52000, 19: 74000, 20: 44000, 21: 57000}},
    {"service_id": 42, "prices": {1: 3500, 2: 4500, 3: 6300, 4: 4000, 5: 5100, 6: 7100, 7: 5000, 8: 6400, 9: 9100, 10: 4500, 11: 5800, 12: 8400, 13: 6800, 14: 9600, 15: 7100, 16: 10200, 17: 4800, 18: 6200, 19: 8900, 20: 5200, 21: 6800}},
    {"service_id": 43, "prices": {1: 4000, 2: 5000, 3: 7000, 4: 4500, 5: 5800, 6: 8000, 7: 5500, 8: 7000, 9: 10000, 10: 5000, 11: 6500, 12: 9300, 13: 7500, 14: 10500, 15: 8000, 16: 11500, 17: 5300, 18: 6800, 19: 9700, 20: 5800, 21: 7500}},
    
    # Washing & Detailing (44-48)
    {"service_id": 44, "prices": {1: 300, 2: 400, 3: 550, 4: 350, 5: 450, 6: 620, 7: 450, 8: 580, 9: 820, 10: 400, 11: 520, 12: 750, 13: 600, 14: 850, 15: 650, 16: 920, 17: 420, 18: 540, 19: 780, 20: 480, 21: 620}},
    {"service_id": 45, "prices": {1: 500, 2: 650, 3: 900, 4: 600, 5: 750, 6: 1050, 7: 750, 8: 950, 9: 1350, 10: 700, 11: 900, 12: 1300, 13: 1000, 14: 1400, 15: 1050, 16: 1500, 17: 720, 18: 920, 19: 1320, 20: 800, 21: 1000}},
    {"service_id": 46, "prices": {1: 800, 2: 1000, 3: 1400, 4: 900, 5: 1200, 6: 1600, 7: 1100, 8: 1400, 9: 2000, 10: 1000, 11: 1300, 12: 1900, 13: 1500, 14: 2100, 15: 1600, 16: 2300, 17: 1050, 18: 1350, 19: 1950, 20: 1150, 21: 1500}},
    {"service_id": 47, "prices": {1: 3000, 2: 3800, 3: 5300, 4: 3400, 5: 4300, 6: 6000, 7: 4200, 8: 5300, 9: 7600, 10: 3800, 11: 4900, 12: 7000, 13: 5600, 14: 7900, 15: 5900, 16: 8500, 17: 4000, 18: 5200, 19: 7400, 20: 4400, 21: 5700}},
    {"service_id": 48, "prices": {1: 6000, 2: 7600, 3: 10600, 4: 6800, 5: 8600, 6: 12000, 7: 8400, 8: 10600, 9: 15200, 10: 7600, 11: 9800, 12: 14000, 13: 11200, 14: 15800, 15: 11800, 16: 17000, 17: 8000, 18: 10400, 19: 14800, 20: 8800, 21: 11400}},
    
    # Accessories & Add-Ons (49-53)
    {"service_id": 49, "prices": {1: 1500, 2: 1900, 3: 2700, 4: 1700, 5: 2200, 6: 3000, 7: 2100, 8: 2700, 9: 3800, 10: 1900, 11: 2500, 12: 3500, 13: 2800, 14: 4000, 15: 3000, 16: 4300, 17: 2000, 18: 2600, 19: 3700, 20: 2200, 21: 2900}},
    {"service_id": 50, "prices": {1: 5000, 2: 6500, 3: 9000, 4: 5500, 5: 7200, 6: 10000, 7: 7000, 8: 9000, 9: 13000, 10: 6500, 11: 8500, 12: 12000, 13: 9500, 14: 13500, 15: 10000, 16: 14500, 17: 6800, 18: 8800, 19: 12500, 20: 7500, 21: 9500}},
    {"service_id": 51, "prices": {1: 3000, 2: 3800, 3: 5300, 4: 3400, 5: 4300, 6: 6000, 7: 4200, 8: 5300, 9: 7600, 10: 3800, 11: 4900, 12: 7000, 13: 5600, 14: 7900, 15: 5900, 16: 8500, 17: 4000, 18: 5200, 19: 7400, 20: 4400, 21: 5700}},
    {"service_id": 52, "prices": {1: 4000, 2: 5000, 3: 7000, 4: 4500, 5: 5800, 6: 8000, 7: 5500, 8: 7000, 9: 10000, 10: 5000, 11: 6500, 12: 9300, 13: 7500, 14: 10500, 15: 8000, 16: 11500, 17: 5300, 18: 6800, 19: 9700, 20: 5800, 21: 7500}},
    {"service_id": 53, "prices": {1: 6000, 2: 7500, 3: 10500, 4: 6500, 5: 8500, 6: 11800, 7: 8000, 8: 10500, 9: 15000, 10: 7500, 11: 9800, 12: 14000, 13: 11000, 14: 15500, 15: 11800, 16: 17000, 17: 7800, 18: 10200, 19: 14500, 20: 8500, 21: 11000}},
    
    # Hybrid & EV Services (54-58)
    {"service_id": 54, "prices": {1: 3500, 2: 4500, 3: 6300, 4: 4000, 5: 5100, 6: 7100, 7: 5000, 8: 6400, 9: 9100, 10: 4500, 11: 5800, 12: 8400, 13: 6800, 14: 9600, 15: 7100, 16: 10200, 17: 4800, 18: 6200, 19: 8900, 20: 5200, 21: 6800}},
    {"service_id": 55, "prices": {1: 4500, 2: 5800, 3: 8100, 4: 5000, 5: 6500, 6: 9000, 7: 6200, 8: 8000, 9: 11500, 10: 5800, 11: 7500, 12: 10800, 13: 8500, 14: 12000, 15: 9000, 16: 13000, 17: 6000, 18: 7800, 19: 11200, 20: 6500, 21: 8500}},
    {"service_id": 56, "prices": {1: 5500, 2: 7000, 3: 9800, 4: 6200, 5: 8000, 6: 11100, 7: 7600, 8: 9800, 9: 14000, 10: 7000, 11: 9100, 12: 13000, 13: 10500, 14: 14800, 15: 11100, 16: 16000, 17: 7400, 18: 9600, 19: 13700, 20: 8100, 21: 10500}},
    {"service_id": 57, "prices": {1: 4000, 2: 5000, 3: 7000, 4: 4500, 5: 5800, 6: 8000, 7: 5500, 8: 7000, 9: 10000, 10: 5000, 11: 6500, 12: 9300, 13: 7500, 14: 10500, 15: 8000, 16: 11500, 17: 5300, 18: 6800, 19: 9700, 20: 5800, 21: 7500}},
    {"service_id": 58, "prices": {1: 2500, 2: 3200, 3: 4500, 4: 2800, 5: 3600, 6: 5000, 7: 3500, 8: 4500, 9: 6500, 10: 3200, 11: 4200, 12: 6000, 13: 4800, 14: 6800, 15: 5000, 16: 7200, 17: 3400, 18: 4400, 19: 6300, 20: 3700, 21: 4800}},
]


# Booking statuses
BOOKING_STATUSES = [
    "booked",
    "pickup",
    "received",
    "analysis",
    "analysed",
    "in-progress",
    "completed",
    "out for delivery",
    "delivered",
    "cancelled",
]

# Additional statuses for assignments and services
OTHER_STATUSES = [
    "assigned",    # for booking_assignment
    "confirmed",   # for booked_services
    "rejected",    # for booked_services
    "pending",     # for payment
    "success",     # for payment
    "failed"       # for payment
]

ALL_STATUSES = BOOKING_STATUSES + OTHER_STATUSES
