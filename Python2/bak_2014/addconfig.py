# -*- coding:utf-8 -*-


def add_config(self, options):
    """Creates analysis.conf file from current analysis options.
    @param options: current configuration options, dict format.
    @return: operation status.
    """
    global ERROR_MESSAGE

    if type(options) != dict:
        return False

    config = ConfigParser.RawConfigParser()
    config.add_section("analysis")

    try:
        for key, value in options.items():
            # Options can be UTF encoded.
            if isinstance(value, basestring):
                try:
                    value = value.encode("utf-8")
                except UnicodeEncodeError:
                    pass

            config.set("analysis", key, value)

        config_path = os.path.join(ANALYZER_FOLDER, "analysis.conf")
    
        with open(config_path, "wb") as config_file:
            config.write(config_file)
    except Exception as e:
        ERROR_MESSAGE = str(e)
        return False

    return True


if __name__ == '__main__':
    options = {'category':'file','target':'/var/VenusAnalysis/cuckoo/web/tmp_uploads/tmpW8gjcv/分xi.doc'}
    add_config(options)