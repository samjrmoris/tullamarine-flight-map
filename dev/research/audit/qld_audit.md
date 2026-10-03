# Brisbane (qld) audit, checked 1 October 2026

## Right
- All runway ends (YBBN both parallels, YBAF, YAMB) are within 60 m of OpenStreetMap; ends[0] is the correct threshold each time. OurAirports differs only where it lists physical ends and displaced thresholds.
- OSM aerodrome boundaries exist for all three airports (YBBN relation 17378993, YBAF way 423143197, YAMB way 902155670). Archerfield's is about 25 percent smaller than the quoted 257 ha.
- Airport notes: no curfew, night over-water rules, SODPROPS (arrive 19R, depart 01R), the July 2026 Package 3 changes, and "regular independent parallel ops from late 2027" all match Airservices / the airport.
- 11 of 17 data centres exist at the stated address and operator.
- Cross River Rail, Wave, Coomera Connector and Bruce Highway status text agrees with official/search sources.
- Education map link loads; most other links load (TMR and delivering2032 return 403 to scripts only).

## Wrong or needs changing
- Data centres: "iseek / DigiCo Brisbane Airport stage 2" is built and operating as DigiCo BNE2 at 4 Cycas Lane (status should be live). "NEXTDC B2 expansion" is approved and under construction (Multiplex), completion about early 2027. Fujitsu (7 Brandl Street, Eight Mile Plains) and DSColo (Unit 6, 2060 Moggill Road, Kenmore) now have street addresses. Swanbank has an address (Lot 5, 6 Leaf Street), developer and application 2285/2026/MCU (still under assessment). The Vocus Eagle Street entry is a telecom room in an office tower and directories disagree on the operator (Vocus vs TPG Telecom).
- Exact coordinates found for 15 of 17 entries (OSM buildings or address points). None for DigiCo Woolloongabba or Swanbank.
- Missing from the file: DigiCo BNE4 next to BNE2 (about 19.6 MW, 2027) and the Quinbrook Supernode at Brendale (approved 2022, status unclear).
- Logan and Gold Coast Faster Rail line is off: several points are 0.9 to 2.6 km from the real stations. Replacement points (station coordinates) are in the JSON. Kuraby, Loganlea and Beenleigh hubs are 330 to 680 m out.
- Cross River Rail: Exhibition hub is 480 m off and is a new station, not an upgrade; the official page lists 7 rebuilt stations, not eight.
- Flight-path fans: the map's -40/0/+40 on all four ends is not what is flown. 19R/19L, 01L/01R each differ (see JSON). 19R jets go straight then turn right; 19L jets turn left to the south (right at night for northbound); 01R turns right at the VOR over the bay; 01L jets go north over the bay and non-jets turn about 30 degrees left. The 26 km straight arrival is longer than the ILS final (about 18 to 22 km); suggest about 22 km. Confidence is low to medium; official tracks are in charts I could not read.
- regions/qld.js has `future: null` although the research file defines a "late 2027" future scenario; decide whether that is intentional.
- Skytower is 274.3 m, not about 270 m (the map shows the name only).

## Could not verify
- Exact current departure tracks after July 2026, and the Airservices interactive map.
- datacentermap.com (HTTP 429 and bot check), TMR project pages (403), so alignments for The Wave, Coomera Connector and Bruce Highway, and the Woolloongabba station coordinates, are unconfirmed.
- Whether Datacom and Vocus/TPG are still operating data centres in 2026 (directory listings only).
