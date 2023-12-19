

<!-- OBJECTIVE -->
## OBJECTIVE

OBJECTIVE: Create a simple Natural Language Processing (NLP) model that iterates over a list of plain text from workover reports and searches for location of rod breaks and root cause of failure. 

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

Currently well site supervisors create a workover log every time they service a well. The logs are in long-text form with no particular pattern. There are pieces of information that are currently not captured in salesforce that are invaluable in troubleshooting well servicing such as location of rod breaks and root cause of failure (i.e. wear or corrosion).

Example of a workover report:
"06:00 - 07:00 - Travel from base to above location and load fluid 07:00 - 07:15 - Safety Meeting/Hazard assessment with all personal on location. Discuss task at hand, fit for duty policy, moving parts, pinch points, overhead loads, spotting equipment, LEL's, use of tag lines, Rigging in/out equipment, lease conditions, muster point, safety slings, smoking area, lifting heavy objects, ERP, Work duties, PPE, Proper grounding of equipment, Weather conditions, pumping fluids, checking pressures on well, see attached Site Specific. 07:15 - 07:25 - Sweep lease (GOOD). Check well pressure. 07:25 - 08:00 - Spot and RU rod rig according to AEB, OH&S, Husky regs and company policies. Pressure test and function test rod BOP (Good), crown saver, emergency shut downs and other associated safety equipment. 08:00 - 08:45 - Latch onto rod string and check string weight (4200lbs), Remove drive head, install rod BOP, POOH w/polish rod and sucker rods. Rig in Rod guide, rod reel, function test safety brake (Good). POOH w/28.6mm prorod rod to break (784m). Cap well. Weld on fish pin. Rod string is showing signs of major corrosion. (pictures attached in attachment folder) 08:45 - 10:00 - Weld on production pin. 10:00 - 11:45 - RIH w/overshot prorod, ponies and polish rod, install rod spinner, latch overshot onto fish and pull rotor from stator @ 9decs with good rotation, lay out sucker rod and ponies, flush well w/4m3 of produced water, POOH w/prorod to fish, Remove 21? of prorod , pull and inspect shear and rotor (Good). 11:45 - 13:30 - RIH w/prorod string, rig out rod reel and rod guide, put accelerator away and RIH w/sucker rod, pony rods and polish rod. Space out rod string has per manufactures specs. Remove rod BOP, install drive head, tighten rod clamps, tie in and pressure test pump to 3500kpa(Good). Rig out all associated equipment, blow off remaining fluid, clean up location, well will be started up by operations when tanks are repaired. Sign Vendor invoices and release all services. Update wellview, attach ERP, Site Specific and invoices in salesforce. Job Complete. Final Cost $4570.00"

Text processing steps are as follows:
1) Remove punctuation
2) Lowercase
3) Tokenize
4) Remove Connecting Words “a, and, but, how, or , what”
5) Word Normalization – “Playing à Play, Played à Play, etc…”
6) Create grams (in this case I chose trigrams - 3 word triples)

<!-- USAGE EXAMPLES -->
## Usage

Output from the script are ingested into Spotfire. A visual representation of the wellbore (using the wells directional survey) is joined with the meta data scraped from the workover report including location of the breaks and notes of the root cause (if available). This should be used to assist production engineers with deciding on curative measures on future workovers (i.e. coated tubing, hardened rods, shallower pump depth)

![Example of rod break dashboard](https://lh3.googleusercontent.com/pw/ABLVV87CuKA9AzajlHjcxFDrWHoaOutapYRbV9cICTGcom5d1AV-2Z_eC_2L9keP2YpXOxvyOMBKG8_pLmg36nK3i_qOFSkyyRshQRY4_sqODPEizAGsCIg=w1376-h766-s-no-gm)

<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com

