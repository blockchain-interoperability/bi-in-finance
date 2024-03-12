struct TtlIntrBkSttlmAmt {
    string Ccy;
    Amt Amt;
}

struct SchmeNm {
    string Cd;
    Prtry Prtry;
}

struct Othr {
    string ChanlTp;
    Id Id;
}

struct Id {
    OrgId OrgId;
    PrvtId PrvtId;
}

struct Tp {
    CdOrPrtry CdOrPrtry;
    string Issr;
}

struct Prxy {
    Tp Tp;
    Id Id;
}

struct SttlmAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct ClrSys {
    string Cd;
    Prtry Prtry;
}

struct ClrSysId {
    string Cd;
    Prtry Prtry;
}

struct ClrSysMmbId {
    ClrSysId ClrSysId;
    string MmbId;
}

struct Prtry {
    Id Id;
    string Issr;
    SchmeNm SchmeNm;
}

struct AdrTp {
    string Cd;
    Prtry Prtry;
}

struct PstlAdr {
    AdrTp AdrTp;
    string Dept;
    string SubDept;
    string StrtNm;
    string BldgNb;
    string BldgNm;
    string Flr;
    string PstBx;
    string Room;
    string PstCd;
    string TwnNm;
    string TwnLctnNm;
    string DstrctNm;
    string CtrySubDvsn;
    string Ctry;
    string AdrLine;
}

struct FinInstnId {
    string BICFI;
    ClrSysMmbId ClrSysMmbId;
    string LEI;
    string Nm;
    PstlAdr PstlAdr;
    Othr Othr;
}

struct BrnchId {
    Id Id;
    string LEI;
    string Nm;
    PstlAdr PstlAdr;
}

struct InstgRmbrsmntAgt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct InstgRmbrsmntAgtAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct InstdRmbrsmntAgt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct InstdRmbrsmntAgtAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct ThrdRmbrsmntAgt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct ThrdRmbrsmntAgtAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct SttlmInf {
    string SttlmMtd;
    SttlmAcct SttlmAcct;
    ClrSys ClrSys;
    InstgRmbrsmntAgt InstgRmbrsmntAgt;
    InstgRmbrsmntAgtAcct InstgRmbrsmntAgtAcct;
    InstdRmbrsmntAgt InstdRmbrsmntAgt;
    InstdRmbrsmntAgtAcct InstdRmbrsmntAgtAcct;
    ThrdRmbrsmntAgt ThrdRmbrsmntAgt;
    ThrdRmbrsmntAgtAcct ThrdRmbrsmntAgtAcct;
}

struct SvcLvl {
    string Cd;
    Prtry Prtry;
}

struct LclInstrm {
    string Cd;
    Prtry Prtry;
}

struct CtgyPurp {
    string Cd;
    Prtry Prtry;
}

struct PmtTpInf {
    string InstrPrty;
    string ClrChanl;
    SvcLvl SvcLvl;
    LclInstrm LclInstrm;
    CtgyPurp CtgyPurp;
}

struct InstgAgt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct InstdAgt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct GrpHdr {
    string MsgId;
    string CreDtTm;
    string BtchBookg;
    string NbOfTxs;
    string CtrlSum;
    TtlIntrBkSttlmAmt TtlIntrBkSttlmAmt;
    string IntrBkSttlmDt;
    SttlmInf SttlmInf;
    PmtTpInf PmtTpInf;
    InstgAgt InstgAgt;
    InstdAgt InstdAgt;
}

struct PmtId {
    string InstrId;
    string EndToEndId;
    string TxId;
    string UETR;
    string ClrSysRef;
}

struct IntrBkSttlmAmt {
    string Ccy;
    Amt Amt;
}

struct SttlmTmIndctn {
    string DbtDtTm;
    string CdtDtTm;
}

struct SttlmTmReq {
    string CLSTm;
    string TillTm;
    string FrTm;
    string RjctTm;
}

struct InstdAmt {
    string Ccy;
    Amt Amt;
}

struct Amt {
    string Ccy;
    Amt Amt;
}

struct Agt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct ChrgsInf {
    Amt Amt;
    Agt Agt;
    Tp Tp;
}

struct Clssfctn {
    string Cd;
    Prtry Prtry;
}

struct Prd {
    string Yr;
    Tp Tp;
    FrToDt FrToDt;
}

struct PtInTm {
    Tp Tp;
    PtInTm PtInTm;
}

struct Frqcy {
    Tp Tp;
    Prd Prd;
    PtInTm PtInTm;
}

struct Rsn {
    string Cd;
    Prtry Prtry;
}

struct MndtRltdInf {
    string MndtId;
    Tp Tp;
    string DtOfSgntr;
    string DtOfVrfctn;
    string ElctrncSgntr;
    string FrstPmtDt;
    string FnlPmtDt;
    Frqcy Frqcy;
    Rsn Rsn;
}

struct PrvsInstgAgt1 {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct PrvsInstgAgt1Acct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct PrvsInstgAgt2 {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct PrvsInstgAgt2Acct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct PrvsInstgAgt3 {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct PrvsInstgAgt3Acct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct IntrmyAgt1 {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct IntrmyAgt1Acct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct IntrmyAgt2 {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct IntrmyAgt2Acct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct IntrmyAgt3 {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct IntrmyAgt3Acct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct OrgId {
    string AnyBIC;
    string LEI;
    Othr Othr;
}

struct DtAndPlcOfBirth {
    string BirthDt;
    string PrvcOfBirth;
    string CityOfBirth;
    string CtryOfBirth;
}

struct PrvtId {
    DtAndPlcOfBirth DtAndPlcOfBirth;
    Othr Othr;
}

struct CtctDtls {
    string NmPrfx;
    string Nm;
    string PhneNb;
    string MobNb;
    string FaxNb;
    string EmailAdr;
    string EmailPurp;
    string JobTitl;
    string Rspnsblty;
    string Dept;
    Othr Othr;
    string PrefrdMtd;
}

struct UltmtDbtr {
    string TaxId;
    string RegnId;
    string TaxTp;
    Authstn Authstn;
}

struct InitgPty {
    string Nm;
    PstlAdr PstlAdr;
    Id Id;
    string CtryOfRes;
    CtctDtls CtctDtls;
}

struct Dbtr {
    string TaxId;
    string RegnId;
    string TaxTp;
    Authstn Authstn;
}

struct DbtrAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct DbtrAgt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct DbtrAgtAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct CdtrAgt {
    FinInstnId FinInstnId;
    BrnchId BrnchId;
}

struct CdtrAgtAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct Cdtr {
    string TaxId;
    string RegnId;
    string TaxTp;
}

struct CdtrAcct {
    Id Id;
    Tp Tp;
    string Ccy;
    string Nm;
    Prxy Prxy;
}

struct UltmtCdtr {
    string Nm;
    PstlAdr PstlAdr;
    Id Id;
    string CtryOfRes;
    CtctDtls CtctDtls;
}

struct InstrForCdtrAgt {
    string Cd;
    string InstrInf;
}

struct InstrForNxtAgt {
    string Cd;
    string InstrInf;
}

struct Purp {
    string Cd;
    Prtry Prtry;
}

struct Authrty {
    string Nm;
    string Ctry;
}

struct Dtls {
    Prd Prd;
    Amt Amt;
}

struct RgltryRptg {
    string DbtCdtRptgInd;
    Authrty Authrty;
    Dtls Dtls;
}

struct Authstn {
    string Titl;
    string Nm;
}

struct TtlTaxblBaseAmt {
    string Ccy;
    Amt Amt;
}

struct TtlTaxAmt {
    string Ccy;
    Amt Amt;
}

struct FrToDt {
    string FrDt;
    string ToDt;
}

struct TaxblBaseAmt {
    string Ccy;
    Amt Amt;
}

struct TtlAmt {
    string Ccy;
    Amt Amt;
}

struct TaxAmt {
    string Rate;
    TaxblBaseAmt TaxblBaseAmt;
    TtlAmt TtlAmt;
    Dtls Dtls;
}

struct Rcrd {
    Tp Tp;
    string Ctgy;
    string CtgyDtls;
    string DbtrSts;
    string CertId;
    string FrmsCd;
    Prd Prd;
    TaxAmt TaxAmt;
    string AddtlInf;
}

struct Tax {
    Cdtr Cdtr;
    Dbtr Dbtr;
    string AdmstnZone;
    string RefNb;
    string Mtd;
    TtlTaxblBaseAmt TtlTaxblBaseAmt;
    TtlTaxAmt TtlTaxAmt;
    string Dt;
    string SeqNb;
    Rcrd Rcrd;
}

struct Adr {
    AdrTp AdrTp;
    string Dept;
    string SubDept;
    string StrtNm;
    string BldgNb;
    string BldgNm;
    string Flr;
    string PstBx;
    string Room;
    string PstCd;
    string TwnNm;
    string TwnLctnNm;
    string DstrctNm;
    string CtrySubDvsn;
    string Ctry;
    string AdrLine;
}

struct RmtLctnDtls {
    string Mtd;
    string ElctrncAdr;
    PstlAdr PstlAdr;
}

struct RltdRmtInf {
    string RmtId;
    RmtLctnDtls RmtLctnDtls;
}

struct CdOrPrtry {
    string Cd;
    Prtry Prtry;
}

struct DuePyblAmt {
    string Ccy;
    Amt Amt;
}

struct DscntApldAmt {
    Tp Tp;
    Amt Amt;
}

struct CdtNoteAmt {
    string Ccy;
    Amt Amt;
}

struct AdjstmntAmtAndRsn {
    Amt Amt;
    string CdtDbtInd;
    Rsn Rsn;
    string AddtlInf;
}

struct RmtdAmt {
    string Ccy;
    Amt Amt;
}

struct LineDtls {
    Id Id;
    string Desc;
    Amt Amt;
}

struct RfrdDocInf {
    Tp Tp;
    string Nb;
    string RltdDt;
    LineDtls LineDtls;
}

struct RfrdDocAmt {
    DuePyblAmt DuePyblAmt;
    DscntApldAmt DscntApldAmt;
    CdtNoteAmt CdtNoteAmt;
    TaxAmt TaxAmt;
    AdjstmntAmtAndRsn AdjstmntAmtAndRsn;
    RmtdAmt RmtdAmt;
}

struct CdtrRefInf {
    Tp Tp;
    string Ref;
}

struct Invcr {
    string Nm;
    PstlAdr PstlAdr;
    Id Id;
    string CtryOfRes;
    CtctDtls CtctDtls;
}

struct Invcee {
    string Nm;
    PstlAdr PstlAdr;
    Id Id;
    string CtryOfRes;
    CtctDtls CtctDtls;
}

struct TaxRmt {
    Cdtr Cdtr;
    Dbtr Dbtr;
    UltmtDbtr UltmtDbtr;
    string AdmstnZone;
    string RefNb;
    string Mtd;
    TtlTaxblBaseAmt TtlTaxblBaseAmt;
    TtlTaxAmt TtlTaxAmt;
    string Dt;
    string SeqNb;
    Rcrd Rcrd;
}

struct Grnshee {
    string Nm;
    PstlAdr PstlAdr;
    Id Id;
    string CtryOfRes;
    CtctDtls CtctDtls;
}

struct GrnshmtAdmstr {
    string Nm;
    PstlAdr PstlAdr;
    Id Id;
    string CtryOfRes;
    CtctDtls CtctDtls;
}

struct GrnshmtRmt {
    Tp Tp;
    Grnshee Grnshee;
    GrnshmtAdmstr GrnshmtAdmstr;
    string RefNb;
    string Dt;
    RmtdAmt RmtdAmt;
    string FmlyMdclInsrncInd;
    string MplyeeTermntnInd;
}

struct Strd {
    RfrdDocInf RfrdDocInf;
    RfrdDocAmt RfrdDocAmt;
    CdtrRefInf CdtrRefInf;
    Invcr Invcr;
    Invcee Invcee;
    TaxRmt TaxRmt;
    GrnshmtRmt GrnshmtRmt;
    string AddtlRmtInf;
}

struct RmtInf {
    string Ustrd;
    Strd Strd;
}

struct SplmtryData {
    string PlcAndNm;
    string Envlp;
}

struct CdtTrfTxInf {
    PmtId PmtId;
    PmtTpInf PmtTpInf;
    IntrBkSttlmAmt IntrBkSttlmAmt;
    string IntrBkSttlmDt;
    string SttlmPrty;
    SttlmTmIndctn SttlmTmIndctn;
    SttlmTmReq SttlmTmReq;
    string AccptncDtTm;
    string PoolgAdjstmntDt;
    InstdAmt InstdAmt;
    string XchgRate;
    string ChrgBr;
    ChrgsInf ChrgsInf;
    MndtRltdInf MndtRltdInf;
    PrvsInstgAgt1 PrvsInstgAgt1;
    PrvsInstgAgt1Acct PrvsInstgAgt1Acct;
    PrvsInstgAgt2 PrvsInstgAgt2;
    PrvsInstgAgt2Acct PrvsInstgAgt2Acct;
    PrvsInstgAgt3 PrvsInstgAgt3;
    PrvsInstgAgt3Acct PrvsInstgAgt3Acct;
    InstgAgt InstgAgt;
    InstdAgt InstdAgt;
    IntrmyAgt1 IntrmyAgt1;
    IntrmyAgt1Acct IntrmyAgt1Acct;
    IntrmyAgt2 IntrmyAgt2;
    IntrmyAgt2Acct IntrmyAgt2Acct;
    IntrmyAgt3 IntrmyAgt3;
    IntrmyAgt3Acct IntrmyAgt3Acct;
    UltmtDbtr UltmtDbtr;
    InitgPty InitgPty;
    Dbtr Dbtr;
    DbtrAcct DbtrAcct;
    DbtrAgt DbtrAgt;
    DbtrAgtAcct DbtrAgtAcct;
    CdtrAgt CdtrAgt;
    CdtrAgtAcct CdtrAgtAcct;
    Cdtr Cdtr;
    CdtrAcct CdtrAcct;
    UltmtCdtr UltmtCdtr;
    InstrForCdtrAgt InstrForCdtrAgt;
    InstrForNxtAgt InstrForNxtAgt;
    Purp Purp;
    RgltryRptg RgltryRptg;
    Tax Tax;
    RltdRmtInf RltdRmtInf;
    RmtInf RmtInf;
    SplmtryData SplmtryData;
}

struct FIToFICstmrCdtTrf {
    GrpHdr GrpHdr;
    CdtTrfTxInf CdtTrfTxInf;
    SplmtryData SplmtryData;
}

