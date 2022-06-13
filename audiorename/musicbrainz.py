import typing
import musicbrainzngs as musicbrainz

from ._version import get_versions

"""Query the musicbrainz API using the library
`musicbrainzngs <https://pypi.org/project/musicbrainzngs>`_.

.. code-block:: Python

    import json
    print(json.dumps(result,indent=2))

``get_recording_by_id`` with ``work-rels``

soundtrack/Pulp-Fiction/01.mp3

.. code-block:: JSON

    {
      "recording": {
        "length": "149000",
        "id": "0480672d-4d88-4824-a06b-917ff408eabe",
        "title": "Pumpkin and Honey Bunny ..."
      }
    }

classical/Mozart_Horn-concertos/01.mp3

.. code-block:: JSON

    {
      "recording": {
        "length": "286826",
        "work-relation-list": [
          {
            "type-id": "a3005666-a872-32c3-ad06-98af558e99b0",
            "begin": "1987-03",
            "end": "1987-03",
            "target": "21fe0bf0-a040-387c-a39d-369d53c251fe",
            "ended": "true",
            "work": {
              "id": "21fe0bf0-a040-387c-a39d-369d53c251fe",
              "language": "zxx",
              "title": "Concerto [...] KV 412: I. Allegro"
            },
            "type": "performance"
          }
        ],
        "id": "7886ad6c-11af-435b-8ec3-bca5711f7728",
        "title": "Konzert f\u00fcr [...] K. 386b/514: I. Allegro"
      }
    }

``get_work_by_id`` with ``work-rels``

.. code-block:: JSON

    {
      "work": {
        "work-relation-list": [
          {
            "type-id": "ca8d3642-ce5f-49f8-91f2-125d72524e6a",
            "direction": "backward",
            "target": "5adc213f-700a-4435-9e95-831ed720f348",
            "ordering-key": "3",
            "work": {
              "id": "5adc213f-700a-4435-9e95-831ed720f348",
              "language": "deu",
              "title": "Die Zauberfl\u00f6te, K. 620: Akt I"
            },
            "type": "parts"
          },
          {
            "type-id": "51975ed8-bbfa-486b-9f28-5947f4370299",
            "work": {
              "disambiguation": "for piano, arr. Matthias",
              "id": "798f4c25-0ab3-44ba-81b6-3d856aedf82a",
              "language": "zxx",
              "title": "Die Zauberfl\u00f6te, K. 620: Aria ..."
            },
            "type": "arrangement",
            "target": "798f4c25-0ab3-44ba-81b6-3d856aedf82a"
          }
        ],
        "type": "Aria",
        "id": "eafec51f-47c5-3c66-8c36-a524246c85f8",
        "language": "deu",
        "title": "Die Zauberfl\u00f6te: Act I, Scene II. No. 2 Aria ..",
        "artist-relation-list": [
          {
            "type-id": "7474ab81-486f-40b5-8685-3a4f8ea624cb",
            "direction": "backward",
            "type": "librettist",
            "target": "86104c7c-cda4-4798-a4ab-104318c7ae9c",
            "artist": {
              "sort-name": "Schikaneder, Emanuel",
              "id": "86104c7c-cda4-4798-a4ab-104318c7ae9c",
              "name": "Emanuel Schikaneder"
            }
          },
          {
            "begin": "1791",
            "end": "1791",
            "target": "b972f589-fb0e-474e-b64a-803b0364fa75",
            "artist": {
              "sort-name": "Mozart, Wolfgang Amadeus",
              "disambiguation": "classical composer",
              "id": "b972f589-fb0e-474e-b64a-803b0364fa75",
              "name": "Wolfgang Amadeus Mozart"
            },
            "direction": "backward",
            "type-id": "d59d99ea-23d4-4a80-b066-edca32ee158f",
            "ended": "true",
            "type": "composer"
          }
        ]
      }
    }


.. code-block:: JSON

    {
      "work": {
        "work-relation-list": [
          {
            "type-id": "c1dca2cd-194c-36dd-93f8-6a359167e992",
            "direction": "backward",
            "work": {
              "id": "70e53569-258c-463d-9505-5b69dcbf374a",
              "title": "Can\u2019t Stop the Classics, Part 2"
            },
            "type": "medley",
            "target": "70e53569-258c-463d-9505-5b69dcbf374a"
          },
          {
            "type-id": "ca8d3642-ce5f-49f8-91f2-125d72524e6a",
            "direction": "backward",
            "target": "73663bd3-392f-45a7-b4ff-e75c01f5926a",
            "ordering-key": "1",
            "work": {
              "id": "73663bd3-392f-45a7-b4ff-e75c01f5926a",
              "language": "deu",
              "title": "Die Meistersinger von N\u00fcrnberg, WWV 96: Akt I"
            },
            "type": "parts"
          }
        ]
      }
    }

``get_release_by_id`` with ``release-groups``

soundtrack/Pulp-Fiction/01.mp3

.. code-block:: JSON

    {
      "release": {
        "status": "Bootleg",
        "release-event-count": 1,
        "title": "Pulp Fiction",
        "country": "US",
        "cover-art-archive": {
          "count": "1",
          "front": "true",
          "back": "false",
          "artwork": "true"
        },
        "release-event-list": [
          {
            "date": "2005-12-01",
            "area": {
              "sort-name": "United States",
              "iso-3166-1-code-list": [
                "US"
              ],
              "id": "489ce91b-6658-3307-9877-795b68554c98",
              "name": "United States"
            }
          }
        ],
        "release-group": {
          "first-release-date": "1994-09-27",
          "secondary-type-list": [
            "Compilation",
            "Soundtrack"
          ],
          "primary-type": "Album",
          "title": "Pulp Fiction: Music From the Motion Picture",
          "type": "Soundtrack",
          "id": "1703cd63-9401-33c0-87c6-50c4ba2e0ba8"
        },
        "text-representation": {
          "language": "eng",
          "script": "Latn"
        },
        "date": "2005-12-01",
        "quality": "normal",
        "id": "ab81edcb-9525-47cd-8247-db4fa969f525",
        "asin": "B000002OTL"
      }
    }

classical/Mozart_Horn-concertos/01.mp3

.. code-block:: JSON

    {
      "release": {
        "status": "Official",
        "release-event-count": 1,
        "title": "4 Hornkonzerte (Concertos for Horn and Orchestra)",
        "country": "DE",
        "barcode": "028942781429",
        "cover-art-archive": {
          "count": "0",
          "front": "false",
          "back": "false",
          "artwork": "false"
        },
        "release-event-list": [
          {
            "date": "1988",
            "area": {
              "sort-name": "Germany",
              "iso-3166-1-code-list": [
                "DE"
              ],
              "id": "85752fda-13c4-31a3-bee5-0e5cb1f51dad",
              "name": "Germany"
            }
          }
        ],
        "release-group": {
          "first-release-date": "1988",
          "title": "4 Hornkonzerte (Concertos for Horn and Orchestra)",
          "type": "Album",
          "id": "e1fa28f0-e56e-395b-82d3-a8de54e8c627",
          "primary-type": "Album"
        },
        "text-representation": {
          "language": "deu",
          "script": "Latn"
        },
        "date": "1988",
        "quality": "normal",
        "id": "5ed650c5-0f72-4b79-80a7-c458c869f53e",
        "asin": "B00000E4FA"
      }
    }

"""


def set_useragent() -> None:
    musicbrainz.set_useragent(
        'audiorename',
        get_versions()['version'],
        'https://github.com/Josef-Friedrich/audiorename',
    )


def query(
        mb_type: typing.Literal['recording', 'work', 'release'],
        mb_id: str) -> typing.Union[typing.Dict[str, typing.Any], None]:
    method = 'get_' + mb_type + '_by_id'
    query = getattr(musicbrainz, method)

    if mb_type == 'recording' or mb_type == 'work':
        mb_includes = ['work-rels']
    elif mb_type == 'release':
        mb_includes = ['release-groups']
    else:
        mb_includes = []

    if mb_type == 'work':
        mb_includes.append('artist-rels')

    try:
        result = query(mb_id, includes=mb_includes)
        return result[mb_type]

    except musicbrainz.ResponseError as err:
        if err.cause and err.cause.code == 404:
            print('Item of type “' + mb_type + '” with the ID '
                  '“' + mb_id + '” not found.')
        else:
            print("Received bad response from the MusicBrainz server.")


def query_works_recursively(work_id: str, works=[]):
    work = query('work', work_id)

    if not work:
        return works

    works.append(work)

    parent_work = False
    if 'work-relation-list' in work:
        for relation in work['work-relation-list']:
            if 'direction' in relation and \
                    relation['direction'] == 'backward' and \
                    relation['type'] == 'parts':
                parent_work = relation
                break

    if parent_work:
        query_works_recursively(parent_work['work']['id'], works)

    return works
