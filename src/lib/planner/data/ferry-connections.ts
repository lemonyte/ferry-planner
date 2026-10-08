import type { TerminalId } from "./locations";

export interface FerryConnection {
    bookable: boolean;
}

/** Ferry connections by origin, then destination. */
export const ferryConnections: {
    readonly [Origin in TerminalId]?: { readonly [Destination in TerminalId]?: FerryConnection };
} = {
    LNG: {
        HSB: { bookable: true },
    },
    KLE: {
        PBB: { bookable: true },
        PPH: { bookable: true },
        PPR: { bookable: true },
    },
    PSK: {
        PPR: { bookable: true },
        ALF: { bookable: false },
    },
    PPH: {
        BEC: { bookable: true },
        PBB: { bookable: true },
        PPR: { bookable: true },
        KLE: { bookable: true },
    },
    PVB: {
        TSA: { bookable: true },
        PST: { bookable: false },
        SWB: { bookable: false },
        PSB: { bookable: false },
        POB: { bookable: false },
        PLH: { bookable: false },
    },
    DNE: {
        HRN: { bookable: false },
    },
    ALF: {
        PSK: { bookable: false },
    },
    PWR: {
        CMX: { bookable: true },
        TEX: { bookable: false },
    },
    TSA: {
        DUK: { bookable: true },
        SWB: { bookable: true },
        PSB: { bookable: true },
        PVB: { bookable: true },
        POB: { bookable: true },
        PLH: { bookable: true },
        PST: { bookable: true },
    },
    ERL: {
        SLT: { bookable: false },
    },
    PBB: {
        KLE: { bookable: true },
        PPH: { bookable: true },
        PPR: { bookable: true },
        SHW: { bookable: true },
        BEC: { bookable: true },
        POF: { bookable: true },
    },
    FUL: {
        SWB: { bookable: false },
    },
    SOI: {
        MCN: { bookable: false },
        ALR: { bookable: false },
    },
    DUK: {
        TSA: { bookable: true },
    },
    CFT: {
        VES: { bookable: false },
    },
    BEC: {
        POF: { bookable: true },
        PPH: { bookable: true },
        PBB: { bookable: true },
    },
    CMX: {
        PWR: { bookable: true },
        TEX: { bookable: false },
    },
    QDR: {
        CAM: { bookable: false },
    },
    PPR: {
        PPH: { bookable: true },
        PBB: { bookable: true },
        PSK: { bookable: true },
        KLE: { bookable: true },
    },
    PSB: {
        SWB: { bookable: false },
        TSA: { bookable: true },
        PST: { bookable: false },
        PVB: { bookable: false },
        POB: { bookable: false },
        PLH: { bookable: false },
    },
    PST: {
        SWB: { bookable: false },
        TSA: { bookable: true },
        PSB: { bookable: false },
        PVB: { bookable: false },
        POB: { bookable: false },
    },
    HSB: {
        LNG: { bookable: true },
        BOW: { bookable: false },
        NAN: { bookable: true },
    },
    MCN: {
        ALR: { bookable: false },
        SOI: { bookable: false },
    },
    SHW: {
        POF: { bookable: true },
        PBB: { bookable: true },
    },
    POB: {
        PLH: { bookable: false },
        PVB: { bookable: false },
        TSA: { bookable: true },
        SWB: { bookable: false },
        PST: { bookable: false },
        PSB: { bookable: false },
    },
    ALR: {
        MCN: { bookable: false },
        SOI: { bookable: false },
    },
    CHM: {
        THT: { bookable: false },
        PEN: { bookable: false },
    },
    BKY: {
        DNM: { bookable: false },
    },
    GAB: {
        NAH: { bookable: false },
    },
    PLH: {
        TSA: { bookable: true },
        SWB: { bookable: false },
        PSB: { bookable: false },
        PVB: { bookable: false },
        POB: { bookable: false },
    },
    CAM: {
        QDR: { bookable: false },
    },
    SWB: {
        TSA: { bookable: true },
        PSB: { bookable: false },
        PVB: { bookable: false },
        POB: { bookable: false },
        FUL: { bookable: false },
        PST: { bookable: false },
    },
    MIL: {
        BTW: { bookable: false },
    },
    NAN: {
        HSB: { bookable: true },
    },
    TEX: {
        CMX: { bookable: false },
        PWR: { bookable: false },
    },
    NAH: {
        GAB: { bookable: false },
    },
    DNM: {
        BKY: { bookable: false },
    },
    THT: {
        PEN: { bookable: false },
        CHM: { bookable: false },
    },
    VES: {
        CFT: { bookable: false },
    },
    PEN: {
        CHM: { bookable: false },
        THT: { bookable: false },
    },
    HRB: {
        COR: { bookable: false },
    },
    BTW: {
        MIL: { bookable: false },
    },
    SLT: {
        ERL: { bookable: false },
    },
    HRN: {
        DNE: { bookable: false },
    },
    POF: {
        PBB: { bookable: true },
        BEC: { bookable: true },
        SHW: { bookable: true },
    },
};
