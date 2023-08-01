COUPON_CODE_LENGTH = 15
VOUCHER_CODE_LENGTH = 15

PERIODS = [("DAY", "Day"), ("WEEK", "Week"), ("MONTH", "Month"), ("YEAR", "Year")]


DISCOUNT_ACTIONS = [("COUNT", "Count"), ("SINGLE", "Single"), ("DEADLINE", "Deadline")]


DISCOUNT_UNITS = [
    ("DAYS", "Days"),
    ("LISTINGS", "Listings"),
    ("SUBSCRIPTION", "Subscription"),
]

DISCOUNT_TYPES = [
    ("PAY_PER_LISTING", "Pay-per-listing"),
    ("SUBSCRIPTION", "Subscription"),
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


LISTING_TYPE_RENT = "RENT"
LISTING_TYPE_SALE = "SALE"

LISTING_TYPE = [
    (LISTING_TYPE_RENT, "Rent"),
    (LISTING_TYPE_SALE, "Sale"),
]

# PAYMENT

PAYMENT_METHOD_CARD_PAYMENT = "CARD"
PAYMENT_METHOD_VOUCHER = "VOUCHER"
PAYMENT_METHOD_MOBILE_PAYMENT = "MOBILE_PAYMENT"
PAYMENT_METHOD_BANK_TRANSFER = "BANK_TRANSFER"

PAYMENT_METHODS = [
    (PAYMENT_METHOD_CARD_PAYMENT, "Card"),
    (PAYMENT_METHOD_VOUCHER, "Voucher"),
    (PAYMENT_METHOD_MOBILE_PAYMENT, "Mobile Payment"),
    (PAYMENT_METHOD_BANK_TRANSFER, "Bank Transfer"),
]

PAYMENT_PURPOSE_LISTING = "LISTING"
PAYMENT_PURPOSE_FEATURING = "FEATURING"
PAYMENT_PURPOSE_SUBSCRIPTION = "SUBSCRIPTION"
PAYMENT_PURPOSE_VOUCHER_PURCHASE = "VOUCHER_PURCHASE"

PAYMENT_PURPOSES = [
    (PAYMENT_PURPOSE_LISTING, PAYMENT_PURPOSE_LISTING),
    (PAYMENT_PURPOSE_FEATURING, PAYMENT_PURPOSE_FEATURING),
    (PAYMENT_PURPOSE_VOUCHER_PURCHASE, PAYMENT_PURPOSE_VOUCHER_PURCHASE),
]

TRANSACTION_REFERENCE_NUMBER_INITIAL = {
    PAYMENT_METHOD_VOUCHER: "VTRN_",
    PAYMENT_METHOD_BANK_TRANSFER: "BTRN_",
    PAYMENT_METHOD_MOBILE_PAYMENT: "MTRN_",
    PAYMENT_METHOD_CARD_PAYMENT: "CTRN_",
}


LISTING_PAYMENT_TYPES = [
    ("SUBSCRIPTION", "Subscription"),
    ("PAY_PER_LISTING", "Pay per listing"),
]

PAYMENT_APPROVAL_MODE_AUTO = "AUTO"
PAYMENT_APPROVAL_MODE_MANUAL = "MANUAL"

PAYMENT_APPROVAL_MODES = [
    (PAYMENT_APPROVAL_MODE_AUTO, "Automatic"),
    (PAYMENT_APPROVAL_MODE_MANUAL, "Manual"),
]

PAYMENT_REQUESTED_BY_AGENT = "AGENT"
PAYMENT_REQUESTED_BY_USER = "USER"


RENT_TERM = [("LONG_TERM", "Long term"), ("SHORT_TERM", "Short term")]

# LISTING PARAMS
AGENT_REFERRAL_COUPON = "AGENT_REFERRAL_COUPON"
LISTING_LIFE_TIME = "LISTING_LIFE_TIME"

LISTING_PARAMETER_NAMES = [
    ("*", "*"),
    (AGENT_REFERRAL_COUPON, "AGENT_REFERRAL_COUPON"),
    (LISTING_LIFE_TIME, "LISTING_LIFE_TIME"),
]

# SYSTEM PARAMS
VOUCHER_LIFE_TIME = "VOUCHER_LIFE_TIME"
COUPON_LIFE_TIME = "COUPON_LIFE_TIME"

SYSTEM_PARAMETER_NAMES = [
    ("*", "*"),
    (VOUCHER_LIFE_TIME, "VOUCHER_LIFE_TIME"),
    (COUPON_LIFE_TIME, "COUPON_LIFE_TIME"),
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
    (APARTMENT_KEY, "Apartment"),
    (CONDOMINIUM_KEY, "Condominium"),
    (TOWNHOUSE_KEY, "Townhouse"),
    (VILLA_KEY, "Villa"),
    (SHAREHOUSE_KEY, "Sharehouse"),
    (COMMERCIAL_PROPERTY_KEY, "Commercial Property"),
    (VENUE_KEY, "Venue"),
    (LAND_KEY, "Land"),
]

OTHER_COMMERCIAL_PROPERTY_UNIT = "OTHER_UNIT"
OFFICE_COMMERCIAL_PROPERTY_UNIT = "OFFICE_UNIT"
COMMERCIAL_PROPERTY_UNIT_TYPES = [
    (OTHER_COMMERCIAL_PROPERTY_UNIT, "Other unit"),
    (OFFICE_COMMERCIAL_PROPERTY_UNIT, "Office unit"),
]

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


GENDER = [("MALE", "Male"), ("Female", "Female"), ("ANY", "Any")]

USER_GROUP_AGENT = "AGENT"
USER_GROUP_ADMIN = "ADMIN"
USER_GROUP_ANY = "ANY"
AGENT_REFERRAL_CODE_INITIAL = "ARC_"
AGENT_BRANCH_CODE_INITIAL = "AB_"
PROPERTY_CUSTOM_ID_INITIAL = "PRO_"
PAYMENT_ORDER_INITIAL = "PO_"


# NOTIFICATIONS
# NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED = (
#     "NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED"
# )
NOTIFICATION_TOPIC_NEW_PROPERTY_ADDED = "NEW_PROPERTY_ADDED"
NOTIFICATION_TOPIC_NEW_LISTING_ADDED = "NEW_LISTING_ADDED"
NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED = "PAYMENT_ORDER_REQUESTED"
NOTIFICATION_TOPIC_PAYMENT_ORDER_APPROVED = "PAYMENT_ORDER_APPROVED"
# NOTIFICATION_TOPIC_FEATURING_PAYMENT_ORDER_REQUESTED = (
#     "FEATURING_PAYMENT_ORDER_REQUESTED"
# )
# NOTIFICATION_TOPIC_FEATURING_PAYMENT_OREDR_APPROVED = "FEATURING_PAYMENT_OREDR_APPROVED"
# NOTIFICATION_TOPIC_SUBSCRIPTION_PAYMENT_ORDER_REQUESTED = (
#     "SUBSCRIPTION_PAYMENT_ORDER_REQUESTED"
# )
# NOTIFICATION_TOPIC_SUBSCRIPTION_PAYMENT_OREDR_APPROVED = (
#     "SUBSCRIPTION_PAYMENT_OREDR_APPROVED"
# )
NOTIFICATION_TOPIC_MARKETING = "MARKETING"
NOTIFICATION_TOPIC_LISTING_VIEWED = "LISTING_VIEWED"

NOTIFICATION_TOPICS = [
    (NOTIFICATION_TOPIC_NEW_PROPERTY_ADDED, "New Property Addded"),
    (NOTIFICATION_TOPIC_NEW_LISTING_ADDED, "New Listing Addded"),
    (
        NOTIFICATION_TOPIC_PAYMENT_ORDER_REQUESTED,
        "Payment Order Requested",
    ),
    (
        NOTIFICATION_TOPIC_PAYMENT_ORDER_APPROVED,
        "Payment Order Approved",
    ),
    (NOTIFICATION_TOPIC_MARKETING, "Marketing"),
    (NOTIFICATION_TOPIC_LISTING_VIEWED, "Listing Viewed"),
]

NOTIFICATION_TARGET_GROUP_USER = "USER"
NOTIFICATION_TARGET_GROUP_AGENT = "AGENT"
NOTIFICATION_TARGET_GROUPS = [
    (NOTIFICATION_TARGET_GROUP_USER, "User"),
    (NOTIFICATION_TARGET_GROUP_AGENT, "Agent"),
]

NOTIFICATION_CHANNEL_EMAIL = "EMAIL"
NOTIFICATION_CHANNEL_IN_APP = "IN_APP"
NOTIFICATION_CHANNEL_SMS = "SMS"

NOTIFICATION_CHANNELS = [
    (NOTIFICATION_CHANNEL_EMAIL, "Email"),
    (NOTIFICATION_CHANNEL_IN_APP, "In App"),
    (NOTIFICATION_CHANNEL_SMS, "SMS"),
]
