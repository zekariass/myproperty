
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


USER_GROUP_AGENT = "AGENT"
USER_GROUP_ADMIN = "ADMIN"
USER_GROUP_ANY = "ANY"
AGENT_REFERRAL_CODE_INITIAL = "ARC_"
AGENT_BRANCH_CODE_INITIAL = "AB_"