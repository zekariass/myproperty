
COUPON_CODE_LENGTH = 15
VOUCHER_CODE_LENGTH = 15

PERIODS = [
    ("DAY", "Day"),
    ("WEEK", "Week"),
    ("MONTH", "Month"),
    ("YEAR", "Year")
]


DISCOUNT_ACTIONS = [
    ("COUNT", "Count"),
    ("SINGLE", "Single"),
    ("DEADLINE", "Deadline")
]


DISCOUNT_UNITS = [
    ("DAYS", "Days"),
    ("LISTINGS", "Listings"),
    ("SUBSCRIPTION", "Subscription")
]

DISCOUNT_TYPES = [
    ("PAY_PER_LISTING", "Pay-per-listing"),
    ("SUBSCRIPTION", "Subscription")
]

AGENT_REQUEST_TYPES = [
    ("VIEW_PROPERTY", "View the property"),
    ("AVAILABILITY", "Check availability"),
    ("INFORMATION", "Get more information"),
]

AGENT_REQUEST_SENDER = [
    ("AGENT", "Agent"),
    ("CLIENT", "Client"),
]

LISTING_TYPE = [
    ("RENT", "Rent"),
    ("SALE", "Sale"),
]


AGENT_REFERRAL_COUPON_PARAM_NAME = "AGENT_REFERRAL_COUPON"

LISTING_PARAMETER_NAMES = [
    ("*", "*"),
    (AGENT_REFERRAL_COUPON_PARAM_NAME, "Agent Referral Coupon"),
]

MYPROPERY_SYSTEM_MODULE_NAME = "MYPROPERTY"

SYSTEM_MODULE_NAMES = [
    ("*", "*"),
    (MYPROPERY_SYSTEM_MODULE_NAME, "Property renting/selling system"),
]


APARTMENT_KEY = "PROPCAT001"
CONDOMINIUM_KEY = "PROPCAT002"
TOWNHOUSE_KEY = "PROPCAT003"
VILLA_KEY = "PROPCAT004"
SHAREHOUSE_KEY = "PROPCAT005"
COMMERCIAL_PROPERTY_KEY = "PROPCAT006"
VENUE_KEY = "PROPCAT007"
LAND_KEY = "PROPCAT008"

PROPERTY_CATEGORY_KEY = [
    (APARTMENT_KEY, 'Apartment'),
    (CONDOMINIUM_KEY, 'Condominium'),
    (TOWNHOUSE_KEY, 'Townhouse'),
    (VILLA_KEY, 'Villa'),
    (SHAREHOUSE_KEY, 'Sharehouse'),
    (COMMERCIAL_PROPERTY_KEY, 'Commercial Property'),
    (VENUE_KEY, 'Venue'),
    (LAND_KEY, 'Land'),
]

OTHER_COMMERCIAL_PROPERTY_UNIT = "OTHER_UNIT"
OFFICE_COMMERCIAL_PROPERTY_UNIT = "OFFICE_UNIT"

PROPERTY_TENURE_TYPES = [
    ("FREEHOLD", "Freehold"),
    ("LEASEHOLD", "Leasehold"),
    ("COMMONHOLD", "Commonhold"),
]


PROPERTY_TAX_BANDS = [
    ("BAND_A", "Band A"),
    ("BAND_B", "Band B"),
    ("BAND_C", "Band C"),
]


PROPERTY_STATUS = [
    ("NEW", "New"),
    ("RESTORED", "Restored"),
    ("IN_GOOD_CONDITION", "In Good Condition"),
    ("OLD", "OLD"),
]


PROPERTY_STRUCTURE = [
    ("DETACHED", "Detached"),
    ("SEMI_DETACHED", "Semi Detached"),
    ("TERRACED", "Terraced"),
    ("IN_COMPOUND", "In Compound"),
]


BUILDING_TYPES = [
    ("APARTMENT", "Apartment"),
    ("CONDOMINIUM", "Condominium"),
    ("TOWNHOUSE", "Townhouse"),
    ("VILLA", "Villa"),
    ("OTHER", "Other"),
]


GENDER = [
    ("MALE", "Male"),
    ("Female", "Female"),
    ("ANY", "Any")
]

USER_GROUP_AGENT = "AGENT"
USER_GROUP_ADMIN = "ADMIN"
USER_GROUP_ANY = "ANY"
AGENT_REFERRAL_CODE_INITIAL = "ARC_"
AGENT_BRANCH_CODE_INITIAL = "AB_"
PROPERTY_CUSTOM_ID_INITIAL = "PRO_"
