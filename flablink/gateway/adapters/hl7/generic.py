# -*- coding: utf-8 -*-

from flablink.gateway.adapters.hl7.base import  HL7BaseAdapter


class GenericHl7Adapter(HL7BaseAdapter):
    """Adapter HL7 messages"""

    def __init__(self, message):
        super(GenericHl7Adapter, self).__init__(message)

    @property
    def header_record(self):
        """
        Returns a dict that represents the header of the message
        """
        # MSH|^~\&|COBAS6800/8800||LIS||20230123104355||OUL^R22|13968052-baa9-474c-91bb-f7cf19d988fe|P|2.5||||||ASCII
        message_type = self.get_field(self.raw_header_record, 8)
        return {
            "RecordTypeId": self.get_field(self.raw_header_record, 0),
            "FieldDelimiter": self.field_delimiter,
            "RepeatDelimiter": self.repeat_delimiter,
            "ComponentDelimiter": self.component_delimiter,
            "SubComponentDelimiter": self.sub_component_delimiter,
            "EscapeDelimiter": self.escape_delimiter,
            "SendingApplication": self.get_field(self.raw_header_record, 2),
            "ReceivingApplication": self.get_field(self.raw_header_record, 4),
            "DateTimeOfMessage": self.get_field(self.raw_header_record, 6),
            "MesageCode": self.get_component(message_type, 0),
            "TriggerEvent": self.get_component(message_type, 1),
            "MessageControlId": self.get_field(self.raw_header_record, 9),
            "ProcessingId": self.get_field(self.raw_header_record, 10),
            "VersionId": self.get_field(self.raw_header_record, 11),
            "CharacterSet": self.get_field(self.raw_header_record, 17),
        }

    @property
    def patient_record(self):
        return {}

    @property
    def specimen_record(self):
        # SPM||BP23-04444||PLAS^plasma^HL70487|||||||P||||||||||||||||
        specimen_type = self.get_field(self.raw_specimen_record, 4)
        return {
            "RecordTypeId": self.get_field(self.raw_specimen_record, 0),
            "SpecimenId": self.get_field(self.raw_specimen_record, 2),
            "SpecimenTypeIdentifier": self.get_component(specimen_type, 0),
            "SpecimenTypeText": self.get_component(specimen_type, 1),
            "SpecimenTypeCoding": self.get_component(specimen_type, 2),
            "SpecimenRole": self.get_field(self.raw_specimen_record, 11),
        }
    
    @property
    def specimen_container_record(self):
        # SAC|||BP24-33200|||||||A097802|12||||12^Position^99ABT
        return {
            "ContainerIdentifier": self.get_field(self.raw_specimen_container_record, 3),
        }

    @property
    def observation_request_record(self):
        # OBR|1|||70241-5^HIV^LN|||||||A
        universal_service = self.get_field(
            self.raw_observation_request_record, 4)
        return {
            "RecordTypeId": self.get_field(self.raw_observation_request_record, 0),
            "UniversalServiceIdentifier": self.get_component(universal_service, 0),
            "UniversalServiceText": self.get_component(universal_service, 1),
            "UniversalServiceCoding": self.get_component(universal_service, 2),
            "SpecimenActionCode": self.get_field(self.raw_observation_request_record, 11),
        }

    @property
    def test_code_record(self):
        # TCD|70241-5^HIV^LN|^1^:^0
        universal_service = self.get_field(
            self.raw_test_code_record, 1)
        return {
            "RecordTypeId": self.get_field(self.raw_test_code_record, 0),
            "UniversalServiceIdentifier": self.get_component(universal_service, 0),
            "UniversalServiceText": self.get_component(universal_service, 1),
            "UniversalServiceCoding": self.get_component(universal_service, 2),
            "AutoDilutionFactor": self.get_field(self.raw_test_code_record, 2),
        }

    def get_result_metadata(self, record):
        # OBX|1|ST|HIV^HIV^99ROC||ValueNotSet|||BT|||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
        # OBX|2|NA|HIV^HIV^99ROC^S_OTHER^Other Supplemental^IHELAW||41.47^^37.53||||||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
        # OBX|3|ST|70241-5^HIV^LN|1/1|ValueNotSet|||RR|||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
        # OBX|4|ST|70241-5^HIV^LN|1/2|< Titer min|||""|||F|||||Lyna||C6800/8800^Roche^^~Unknown^Roche^^~ID_000000000012076380^IM300-002765^^|20230120144614|||||||||386_neg^^99ROC~385_pos^^99ROC
        # OBX|1|ST|1006^HIV-1^99ABT||Not Detected|||""|||F|||||Funkydee~Admin||Alinity m^Abbott~M01143^Abbott~1^Abbott~10^Abbott|20240517174741||||||||||RSLT

        manufacturer = self.get_record_component(record, 18, 1)
        model = self.get_record_component(record, 18, 0)
        return {
            "RecordTypeId": self.get_field(record, 0),
            "ValueType": self.get_field(record, 2),
            "ObservationSubID": self.get_field(record, 4),
            "ObservationValue": self.get_field(record, 5),
            "Units": self.get_field(record, 6),
            "ReferenceRange": self.get_field(record, 7),
            "AbnormalFlags": self.get_field(record, 8),
            "ObservationResultStatus": self.get_field(record, 11),
            "ResponsibleObserver": self.get_field(record, 16),
            "DateTimeofAnalysis": self.get_field(record, 19),
            "EquipmentInstanceIdentifier": f"{model}:{manufacturer}"
        }

    def resolve_final_result_record(self, records):
        """Returns the result record (raw) to be considered as the final result
        """
        if isinstance(records, dict):
            return records

        if len(records) == 1:
            return self.get_result_metadata(records[0])

        for record in records:
            meta = self.get_result_metadata(record)
            if self.is_final_result(meta):
                if meta["ObservationValue"] == "Titer":
                    return self.get_result_metadata(records[0])
                return meta

        return self.get_result_metadata(records[0])

    def is_final_result(self, meta_result):
        """Returns whether a (R)sult record must be considered as the final result or not
        """
        if meta_result["ObservationSubID"] == "1/2":
            return True
        return False

    @property
    def observation_record(self):
        return self.resolve_final_result_record(self.raw_observation_record)

    def is_supported(self):
        """Returns whether the current adapter supports the given message
        """
        return True

    def read(self):
        """Returns a list of ASTMDataResult objects
        """
        id = self.specimen_record["SpecimenId"]
        if not id:
            id = self.specimen_container_record["ContainerIdentifier"]
        
        keyword = self.test_code_record["UniversalServiceText"]
        if not keyword:
            keyword = self.observation_request_record["UniversalServiceText"]

        data = {}
        data["id"] = id
        data["keyword"] = keyword
        data["result"] = self.observation_record["ObservationValue"]
        data["instrument"] = self.observation_record["EquipmentInstanceIdentifier"]
        data["capture_date"] = self.observation_record["DateTimeofAnalysis"]
        data["raw_message"] = self.message
        return [data]
