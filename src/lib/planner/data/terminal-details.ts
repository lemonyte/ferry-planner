// Moved out of `locations.ts` while nothing uses it, so that the site does not download it.
// Import it only where it is used, which keeps it out of the pages that do not use it.

import type { TerminalId } from "./locations.ts";

export interface TerminalDetails {
    long_id: string;
    address: string;
    /** Booking check-in open time in minutes. */
    res_open?: number;
    /** Booking check-in extra time required at peak season in minutes. */
    res_peak_extra?: number;
    /** Assured loading check-in open time in minutes. */
    assured_open?: number;
    /** Hostled vehicles check-in open time in minutes. */
    hostled_open?: number;
}

/** Terminal details that the planner does not use, by terminal ID. */
export const terminalDetails: Readonly<Record<TerminalId, TerminalDetails>> = {
    SLT: {
        long_id: "powell-river-saltery-bay",
        address: "15070 Highway 101, Powell River, V8A 0N2",
    },
    NAH: {
        long_id: "nanaimo-nanaimo-harbour",
        address: "160 Front Street, Nanaimo, V9S 5R1",
    },
    COR: {
        long_id: "cortes-island-whaletown",
        address: "Whaletown, Cortes Island, V0P 1Z0",
    },
    TSA: {
        long_id: "vancouver-tsawwassen",
        address: "1 Ferry Causeway, Delta, V4M 4G6",
        res_open: 60,
        assured_open: 60,
    },
    SHW: {
        long_id: "shearwater",
        address: "Denny Island, Shearwater, V0T 1B0",
    },
    POB: {
        long_id: "pender-island-otter-bay",
        address: "1371 Otter Bay Road, North Pender Island, V0N 2M0",
        res_open: 60,
    },
    SWB: {
        long_id: "victoria-swartz-bay",
        address: "11300 Patricia Bay Hwy, Sidney, V8L 5J4",
        res_open: 60,
        assured_open: 60,
    },
    PSK: {
        long_id: "graham-island-skidegate",
        address: "#1 Hwy 16 Skidegate Landing, Haida Gwaii, V0T 1S1",
        res_open: 120,
    },
    FUL: {
        long_id: "salt-spring-island-fulford-harbour",
        address: "2920 Fulford-Ganges Road, Salt Spring Island, V8K 1Z2",
    },
    NBN: {
        long_id: "gambier-island-new-brighton",
        address: "Austin Road, New Brighton, Gambier Island, V0N 1V0",
    },
    DNE: {
        long_id: "denman-island-east-gravelly-bay",
        address: "Gravelly Bay, East Road, Denman Island, V0R 1T0",
    },
    ALF: {
        long_id: "moresby-island-alliford-bay",
        address: "Beach Road, Moresby Island Haida Gwaii, V0T 1T0",
    },
    DNM: {
        long_id: "denman-island-west",
        address: "3661 Denman Road, Denman Island , V0R 1T0",
    },
    CAM: {
        long_id: "campbell-river",
        address: "1001 Island Highway, Campbell River, V9W 8C7",
    },
    BTW: {
        long_id: "brentwood-bay",
        address: "809 Verdier Avenue, Brentwood Bay, V8M 1C5",
    },
    DUK: {
        long_id: "nanaimo-duke-point",
        address: "400 Duke Point Highway, Nanaimo, V9X 1H6",
        res_open: 60,
        assured_open: 60,
    },
    PVB: {
        long_id: "mayne-island-village-bay",
        address: "Village Bay Road, Mayne Island , V0N 2J0",
        res_open: 60,
    },
    PLH: {
        long_id: "salt-spring-island-long-harbour",
        address: "1000 Long Harbour Rd, Salt Spring Island, V8K 2L8",
        res_open: 60,
    },
    BKY: {
        long_id: "buckley-bay",
        address: "6866 Island Highway, Fanny Bay, V0R 1W0",
    },
    KLE: {
        long_id: "klemtu",
        address: "Marine Drive, Swindle Island, V0T 1L0",
        res_open: 90,
    },
    HRN: {
        long_id: "hornby-island-shingle-spit",
        address: "Shingle Spit, 4000 Central Rd, Hornby Island, V0R 1Z0",
    },
    THT: {
        long_id: "thetis-island-preedy-harbour",
        address: "Preedy Harbour, Thetis Island, V0R 2Y0",
    },
    MIL: {
        long_id: "mill-bay",
        address: "Ferry Road, Mill Bay, V0R 2P4",
    },
    GAB: {
        long_id: "gabriola-island-descanso-bay",
        address: "350 North Road, Descanso Bay, Gabriola, V0R 1X2",
    },
    HRB: {
        long_id: "quadra-island-heriot-bay",
        address: "West Road, Heriot Bay, V9W 5E3",
    },
    NAN: {
        long_id: "nanaimo-departure-bay",
        address: "680 Trans-Canada Highway, Nanaimo, V9S 5R1",
        res_open: 120,
        assured_open: 60,
    },
    SOI: {
        long_id: "malcolm-island-sointula",
        address: "1st Street, Malcolm Island, V0N 3E0",
    },
    PEN: {
        long_id: "penelakut-island-telegraph-harbour",
        address: "Clam Bay Rd N, Penelakut Island, V0R 1K6",
    },
    KTS: {
        long_id: "keats-island-keats-landing",
        address: "Keats Road, Keats Island, Keats Island, V0N 1V0",
    },
    ALR: {
        long_id: "cormorant-island-alert-bay",
        address: "10 Fir Street, Alert Bay, V0N 1A0",
    },
    POF: {
        long_id: "ocean-falls",
        address: "Marine Drive, Ocean Falls, V0T 1P0",
    },
    HSB: {
        long_id: "vancouver-horseshoe-bay",
        address: "6750 Keith Rd , West Vancouver, V7W 2V1",
        res_open: 120,
        assured_open: 60,
    },
    BEC: {
        long_id: "bella-coola",
        address: "Chilcotin-Bella Coola Hwy, Bella Coola, V0T 1C0",
        res_open: 90,
        res_peak_extra: 30,
    },
    EAS: {
        long_id: "keats-island-eastbourne",
        address: "Esplanade Road, Keats Island, Keats Island, V0N 1V0",
    },
    QDR: {
        long_id: "quadra-island-quathiaski-cove",
        address: "Quathiaski Cove Road, Quathiaski Cove, V0P 1N0",
    },
    PPH: {
        long_id: "port-hardy-bear-cove",
        address: "6800 Highway 19, Port Hardy, V0N 2P0",
        res_open: 120,
    },
    PSB: {
        long_id: "galiano-island-sturdies-bay",
        address: "2622 Sturdies Bay Road, Galiano Island, V0N 1P0",
        res_open: 60,
    },
    PBB: {
        long_id: "bella-bella-mcloughlin-bay",
        address: "Waglisla , Bella Bella, V0T 1Z0",
        res_open: 120,
    },
    PPR: {
        long_id: "prince-rupert",
        address: "2000 Park Avenue, Prince Rupert, V8J 3S1",
        res_open: 120,
    },
    PST: {
        long_id: "saturna-island-lyall-harbour",
        address: "100 East Point Rd, Saturna Island, V0N 2Y0",
        res_open: 60,
    },
    PWR: {
        long_id: "powell-river-westview",
        address: "4465 Willingdon Avenue, Powell River, V8A 2M7",
        res_open: 60,
    },
    BOW: {
        long_id: "bowen-island-snug-cove",
        address: "Snug Cove,  Bowen Island, V0N 1G0",
    },
    CMX: {
        long_id: "comox-little-river",
        address: "1300 Ellenor Rd, Comox, V9M 4B3",
        res_open: 60,
    },
    CHM: {
        long_id: "chemainus",
        address: "2830 Oak Street, Chemainus, V0R 1K1",
    },
    MCN: {
        long_id: "port-mcneill",
        address: "1626 Beach Drive , Port McNeill, V0N 2R0",
    },
    VES: {
        long_id: "salt-spring-island-vesuvius-bay",
        address: "Vesuvius Bay Road, Salt Spring Island, V8K 1L6",
    },
    LNG: {
        long_id: "sunshine-coast-langdale",
        address: "1376 Port Mellon Highway, Langdale, V0N 1V0",
        res_open: 60,
    },
    ERL: {
        long_id: "sunshine-coast-earls-cove",
        address: "16550 Sunshine Coast Highway, Madeira Park, V0N 2H4",
    },
    TEX: {
        long_id: "texada-island-blubber-bay",
        address: "1000 Blubber Bay Road, Texada Island, V0N 3K0",
    },
    CFT: {
        long_id: "crofton",
        address: "1499 Chaplin Street, Crofton, V0R 1R0",
    },
};
