from flablink.gateway.services.transformer import Transformer


def trial():
    msg = """
    H|\^&|||m2000^8.1.9.0^275022112^H1P1O1R1C1L1|||||||P|1|20190903162134
    P|1
    O|1|DBS19-002994|DBS19-002994^WS19-2459^D1|^^^HIV1mlDBS^HIV1.0mlDBS|||||||||||||||||||||F
    R|1|^^^HIV1mlDBS^HIV1.0mlDBS^489932^11790271^^F|< 839|Copies / mL||||R||naralabs^naralabs||20190902191654|275022112
    R|2|^^^HIV1mlDBS^HIV1.0mlDBS^489932^11790271^^I|Detected|||||R||naralabs^naralabs||20190902191654|275022112
    R|3|^^^HIV1mlDBS^HIV1.0mlDBS^489932^11790271^^P|28.21|cycle number||||R||naralabs^naralabs||20190902191654|275022112
    """
    Transformer().transform_message(msg)


def hl7Try():
    hl_mess = """
    MSH|^~\&|COBAS6800/8800||LIS||20230123104355||OUL^R22|13968052-baa9-474c-91bb-f7cf19d988fe|P|2.5||||||ASCII
    SPM||BP23-04444||PLAS^plasma^HL70487|||||||P||||||||||||||||
    SAC|||||||||||||||||||||500|||uL^^UCUM
    OBR|1|||70241-5^HIV^LN|||||||A
    OBX|1|ST|HIV^HIV^99ROC||ValueNotSet|||BT|||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
    TCD|70241-5^HIV^LN|^1^:^0
    OBX|2|NA|HIV^HIV^99ROC^S_OTHER^Other Supplemental^IHELAW||41.47^^37.53||||||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
    OBX|3|ST|70241-5^HIV^LN|1/1|ValueNotSet|||RR|||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
    OBX|4|ST|70241-5^HIV^LN|1/2|< Titer min|||""|||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
    TCD|70241-5^HIV^LN|^1^:^0
    """
    Transformer().transform_message(hl_mess)


def hpvTry():
    ms = """
    H|\^&|||Panther|||||Host||P|1|
    P|5||||^^|||||||||||^|^|||||||||||||||^|^|
    O|1|CS23-22443|cc72d06c-87de-463c-ad08-275211789126^451167|^^^HPV^HPV^^1|R|20230222142246|||||||||||||||||||F
    R|1|^^^HPV^ICRLU^^1|181107|||||F\R||||20230222192433|
    R|2|^^^HPV^ICInterpretation^^1|Valid|||||F\R||||20230222192433|
    R|3|^^^HPV^AnalyteRLU^^1|2746489|||||F\R||||20230222192433|
    R|4|^^^HPV^AnalyteSCO^^1|20.07|||||F\R||||20230222192433|
    R|5|^^^HPV^OverallInterpretation^^1|POSITIVE|||||F\R||||20230222192433|
    R|6|^^^HPV^Analyte Cutoff^^1||||||F\R||||20230222192433|
    R|7|^^^HPV^IC Cutoff^^1||||||F\R||||20230222192433|
    L|1|N
    """
    Transformer().transform_message(ms)


def err():
    ms = """
    H|\^&|||m2000^8.1.9.0^275022096^H1P1O1R1C1L1|||||||P|1|20230717163415
    P|1
    O|1|DB&E&23-33E22|DB&E&23-33E22^WS23-11684^D2|^^^HIV1mlDBS^HIV1.0mlDBS|||||||||||||||||||||F
    R|1|^^^HIV1mlDBS^HIV1.0mlDBS^381303^10003187^^F|Not detected|Copies / mL||||R||BRIAN PAKARIMWA^BRIAN PAKARIMWA||20230713214311|275022096
    R|2|^^^HIV1mlDBS^HIV1.0mlDBS^381303^10003187^^I|Target not detected|||||R||BRIAN PAKARIMWA^BRIAN PAKARIMWA||20230713214311|275022096
    R|3|^^^HIV1mlDBS^HIV1.0mlDBS^381303^10003187^^P|-1.00|cycle number||||R||BRIAN PAKARIMWA^BRIAN PAKARIMWA||20230713214311|275022096
    L|1
    """
    Transformer().transform_message(ms)


if __name__ == "__main__":
    hpvTry()
    err()
    hl7Try()
    trial()