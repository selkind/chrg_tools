import pytest
from hearings_lib.summary_parsing_types import ParsedMember, ParsedCommittee, ParsedModsData


@pytest.fixture
def expected_alt_committees():
    return [
        ParsedCommittee(
            name='Committee on Finance',
            chamber='S',
            congress=113,
            subcommittees=[]
        )
    ]


@pytest.fixture
def expected_alt_witnesses():
    return [
        'Cohen, Gary, Deputy Administrator and Director, Center for Consumer Information and Insurance Oversight (CCIIO), Centers for Medicare and Medicaid Services, Department of Health and Human Services, Washington, DC',
        'Hughes, Don, Advisor to the Office of the Governor, State of Arizona, Phoenix, AZ',
        'Ferguson, Christine, Director of the Rhode Island Health Benefit Exchange, State of Rhode Island, Providence, RI',
        'Tweardy Riveros, Bettina, Advisor to the Governor and Chair of the Delaware Health Care Commission, State of Delaware, Wilmington, DE',
    ]


@pytest.fixture
def expected_first_ten_alt_members():
    return [
        ParsedMember(
            name='Schumer, Charles E.',
            chamber='S',
            party='D',
            congress=113,
            state='NY'
        ),
        ParsedMember(
            name='Wyden, Ron',
            chamber='S',
            party='D',
            congress=113,
            state='OR'
        ),
        ParsedMember(
            name='Brown, Sherrod',
            chamber='S',
            party='D',
            congress=113,
            state='OH'
        ),
        ParsedMember(
            name='Stabenow, Debbie',
            chamber='S',
            party='D',
            congress=113,
            state='MI'
        ),
        ParsedMember(
            name='Thune, John',
            chamber='S',
            party='R',
            congress=113,
            state='SD'
        ),
        ParsedMember(
            name='Burr, Richard',
            chamber='S',
            party='R',
            congress=113,
            state='NC'
        ),
        ParsedMember(
            name='Enzi, Michael B.',
            chamber='S',
            party='R',
            congress=113,
            state='WY'
        ),
        ParsedMember(
            name='Toomey, Pat',
            chamber='S',
            party='R',
            congress=113,
            state='PA'
        ),
        ParsedMember(
            name='Isakson, Johnny',
            chamber='S',
            party='R',
            congress=113,
            state='GA'
        ),
        ParsedMember(
            name='Cornyn, John',
            chamber='S',
            party='R',
            congress=113,
            state='TX'
        )
    ]


@pytest.fixture
def expected_alt_parsed_mods(expected_first_ten_alt_members, expected_alt_witnesses, expected_alt_committees):
    return ParsedModsData(
        members=expected_first_ten_alt_members,
        witnesses=expected_alt_witnesses,
        committees=expected_alt_committees,
        uri='https://www.govinfo.gov/app/details/CHRG-113shrg87945'
    )


@pytest.fixture
def expected_parsed_committees():
    return [
        ParsedCommittee(
            name='Committee on Foreign Affairs',
            chamber='H',
            congress=113,
            subcommittees=[
                'Subcommittee on the Middle East and North Africa',
                'Subcommittee on Terrorism, Nonproliferation, and Trade'
            ]
        )
    ]


@pytest.fixture
def expected_parsed_witnesses():
    return [
        'The Honorable Mark D. Wallace, chief executive officer, United Against Nuclear Iran (former United States Ambassador to the United Nations)',
        'Mr. Gregory S. Jones, senior researcher, Nonproliferation Policy Education Center',
        'Mr. Olli Heinonen, senior fellow, Belfer Center for Science and International Affairs, Harvard University (former Deputy Director General of the International Atomic Energy Agency)',
        'Mr. David Albright, founder and president, Institute for Science and International Security'
    ]


@pytest.fixture
def expected_parsed_members():
    return [
        ParsedMember(
            name='Salmon, Matt',
            chamber='H',
            party='R',
            congress=113,
            state='AZ'
        ),
        ParsedMember(
            name='Smith, Christopher H.',
            chamber='H',
            party='R',
            congress=113,
            state='NJ'
        ),
        ParsedMember(
            name='Stockman, Steve',
            chamber='H',
            party='R',
            congress=113,
            state='TX'
        ),
        ParsedMember(
            name='Meeks, Gregory W.',
            chamber='H',
            party='D',
            congress=113,
            state='NY'
        ),
        ParsedMember(
            name='Sherman, Brad',
            chamber='H',
            party='D',
            congress=113,
            state='CA'
        ),
        ParsedMember(
            name='Wilson, Joe',
            chamber='H',
            party='R',
            congress=113,
            state='SC'
        ),
        ParsedMember(
            name='Higgins, Brian',
            chamber='H',
            party='D',
            congress=113,
            state='NY'
        ),
        ParsedMember(
            name='Poe, Ted',
            chamber='H',
            party='R',
            congress=113,
            state='TX'
        ),
        ParsedMember(
            name='McCaul, Michael T.',
            chamber='H',
            party='R',
            congress=113,
            state='TX'
        ),
        ParsedMember(
            name='Sires, Albio',
            chamber='H',
            party='D',
            congress=113,
            state='NJ'
        ),
        ParsedMember(
            name='Chabot, Steve',
            chamber='H',
            party='R',
            congress=113,
            state='OH'
        ),
        ParsedMember(
            name='Grayson, Alan',
            chamber='H',
            party='D',
            congress=113,
            state='FL'
        ),
        ParsedMember(
            name='Connolly, Gerald E.',
            chamber='H',
            party='D',
            congress=113,
            state='VA'
        ),
        ParsedMember(
            name='Deutch, Theodore E.',
            chamber='H',
            party='D',
            congress=113,
            state='FL'
        ),
        ParsedMember(
            name='Brooks, Mo',
            chamber='H',
            party='R',
            congress=113,
            state='AL'
        ),
        ParsedMember(
            name='Bass, Karen',
            chamber='H',
            party='D',
            congress=113,
            state='CA'
        ),
        ParsedMember(
            name='Kinzinger, Adam',
            chamber='H',
            party='R',
            congress=113,
            state='IL'
        ),
        ParsedMember(
            name='Keating, William R.',
            chamber='H',
            party='D',
            congress=113,
            state='MA'
        ),
        ParsedMember(
            name='Marino, Tom',
            chamber='H',
            party='R',
            congress=113,
            state='PA'
        ),
        ParsedMember(
            name='Cicilline, David N.',
            chamber='H',
            party='D',
            congress=113,
            state='RI'
        ),
        ParsedMember(
            name='Duncan, Jeff',
            chamber='H',
            party='R',
            congress=113,
            state='SC'
        ),
        ParsedMember(
            name='Cotton, Tom',
            chamber='H',
            party='R',
            congress=113,
            state='AR'
        ),
        ParsedMember(
            name='Bera, Ami',
            chamber='H',
            party='D',
            congress=113,
            state='CA'
        ),
        ParsedMember(
            name='Cook, Paul',
            chamber='H',
            party='R',
            congress=113,
            state='CA'
        ),
        ParsedMember(
            name='Lowenthal, Alan S.',
            chamber='H',
            party='D',
            congress=113,
            state='CA'
        ),
        ParsedMember(
            name='Vargas, Juan',
            chamber='H',
            party='D',
            congress=113,
            state='CA'
        ),
        ParsedMember(
            name='Yoho, Ted S.',
            chamber='H',
            party='R',
            congress=113,
            state='FL'
        ),
        ParsedMember(
            name='DeSantis, Ron',
            chamber='H',
            party='R',
            congress=113,
            state='FL'
        ),
        ParsedMember(
            name='Frankel, Lois',
            chamber='H',
            party='D',
            congress=113,
            state='FL'
        ),
        ParsedMember(
            name='Collins, Doug',
            chamber='H',
            party='R',
            congress=113,
            state='GA'
        ),
        ParsedMember(
            name='Gabbard, Tulsi',
            chamber='H',
            party='D',
            congress=113,
            state='HI'
        ),
        ParsedMember(
            name='Schneider, Bradley Scott',
            chamber='H',
            party='D',
            congress=113,
            state='IL'
        ),
        ParsedMember(
            name='Messer, Luke',
            chamber='H',
            party='R',
            congress=113,
            state='IN'
        ),
        ParsedMember(
            name='Meadows, Mark',
            chamber='H',
            party='R',
            congress=113,
            state='NC'
        ),
        ParsedMember(
            name='Holding, George',
            chamber='H',
            party='R',
            congress=113,
            state='NC'
        ),
        ParsedMember(
            name='Meng, Grace',
            chamber='H',
            party='D',
            congress=113,
            state='NY'
        ),
        ParsedMember(
            name='Perry, Scott',
            chamber='H',
            party='R',
            congress=113,
            state='PA'
        ),
        ParsedMember(
            name='Weber, Randy K., Sr.',
            chamber='H',
            party='R',
            congress=113,
            state='TX'
        ),
        ParsedMember(
            name='Castro, Joaquin',
            chamber='H',
            party='D',
            congress=113,
            state='TX'
        ),
        ParsedMember(
            name='Kennedy, Joseph P., III',
            chamber='H',
            party='D',
            congress=113,
            state='MA'
        ),
        ParsedMember(
            name='Engel, Eliot L.',
            chamber='H',
            party='D',
            congress=113,
            state='NY'
        ),
        ParsedMember(
            name='Rohrabacher, Dana',
            chamber='H',
            party='R',
            congress=113,
            state='CA'
        ),
        ParsedMember(
            name='Ros-Lehtinen, Ileana',
            chamber='H',
            party='R',
            congress=113,
            state='FL'
        ),
        ParsedMember(
            name='Royce, Edward R.',
            chamber='H',
            party='R',
            congress=113,
            state='CA'
        ),
    ]


@pytest.fixture
def expected_parsed_mods(expected_parsed_committees, expected_parsed_members, expected_parsed_witnesses):
    return ParsedModsData(
        members=expected_parsed_members,
        committees=expected_parsed_committees,
        witnesses=expected_parsed_witnesses,
        uri='https://www.govinfo.gov/app/details/CHRG-113hhrg86466'
    )
