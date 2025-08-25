'''Funktion to create links to oral_history_digital'''


def create_link(archive: str ="", interview_id: str = "", chunk_start_time: str = "False",
                link_tape: str = "1", ):
    link_available = False
    if archive.lower() == "adg":
        https = "https://deutsches-gedaechtnis.fernuni-hagen.de/de/interviews/adg"
        link_available = True
    if archive.lower() == "zwa":
        https = "https://archiv.zwangsarbeit-archiv.de/de/interviews/za"
        link_available = True
    if archive.lower() == "fvv":
        https = "https://portal.oral-history.digital/fvv/de/interviews/fvv00"
        link_available = True
    if archive.lower() == "mfl":
        https = "https://portal.oral-history.digital/mfl/de/interviews/mfl"
        link_available = True
    if archive.lower() == "wde":
        https = "https://portal.oral-history.digital/fzh-wde/de/interviews/fzh-wde"
        link_available = True
    if archive.lower() == "cdg":
        https = "https://archiv.cdoh.net/de/interviews/cd"
        link_available = True
    if link_available:
        if chunk_start_time == "False":
            link = (https + interview_id[3:])
        else:
            link = (https + interview_id[3:]
            + "?tape=" + str(link_tape)
            + "&time=" + str(chunk_start_time.split(":")[0][1]) + "h"
            + str(chunk_start_time.split(":")[1]) + "m"
            + str(chunk_start_time.split(":")[2].split(".")[0]) + "s"
            )
    else:
        link = "Not online available"
    return link



