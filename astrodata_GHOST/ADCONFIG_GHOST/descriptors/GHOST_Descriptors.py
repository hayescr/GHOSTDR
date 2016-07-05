from GHOST_Keywords import GHOST_KeyDict

from datetime import datetime
from time import strptime

from astrodata.utils import Errors
from astrodata.interface.Descriptors import DescriptorValue

from gempy.gemini import gemini_metadata_utils as gmu

from astrodata_Gemini.ADCONFIG_Gemini.descriptors.GEMINI_Descriptors import GEMINI_DescriptorCalc

class GHOST_DescriptorCalc(GEMINI_DescriptorCalc):
    _update_stdkey_dict = GHOST_KeyDict

    def __init__(self):
        GEMINI_DescriptorCalc.__init__(self)

    def read_noise(self, dataset, **args):
        # Since this descriptor function accesses keywords in the headers of
        # the pixel data extensions, always construct a dictionary where the
        # key of the dictionary is an (EXTNAME, EXTVER) tuple
        ret_read_noise_dict = {}

        # If the data have been prepared, take the read noise value directly
        # from the appropriate keyword. At some point, a check for the STDHDRSI
        # header keyword should be added, since the function that overwrites
        # the read noise keyword also writes the STDHDRSI keyword.
        if "PREPARED" in dataset.types:

            # Determine the read noise keyword from the global keyword
            # dictionary
            keyword = self.get_descriptor_key("key_read_noise")

            # Get the value of the read noise keyword from the header of each
            # pixel data extension as a dictionary where the key of the
            # dictionary is an ("*", EXTVER) tuple
            read_noise_dict = gmu.get_key_value_dict(adinput=dataset,
                                                     keyword=keyword)
            if read_noise_dict is None:
                # The get_key_value_dict() function returns None if a value
                # cannot be found and stores the exception info. Re-raise the
                # exception. It will be dealt with by the CalculatorInterface.
                if hasattr(dataset, "exception_info"):
                    raise dataset.exception_info

            for ext_name_ver, raw_read_noise in read_noise_dict.iteritems():
                if raw_read_noise is None:
                    read_noise = None
                else:
                    read_noise = float(raw_read_noise)

                # Update the dictionary with the read noise value
                ret_read_noise_dict.update({ext_name_ver: read_noise})
        else:
            # Get the lookup table containing the read noise values by
            # amplifier
            gmosampsRdnoise = GMOSAmpTables.gmosampsRdnoise
            gmosampsRdnoiseBefore20150826 = GMOSAmpTables.gmosampsRdnoiseBefore20150826
            gmosampsRdnoiseBefore20060831 = GMOSAmpTables.gmosampsRdnoiseBefore20060831

            # Get the UT date, gain setting and read speed setting values using
            # the appropriate descriptors
            ut_date_dv = dataset.ut_date()
            gain_setting_dv = dataset.gain_setting()
            read_speed_setting_dv = dataset.read_speed_setting()

            if (ut_date_dv.is_none() or gain_setting_dv.is_none() or
                    read_speed_setting_dv.is_none()):
                # The descriptor functions return None if a value cannot be
                # found and stores the exception info. Re-raise the exception.
                # It will be dealt with by the CalculatorInterface.
                if hasattr(dataset, "exception_info"):
                    raise dataset.exception_info

            # Use as_dict() and as_pytype() to return the values as a
            # dictionary and the default python type, respectively, rather than
            # an object
            ut_date = str(ut_date_dv)
            gain_setting_dict = gain_setting_dv.as_dict()
            read_speed_setting = read_speed_setting_dv.as_pytype()

            obs_ut_date = datetime(*strptime(ut_date, "%Y-%m-%d")[0:6])
            change_2015_ut = datetime(2015, 8, 26, 0, 0)
            change_2006_ut = datetime(2006, 8, 31, 0, 0)
            # Determine the name of the detector amplifier keyword (ampname)
            # from the global keyword dictionary
            keyword = self.get_descriptor_key("key_ampname")

            # Get the value of the name of the detector amplifier keyword from
            # the header of each pixel data extension as a dictionary where the
            # key of the dictionary is an ("*", EXTVER) tuple
            ampname_dict = gmu.get_key_value_dict(adinput=dataset,
                                                  keyword=keyword)
            if ampname_dict is None:
                # The get_key_value_dict() function returns None if a value
                # cannot be found and stores the exception info. Re-raise the
                # exception. It will be dealt with by the CalculatorInterface.
                if hasattr(dataset, "exception_info"):
                    raise dataset.exception_info

            for ext_name_ver, ampname in ampname_dict.iteritems():
                gain_setting = gain_setting_dict[ext_name_ver]

                if ampname is None or gain_setting is None:
                    read_noise = None
                else:
                    read_noise_key = (
                        read_speed_setting, gain_setting, ampname)

                    if obs_ut_date > change_2015_ut:
                        read_noise_dict = gmosampsRdnoise
                    elif obs_ut_date > change_2006_ut:
                        read_noise_dict = gmosampsRdnoiseBefore20150826
                    else:
                        read_noise_dict = gmosampsRdnoiseBefore20060831

                    if read_noise_key in read_noise_dict:
                        read_noise = read_noise_dict[read_noise_key]
                    else:
                        raise Errors.TableKeyError()

                # Update the dictionary with the read noise value
                ret_read_noise_dict.update({ext_name_ver: read_noise})

        # Instantiate the return DescriptorValue (DV) object
        ret_dv = DescriptorValue(ret_read_noise_dict, name="read_noise",
                                 ad=dataset)
        return ret_dv

    def gain(self, dataset, **args):
        # Since this descriptor function accesses keywords in the headers of
        # the pixel data extensions, always construct a dictionary where the
        # key of the dictionary is an (EXTNAME, EXTVER) tuple
        ret_gain_dict = {}

        # If the data have been prepared, take the gain value directly from the
        # appropriate keyword. At some point, a check for the STDHDRSI header
        # keyword should be added, since the function that overwrites the gain
        # keyword also writes the STDHDRSI keyword.
        if "PREPARED" in dataset.types:

            # Determine the gain keyword from the global keyword dictionary
            keyword = self.get_descriptor_key("key_gain")

            # Get the value of the gain keyword from the header of each pixel
            # data extension as a dictionary where the key of the dictionary is
            # an ("*", EXTVER) tuple
            gain_dict = gmu.get_key_value_dict(adinput=dataset,
                                               keyword=keyword)
            if gain_dict is None:
                # The get_key_value_dict() function returns None if a value
                # cannot be found and stores the exception info. Re-raise the
                # exception. It will be dealt with by the CalculatorInterface.
                if hasattr(dataset, "exception_info"):
                    raise dataset.exception_info

            ret_gain_dict = gain_dict

        else:
            # Get the lookup table containing the gain values by amplifier
            gmosampsGain = GMOSAmpTables.gmosampsGain
            gmosampsGainBefore20150826 = GMOSAmpTables.gmosampsGainBefore20150826
            gmosampsGainBefore20060831 = GMOSAmpTables.gmosampsGainBefore20060831

            # Determine the amplifier integration time keyword (ampinteg) from
            # the global keyword dictionary
            keyword = self.get_descriptor_key("key_ampinteg")

            # Get the value of the amplifier integration time keyword from the
            # header of the PHU
            ampinteg = dataset.phu_get_key_value(keyword)

            if ampinteg is None:
                # The phu_get_key_value() function returns None if a value
                # cannot be found and stores the exception info. Re-raise the
                # exception. It will be dealt with by the CalculatorInterface.
                if hasattr(dataset, "exception_info"):
                    raise dataset.exception_info

            # Get the UT date, gain setting and read speed setting values using
            # the appropriate descriptors
            ut_date_dv = dataset.ut_date()
            gain_setting_dv = dataset.gain_setting()
            read_speed_setting_dv = dataset.read_speed_setting()

            if (ut_date_dv.is_none() or gain_setting_dv.is_none() or
                    read_speed_setting_dv.is_none()):
                # The descriptor functions return None if a value cannot be
                # found and stores the exception info. Re-raise the exception.
                # It will be dealt with by the CalculatorInterface.
                if hasattr(dataset, "exception_info"):
                    raise dataset.exception_info

            # Use as_dict() and as_pytype() to return the values as a
            # dictionary where the key of the dictionary is an ("*", EXTVER)
            # tuple and the default python type, respectively, rather than an
            # object
            ut_date = str(ut_date_dv)
            gain_setting_dict = gain_setting_dv.as_dict()
            read_speed_setting = read_speed_setting_dv.as_pytype()

            obs_ut_date = datetime(*strptime(ut_date, "%Y-%m-%d")[0:6])
            # These dates really shouldn't be hard wired so sloppily all over
            # the place (including gempy gemini_data_calculations.py) but that
            # goes as far as the dictionary names so leave it for a possible
            # future clean up of how the dictionaries are keyed.
            change_2015_ut = datetime(2015, 8, 26, 0, 0)
            change_2006_ut = datetime(2006, 8, 31, 0, 0)

            # Determine the name of the detector amplifier keyword (ampname)
            # from the global keyword dictionary
            keyword = self.get_descriptor_key("key_ampname")

            # Get the value of the name of the detector amplifier keyword from
            # the header of each pixel data extension as a dictionary where the
            # key of the dictionary is an ("*", EXTVER) tuple
            ampname_dict = gmu.get_key_value_dict(adinput=dataset,
                                                  keyword=keyword)
            if ampname_dict is None:
                # The get_key_value_dict() function returns None if a value
                # cannot be found and stores the exception info. Re-raise the
                # exception. It will be dealt with by the CalculatorInterface.
                if hasattr(dataset, "exception_info"):
                    raise dataset.exception_info

            for ext_name_ver, ampname in ampname_dict.iteritems():
                gain_setting = gain_setting_dict[ext_name_ver]

                if ampname is None or gain_setting is None:
                    gain = None
                else:
                    gain_key = (read_speed_setting, gain_setting, ampname)

                    if obs_ut_date > change_2015_ut:
                        gain_dict = gmosampsGain
                    elif obs_ut_date > change_2006_ut:
                        gain_dict = gmosampsGainBefore20150826
                    else:
                        gain_dict = gmosampsGainBefore20060831

                    if gain_key in gain_dict:
                        gain = gain_dict[gain_key]
                    else:
                        raise Errors.TableKeyError()

                # Update the dictionary with the gain value
                ret_gain_dict.update({ext_name_ver: gain})

        # Instantiate the return DescriptorValue (DV) object
        ret_dv = DescriptorValue(ret_gain_dict, name="gain", ad=dataset)

        return ret_dv
