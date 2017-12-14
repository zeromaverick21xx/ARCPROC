#~ db_alma = """almasu/alma4dba@(DESCRIPTION=
      #~ (LOAD_BALANCE=on)
      #~ (ADDRESS_LIST=
        #~ (ADDRESS = (PROTOCOL = TCP)(HOST = oracl1-vip.osf.alma.cl)(PORT = 1521))
        #~ (ADDRESS = (PROTOCOL = TCP)(HOST = oracl2-vip.osf.alma.cl)(PORT = 1521))
        #~ (ADDRESS = (PROTOCOL = TCP)(HOST = oracl3-vip.osf.alma.cl)(PORT = 1521))
        #~ (ADDRESS = (PROTOCOL = TCP)(HOST = oracl4-vip.osf.alma.cl)(PORT = 1521)))
      #~ (CONNECT_DATA=(SERVICE_NAME=ALMA.OSF.CL))
      #~ (FAILOVER_MODE=(TYPE=SELECT)(METHOD=BASIC))
#~ )"""


db_alma = """almasu/alma4dba@
    (DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = ora.sco.alma.cl)(PORT = 1521))
    (CONNECT_DATA =
    (SERVER = DEDICATED)
    (SERVICE_NAME = OFFLINE.SCO.CL)
     )
    )    
    """

db_apo05 = '''alma/alma$dba@(DESCRIPTION =(ADDRESS = (PROTOCOL = TCP)(HOST = apo05.osf.alma.cl)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = apo05.osf.alma.cl)))'''

db_testbench = '''alma/alma$dba@(DESCRIPTION =
    (ADDRESS = (PROTOCOL = TCP)(HOST = tb-s1-oracle1.osf.alma.cl)(PORT = 1521))
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = ALMA.OSF.CL)
    ))

'''

#db = "alma3/alma$dba@tfeng-arc.aiv.alma.cl:1521/ALMA.ESO.ORG"


oradict = {
        "ACAPolarization": "XML_ACAPOLARIZATION_ENTITIES",
        "AccumMode": "XML_ACCUMMODE_ENTITIES",
        "ACSAlarmMessage": "XML_ACSALARMMESSAGE_ENTITIES",
        "AcsCommandCenterProject": "XML_ACSCOMMANDCENTERP_ENTITIES",
        "AcsCommandCenterTools": "XML_ACSCOMMANDCENTERT_ENTITIES",
        "ACSError": "XML_ACSERROR_ENTITIES",
        "ACSLogTS": "XML_ACSLOGTS_ENTITIES",
        "Address": "XML_ADDRESS_ENTITIES",
        "AlmaRadiometerTable": "XML_ALMARADIOMETERTAB_ENTITIES",
        "AnnotationTable": "XML_ANNOTATIONTABLE_ENTITIES",
        "AntennaMake": "XML_ANTENNAMAKE_ENTITIES",
        "AntennaMotionPattern": "XML_ANTENNAMOTIONPATT_ENTITIES",
        "AntennaTable": "XML_ANTENNATABLE_ENTITIES",
        "AntennaType": "XML_ANTENNATYPE_ENTITIES",
        "ASDM": "XML_ASDM_ENTITIES",
        "ASDMBinaryTable": "XML_ASDMBINARYTABLE_ENTITIES",
        "ASIConfiguration": "XML_ASICONFIGURATION_ENTITIES",
        "ASIMessage": "XML_ASIMESSAGE_ENTITIES",
        "AssociatedCalNature": "XML_ASSOCIATEDCALNATU_ENTITIES",
        "AssociatedFieldNature": "XML_ASSOCIATEDFIELDNA_ENTITIES",
        "AtmPhaseCorrection": "XML_ATMPHASECORRECTIO_ENTITIES",
        "AxisName": "XML_AXISNAME_ENTITIES",
        "BasebandName": "XML_BASEBANDNAME_ENTITIES",
        "BaselineReferenceCode": "XML_BASELINEREFERENCE_ENTITIES",
        "bulkTest": "XML_BULKTEST_ENTITIES",
        "CalAmpliTable": "XML_CALAMPLITABLE_ENTITIES",
        "CalAtmosphereTable": "XML_CALATMOSPHERETABL_ENTITIES",
        "CalBandpassTable": "XML_CALBANDPASSTABLE_ENTITIES",
        "CalCurveTable": "XML_CALCURVETABLE_ENTITIES",
        "CalCurveType": "XML_CALCURVETYPE_ENTITIES",
        "CalDataOrigin": "XML_CALDATAORIGIN_ENTITIES",
        "CalDataTable": "XML_CALDATATABLE_ENTITIES",
        "CalDelayTable": "XML_CALDELAYTABLE_ENTITIES",
        "CalDeviceTable": "XML_CALDEVICETABLE_ENTITIES",
        "CalFluxTable": "XML_CALFLUXTABLE_ENTITIES",
        "CalFocusModelTable": "XML_CALFOCUSMODELTABL_ENTITIES",
        "CalFocusTable": "XML_CALFOCUSTABLE_ENTITIES",
        "CalGainTable": "XML_CALGAINTABLE_ENTITIES",
        "CalHolographyTable": "XML_CALHOLOGRAPHYTABL_ENTITIES",
        "CalibrationDevice": "XML_CALIBRATIONDEVICE_ENTITIES",
        "CalibrationFunction": "XML_CALIBRATIONFUNCTI_ENTITIES",
        "CalibrationMode": "XML_CALIBRATIONMODE_ENTITIES",
        "CalibrationSet": "XML_CALIBRATIONSET_ENTITIES",
        "CalPhaseTable": "XML_CALPHASETABLE_ENTITIES",
        "CalPointingModelTable": "XML_CALPOINTINGMODELT_ENTITIES",
        "CalPointingTable": "XML_CALPOINTINGTABLE_ENTITIES",
        "CalPositionTable": "XML_CALPOSITIONTABLE_ENTITIES",
        "CalPrimaryBeamTable": "XML_CALPRIMARYBEAMTAB_ENTITIES",
        "CalQueryParameters": "XML_CALQUERYPARAMETER_ENTITIES",
        "CalReductionTable": "XML_CALREDUCTIONTABLE_ENTITIES",
        "CalSeeingTable": "XML_CALSEEINGTABLE_ENTITIES",
        "CalType": "XML_CALTYPE_ENTITIES",
        "CalWVRTable": "XML_CALWVRTABLE_ENTITIES",
        "CommonEntity": "XML_COMMONENTITY_ENTITIES",
        "commontypes": "XML_COMMONTYPES_ENTITIES",
        "ConfigDescriptionTable": "XML_CONFIGDESCRIPTION_ENTITIES",
        "CorrelationBit": "XML_CORRELATIONBIT_ENTITIES",
        "CorrelationMode": "XML_CORRELATIONMODE_ENTITIES",
        "CorrelatorCalibration": "XML_CORRELATORCALIBRA_ENTITIES",
        "CorrelatorModeTable": "XML_CORRELATORMODETAB_ENTITIES",
        "CorrelatorName": "XML_CORRELATORNAME_ENTITIES",
        "CorrelatorType": "XML_CORRELATORTYPE_ENTITIES",
        "DataContent": "XML_DATACONTENT_ENTITIES",
        "DataDescriptionTable": "XML_DATADESCRIPTIONTA_ENTITIES",
        "DataScale": "XML_DATASCALE_ENTITIES",
        "DelayModelTable": "XML_DELAYMODELTABLE_ENTITIES",
        "DetectorBandType": "XML_DETECTORBANDTYPE_ENTITIES",
        "DirectionReferenceCode": "XML_DIRECTIONREFERENC_ENTITIES",
        "DopplerReferenceCode": "XML_DOPPLERREFERENCEC_ENTITIES",
        "DopplerTable": "XML_DOPPLERTABLE_ENTITIES",
        "DopplerTrackingMode": "XML_DOPPLERTRACKINGMO_ENTITIES",
        "EphemerisTable": "XML_EPHEMERISTABLE_ENTITIES",
        "ExecBlockTable": "XML_EXECBLOCKTABLE_ENTITIES",
        "ExecConfig": "XML_EXECCONFIG_ENTITIES",
        "FeedTable": "XML_FEEDTABLE_ENTITIES",
        "FieldCode": "XML_FIELDCODE_ENTITIES",
        "FieldTable": "XML_FIELDTABLE_ENTITIES",
        "FilterMode": "XML_FILTERMODE_ENTITIES",
        "FlagCmdTable": "XML_FLAGCMDTABLE_ENTITIES",
        "FlagTable": "XML_FLAGTABLE_ENTITIES",
        "FluxCalibrationMethod": "XML_FLUXCALIBRATIONME_ENTITIES",
        "FocusMethod": "XML_FOCUSMETHOD_ENTITIES",
        "FocusModelTable": "XML_FOCUSMODELTABLE_ENTITIES",
        "FocusTable": "XML_FOCUSTABLE_ENTITIES",
        "FreqOffsetTable": "XML_FREQOFFSETTABLE_ENTITIES",
        "FrequencyReferenceCode": "XML_FREQUENCYREFERENC_ENTITIES",
        "GainTrackingTable": "XML_GAINTRACKINGTABLE_ENTITIES",
        "HistoryTable": "XML_HISTORYTABLE_ENTITIES",
        "HolographyChannelType": "XML_HOLOGRAPHYCHANNEL_ENTITIES",
        "HolographyTable": "XML_HOLOGRAPHYTABLE_ENTITIES",
        "IdentifierRange": "XML_IDENTIFIERRANGE_ENTITIES",
        "InvalidatingCondition": "XML_INVALIDATINGCONDI_ENTITIES",
        "loggingMI": "XML_LOGGINGMI_ENTITIES",
        "MainTable": "XML_MAINTABLE_ENTITIES",
        "NetSideband": "XML_NETSIDEBAND_ENTITIES",
        "ObsAttachment": "XML_OBSATTACHMENT_ENTITIES",
        "ObservationTable": "XML_OBSERVATIONTABLE_ENTITIES",
        "ObservingControlScript": "XML_OBSERVINGCONTROLS_ENTITIES",
        "ObservingMode": "XML_OBSERVINGMODE_ENTITIES",
        "ObsProject": "XML_OBSPROJECT_ENTITIES",
        "ObsProposal": "XML_OBSPROPOSAL_ENTITIES",
        "ObsReview": "XML_OBSREVIEW_ENTITIES",
        "ObsToolUserPrefs": "XML_OBSTOOLUSERPREFS_ENTITIES",
        "OUSStatus": "XML_OUSSTATUS_ENTITIES",
        "PointingMethod": "XML_POINTINGMETHOD_ENTITIES",
        "PointingModelMode": "XML_POINTINGMODELMODE_ENTITIES",
        "PointingModelTable": "XML_POINTINGMODELTABL_ENTITIES",
        "PointingTable": "XML_POINTINGTABLE_ENTITIES",
        "PolarizationTable": "XML_POLARIZATIONTABLE_ENTITIES",
        "PolarizationType": "XML_POLARIZATIONTYPE_ENTITIES",
        "PositionMethod": "XML_POSITIONMETHOD_ENTITIES",
        "PositionReferenceCode": "XML_POSITIONREFERENCE_ENTITIES",
        "Preferences": "XML_PREFERENCES_ENTITIES",
        "PrimaryBeamDescription": "XML_PRIMARYBEAMDESCRI_ENTITIES",
        "PrimitiveDataType": "XML_PRIMITIVEDATATYPE_ENTITIES",
        "ProcessorSubType": "XML_PROCESSORSUBTYPE_ENTITIES",
        "ProcessorTable": "XML_PROCESSORTABLE_ENTITIES",
        "ProcessorType": "XML_PROCESSORTYPE_ENTITIES",
        "ProjectStatus": "XML_PROJECTSTATUS_ENTITIES",
        "pset": "XML_PSET_ENTITIES",
        "psetdef": "XML_PSETDEF_ENTITIES",
        "QlAtmosphereSummary": "XML_QLATMOSPHERESUMMA_ENTITIES",
        "QlFocusSummary": "XML_QLFOCUSSUMMARY_ENTITIES",
        "QlPointingSummary": "XML_QLPOINTINGSUMMARY_ENTITIES",
        "QuickLookDisplay": "XML_QUICKLOOKDISPLAYX_ENTITIES",
        "QuickLookDisplayX": "XML_QUICKLOOKDISPLAY_ENTITIES",
        "QuickLookResult": "XML_QUICKLOOKRESULT_ENTITIES",
        "QuickLookSummary": "XML_QUICKLOOKSUMMARY_ENTITIES",
        "RadialVelocityReferenceCode": "XML_RADIALVELOCITYREF_ENTITIES",
        "ReceiverBand": "XML_RECEIVERBAND_ENTITIES",
        "ReceiverSideband": "XML_RECEIVERSIDEBAND_ENTITIES",
        "ReceiverTable": "XML_RECEIVERTABLE_ENTITIES",
        "SBStatus": "XML_SBSTATUS_ENTITIES",
        "SBSummaryTable": "XML_SBSUMMARYTABLE_ENTITIES",
        "SBType": "XML_SBTYPE_ENTITIES",
        "ScaleTable": "XML_SCALETABLE_ENTITIES",
        "ScanIntent": "XML_SCANINTENT_ENTITIES",
        "ScanTable": "XML_SCANTABLE_ENTITIES",
        "SchedBlock": "XML_SCHEDBLOCK_ENTITIES",
        "SchedulerMode": "XML_SCHEDULERMODE_ENTITIES",
        "SchedulingPolicy": "XML_SCHEDULINGPOLICY_ENTITIES",
        "SciPipeResults": "XML_SCIPIPERESULTS_ENTITIES",
        "sdmDataHeader": "XML_SDMDATAHEADER_ENTITIES",
        "SeeingTable": "XML_SEEINGTABLE_ENTITIES",
        "SidebandProcessingMode": "XML_SIDEBANDPROCESSIN_ENTITIES",
        "SourceModel": "XML_SOURCEMODEL_ENTITIES",
        "SourceTable": "XML_SOURCETABLE_ENTITIES",
        "SpecialSB": "XML_SPECIALSB_ENTITIES",
        "SpectralResolutionType": "XML_SPECTRALRESOLUTIO_ENTITIES",
        "SpectralWindowTable": "XML_SPECTRALWINDOWTAB_ENTITIES",
        "SquareLawDetectorTable": "XML_SQUARELAWDETECTOR_ENTITIES",
        "StateTable": "XML_STATETABLE_ENTITIES",
        "StationTable": "XML_STATIONTABLE_ENTITIES",
        "StationType": "XML_STATIONTYPE_ENTITIES",
        "StokesParameter": "XML_STOKESPARAMETER_ENTITIES",
        "SubscanFieldSource": "XML_SUBSCANFIELDSOURC_ENTITIES",
        "SubscanIntent": "XML_SUBSCANINTENT_ENTITIES",
        "SubscanSpectralSpec": "XML_SUBSCANSPECTRALSP_ENTITIES",
        "SubscanTable": "XML_SUBSCANTABLE_ENTITIES",
        "SwitchCycleTable": "XML_SWITCHCYCLETABLE_ENTITIES",
        "SwitchingMode": "XML_SWITCHINGMODE_ENTITIES",
        "SyscalMethod": "XML_SYSCALMETHOD_ENTITIES",
        "SysCalTable": "XML_SYSCALTABLE_ENTITIES",
        "TestObsProject": "XML_TESTOBSPROJECT_ENTITIES",
        "TestObsProposal": "XML_TESTOBSPROPOSAL_ENTITIES",
        "TestSchedBlock": "XML_TESTSCHEDBLOCK_ENTITIES",
        "TestValueTypes": "XML_TESTVALUETYPES_ENTITIES",
        "TimeSampling": "XML_TIMESAMPLING_ENTITIES",
        "TimeScale": "XML_TIMESCALE_ENTITIES",
        "TotalPowerTable": "XML_TOTALPOWERTABLE_ENTITIES",
        "User": "XML_USER_ENTITIES",
        "ValueTypes": "XML_VALUETYPES_ENTITIES",
        "WeatherTable": "XML_WEATHERTABLE_ENTITIES",
        "WeightType": "XML_WEIGHTTYPE_ENTITIES",
        "WindowFunction": "XML_WINDOWFUNCTION_ENTITIES",
        "WVMCalTable": "XML_WVMCALTABLE_ENTITIES",
        "WVRMethod": "XML_WVRMETHOD_ENTITIES"
}

schemadict = {
    "ACAPolarization" : "uid://A002/X1eadeb/X12c"
    ,"ACSAlarmMessage" : "uid://A002/X1eadeb/X64"
    ,"ACSError" : "uid://A002/X1eadeb/X41"
    ,"ACSLogTS" : "uid://A002/X1eadeb/X86"
    ,"ASDM" : "uid://A002/X1eadeb/X14f"
    ,"ASDMBinaryTable" : "uid://A002/X1eadeb/X149"
    ,"AccumMode" : "uid://A002/X1eadeb/X72"
    ,"AcsCommandCenterProject" : "uid://A002/X1eadeb/X43"
    ,"AcsCommandCenterTools" : "uid://A002/X1eadeb/X13b"
    ,"Address" : "uid://A002/X1eadeb/X8e"
    ,"AlmaRadiometerTable" : "uid://A002/X1eadeb/X10"
    ,"AnnotationTable" : "uid://A002/X1eadeb/X110"
    ,"AntennaMake" : "uid://A002/X1eadeb/X95"
    ,"AntennaMotionPattern" : "uid://A002/X1eadeb/X1b"
    ,"AntennaTable" : "uid://A002/X1eadeb/X26"
    ,"AntennaType" : "uid://A002/X1eadeb/X151"
    ,"AssociatedCalNature" : "uid://A002/X1eadeb/X5e"
    ,"AssociatedFieldNature" : "uid://A002/X1eadeb/X2d"
    ,"AtmPhaseCorrection" : "uid://A002/X1eadeb/X9"
    ,"AxisName" : "uid://A002/X1eadeb/X11e"
    ,"BasebandName" : "uid://A002/X1eadeb/X7c"
    ,"BaselineReferenceCode" : "uid://A002/X1eadeb/X12e"
    ,"CalAmpliTable" : "uid://A002/X1eadeb/Xe3"
    ,"CalAtmosphereTable" : "uid://A002/X1eadeb/Xa0"
    ,"CalBandpassTable" : "uid://A002/X1eadeb/Xbd"
    ,"CalCurveTable" : "uid://A002/X1eadeb/Xeb"
    ,"CalCurveType" : "uid://A002/X1eadeb/X3b"
    ,"CalDataOrigin" : "uid://A002/X1eadeb/X4e"
    ,"CalDataTable" : "uid://A002/X1eadeb/X14"
    ,"CalDelayTable" : "uid://A002/X1eadeb/X4a"
    ,"CalDeviceTable" : "uid://A002/X1eadeb/X80"
    ,"CalFluxTable" : "uid://A002/X1eadeb/X130"
    ,"CalFocusModelTable" : "uid://A002/X1eadeb/X136"
    ,"CalFocusTable" : "uid://A002/X1eadeb/X13f"
    ,"CalGainTable" : "uid://A002/X1eadeb/X12a"
    ,"CalHolographyTable" : "uid://A002/X1eadeb/X92"
    ,"CalPhaseTable" : "uid://A002/X1eadeb/X134"
    ,"CalPointingModelTable" : "uid://A002/X1eadeb/X45"
    ,"CalPointingTable" : "uid://A002/X1eadeb/X70"
    ,"CalPositionTable" : "uid://A002/X1eadeb/X88"
    ,"CalPrimaryBeamTable" : "uid://A002/X1eadeb/Xf1"
    ,"CalQueryParameters" : "uid://A002/X1eadeb/Xc"
    ,"CalReductionTable" : "uid://A002/X1eadeb/Xe1"
    ,"CalSeeingTable" : "uid://A002/X1eadeb/X3"
    ,"CalType" : "uid://A002/X1eadeb/X29"
    ,"CalWVRTable" : "uid://A002/X1eadeb/Xa6"
    ,"CalibrationDevice" : "uid://A002/X1eadeb/Xa4"
    ,"CalibrationFunction" : "uid://A002/X1eadeb/X10e"
    ,"CalibrationMode" : "uid://A002/X1eadeb/X1f"
    ,"CalibrationSet" : "uid://A002/X1eadeb/Xae"
    ,"CommonEntity" : "uid://A002/X1eadeb/X106"
    ,"ConfigDescriptionTable" : "uid://A002/X1eadeb/X33"
    ,"CorrelationBit" : "uid://A002/X1eadeb/Xd7"
    ,"CorrelationMode" : "uid://A002/X1eadeb/X1"
    ,"CorrelatorCalibration" : "uid://A002/X1eadeb/X66"
    ,"CorrelatorModeTable" : "uid://A002/X1eadeb/X145"
    ,"CorrelatorName" : "uid://A002/X1eadeb/X10c"
    ,"CorrelatorType" : "uid://A002/X1eadeb/Xba"
    ,"DataContent" : "uid://A002/X1eadeb/Xf3"
    ,"DataDescriptionTable" : "uid://A002/X1eadeb/Xcd"
    ,"DelayModelTable" : "uid://A002/X1eadeb/Xe7"
    ,"DetectorBandType" : "uid://A002/X1eadeb/X11a"
    ,"DirectionReferenceCode" : "uid://A002/X1eadeb/X9b"
    ,"DopplerReferenceCode" : "uid://A002/X1eadeb/X139"
    ,"DopplerTable" : "uid://A002/X1eadeb/Xdd"
    ,"EphemerisTable" : "uid://A002/X1eadeb/X13d"
    ,"ExecBlockTable" : "uid://A002/X1eadeb/Xa8"
    ,"ExecConfig" : "uid://A002/X1eadeb/Xbf"
    ,"FeedTable" : "uid://A002/X1eadeb/X12"
    ,"FieldCode" : "uid://A002/X1eadeb/X31"
    ,"FieldTable" : "uid://A002/X1eadeb/Xb4"
    ,"FilterMode" : "uid://A002/X1eadeb/X16"
    ,"FlagCmdTable" : "uid://A002/X1eadeb/X126"
    ,"FlagTable" : "uid://A002/X1eadeb/X54"
    ,"FluxCalibrationMethod" : "uid://A002/X1eadeb/X84"
    ,"FocusMethod" : "uid://A002/X1eadeb/X128"
    ,"FocusModelTable" : "uid://A002/X1eadeb/Xc7"
    ,"FocusTable" : "uid://A002/X1eadeb/Xac"
    ,"FreqOffsetTable" : "uid://A002/X1eadeb/X108"
    ,"FrequencyReferenceCode" : "uid://A002/X1eadeb/X62"
    ,"GainTrackingTable" : "uid://A002/X1eadeb/X120"
    ,"HistoryTable" : "uid://A002/X1eadeb/X153"
    ,"HolographyChannelType" : "uid://A002/X1eadeb/Xf7"
    ,"HolographyTable" : "uid://A002/X1eadeb/X7e"
    ,"IdentifierRange" : "uid://A002/X1eadeb/X118"
    ,"InvalidatingCondition" : "uid://A002/X1eadeb/Xd3"
    ,"MainTable" : "uid://A002/X1eadeb/X1d"
    ,"NetSideband" : "uid://A002/X1eadeb/Xd9"
    ,"OUSStatus" : "uid://A002/X1eadeb/X147"
    ,"ObsAttachment" : "uid://A002/X1eadeb/X6e"
    ,"ObsProject" : "uid://A002/X1eadeb/X14b"
    ,"ObsProposal" : "uid://A002/X1eadeb/X78"
    ,"ObsReview" : "uid://A002/X1eadeb/Xef"
    ,"ObsToolUserPrefs" : "uid://A002/X1eadeb/Xdf"
    ,"ObservationTable" : "uid://A002/X1eadeb/X132"
    ,"PointingMethod" : "uid://A002/X1eadeb/X8c"
    ,"PointingModelMode" : "uid://A002/X1eadeb/X60"
    ,"PointingModelTable" : "uid://A002/X1eadeb/Xdb"
    ,"PointingTable" : "uid://A002/X1eadeb/X114"
    ,"PolarizationTable" : "uid://A002/X1eadeb/X52"
    ,"PolarizationType" : "uid://A002/X1eadeb/X4c"
    ,"PositionMethod" : "uid://A002/X1eadeb/X58"
    ,"PositionReferenceCode" : "uid://A002/X1eadeb/Xf5"
    ,"Preferences" : "uid://A002/X1eadeb/Xaa"
    ,"PrimitiveDataType" : "uid://A002/X1eadeb/X35"
    ,"ProcessorSubType" : "uid://A002/X1eadeb/X11c"
    ,"ProcessorTable" : "uid://A002/X1eadeb/X14d"
    ,"ProcessorType" : "uid://A002/X1eadeb/X82"
    ,"ProjectStatus" : "uid://A002/X1eadeb/Xcf"
    ,"QuickLookDisplay" : "uid://A002/X1eadeb/Xf9"
    ,"QuickLookDisplayX" : "uid://A002/X1eadeb/X76"
    ,"QuickLookResult" : "uid://A002/X1eadeb/X7a"
    ,"RadialVelocityReferenceCode" : "uid://A002/X1eadeb/Xa2"
    ,"ReceiverBand" : "uid://A002/X1eadeb/X68"
    ,"ReceiverSideband" : "uid://A002/X1eadeb/Xb2"
    ,"ReceiverTable" : "uid://A002/X1eadeb/X97"
    ,"SBStatus" : "uid://A002/X1eadeb/X124"
    ,"SBSummaryTable" : "uid://A002/X1eadeb/X99"
    ,"SBType" : "uid://A002/X1eadeb/X100"
    ,"ScanIntent" : "uid://A002/X1eadeb/Xed"
    ,"ScanTable" : "uid://A002/X1eadeb/X8a"
    ,"SchedBlock" : "uid://A002/X1eadeb/X90"
    ,"SchedulerMode" : "uid://A002/X1eadeb/X2f"
    ,"SchedulingPolicy" : "uid://A002/X1eadeb/X56"
    ,"SciPipeResults" : "uid://A002/X1eadeb/X5c"
    ,"SeeingTable" : "uid://A002/X1eadeb/X143"
    ,"SidebandProcessingMode" : "uid://A002/X1eadeb/X21"
    ,"SourceModel" : "uid://A002/X1eadeb/X112"
    ,"SourceTable" : "uid://A002/X1eadeb/X48"
    ,"SpecialSB" : "uid://A002/X1eadeb/Xd5"
    ,"SpectralResolutionType" : "uid://A002/X1eadeb/X74"
    ,"SpectralWindowTable" : "uid://A002/X1eadeb/X9d"
    ,"SquareLawDetectorTable" : "uid://A002/X1eadeb/X5a"
    ,"StateTable" : "uid://A002/X1eadeb/X39"
    ,"StationTable" : "uid://A002/X1eadeb/X2b"
    ,"StationType" : "uid://A002/X1eadeb/X141"
    ,"StokesParameter" : "uid://A002/X1eadeb/Xe5"
    ,"SubscanFieldSource" : "uid://A002/X1eadeb/Xc5"
    ,"SubscanIntent" : "uid://A002/X1eadeb/X50"
    ,"SubscanSpectralSpec" : "uid://A002/X1eadeb/X37"
    ,"SubscanTable" : "uid://A002/X1eadeb/X24"
    ,"SwitchCycleTable" : "uid://A002/X1eadeb/Xb8"
    ,"SwitchingMode" : "uid://A002/X1eadeb/Xe9"
    ,"SysCalTable" : "uid://A002/X1eadeb/X3d"
    ,"SyscalMethod" : "uid://A002/X1eadeb/X122"
    ,"TestObsProject" : "uid://A002/X1eadeb/Xcb"
    ,"TestObsProposal" : "uid://A002/X1eadeb/X116"
    ,"TestSchedBlock" : "uid://A002/X1eadeb/Xc1"
    ,"TestValueTypes" : "uid://A002/X1eadeb/Xc3"
    ,"TimeSampling" : "uid://A002/X1eadeb/Xfe"
    ,"TotalPowerTable" : "uid://A002/X1eadeb/X18"
    ,"User" : "uid://A002/X1eadeb/Xb6"
    ,"ValueTypes" : "uid://A002/X1eadeb/X7"
    ,"WVMCalTable" : "uid://A002/X1eadeb/Xd1"
    ,"WVRMethod" : "uid://A002/X1eadeb/X102"
    ,"WeatherTable" : "uid://A002/X1eadeb/Xfc"
    ,"WindowFunction" : "uid://A002/X1eadeb/X3f"
    ,"bulkTest" : "uid://A002/X1eadeb/X104"
    ,"commontypes" : "uid://A002/X1eadeb/X6a"
    ,"loggingMI" : "uid://A002/X1eadeb/X10a"
    ,"pset" : "uid://A002/X1eadeb/Xb0"
    ,"psetdef" : "uid://A002/X1eadeb/Xe"
    ,"sdmDataHeader" : "uid://A002/X1eadeb/X5"
}

