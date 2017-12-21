# -*- coding: utf-8 -*-

"""Query the MusicBrainz API using the the python module
`musicbrainzngs <https://github.com/alastair/python-musicbrainzngs>`_ .

Main purpose of this file is to get the corresponding work from a recording.
In large releases with many tracks Picard can not get informations about works.
"""

import musicbrainzngs as mbrainz


def get_work(mb_trackid):
    """Get the work title and the work id of a track.

    :param string mb_trackid: The MusicBrainz track id (Example
        :code:`00ba1660-4e35-4985-86b2-8b7a3e99b1e5`).

    :return: A dictonry like this:

    .. code-block:: Python

        {
            'recording': {
                'length': '566933',
                'work-relation-list': [
                    {
                        'type-id': 'a3005666-a872-32c3-ad06-98af558e99b0',
                        'work': {
                            'id': '6b198406-4fbf-3d61-82db-0b7ef195a7fe',
                            'language': 'zxx',
                            'title': u'Die Meistersinger von ....'
                        },
                        'type': 'performance',
                        'target': '6b198406-4fbf-3d61-82db-0b7ef195a7fe'
                    }
                ],
                'id': '00ba1660-4e35-4985-86b2-8b7a3e99b1e5',
                'title': u'Die Meistersinger von N\xfcrnberg: Vorspiel'
            }
        }
    """

    mbrainz.set_useragent(
        "audiorename",
        "1.0.8",
        "https://github.com/Josef-Friedrich/audiorename",
    )

    try:
        return mbrainz.get_recording_by_id(mb_trackid, includes=['work-rels'])

    except mbrainz.ResponseError as err:
        if err.cause.code == 404:
            print("Work not found")
        else:
            print("received bad response from the MB server")
